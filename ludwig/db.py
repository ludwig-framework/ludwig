"""
Ludwig Database - Simple database abstraction
"""

from typing import Any, Optional, Type, TypeVar
from dataclasses import dataclass, field, fields
import json
import sqlite3
import os

T = TypeVar("T", bound="Model")


class Database:
    """
    Simple database wrapper.
    
    Example:
        db = Database("app.db")  # SQLite
        db = Database("postgres://...")  # PostgreSQL
        
        # Query builder
        users = db.table("users").where("age", ">", 18).get()
        
        # Raw queries
        results = db.query("SELECT * FROM users WHERE name = ?", ["Alice"])
    """
    
    _instance: Optional["Database"] = None
    
    def __init__(self, url: str = "app.db"):
        self.url = url
        self._conn = None
        
        Database._instance = self
    
    @classmethod
    def get(cls) -> "Database":
        """Get the current database instance."""
        if cls._instance is None:
            cls._instance = Database()
        return cls._instance
    
    def connect(self):
        """Connect to database."""
        if self._conn:
            return self._conn
        
        if self.url.startswith("postgres://") or self.url.startswith("postgresql://"):
            import psycopg2
            self._conn = psycopg2.connect(self.url)
        else:
            # SQLite
            self._conn = sqlite3.connect(self.url)
            self._conn.row_factory = sqlite3.Row
        
        return self._conn
    
    def query(self, sql: str, params: list = None) -> list[dict]:
        """Execute a raw SQL query."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params or [])
        
        if sql.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        else:
            conn.commit()
            return []
    
    def table(self, name: str) -> "QueryBuilder":
        """Start a query on a table."""
        return QueryBuilder(self, name)
    
    def create_table(self, name: str, schema: dict):
        """
        Create a table.
        
        Args:
            name: Table name
            schema: Column definitions {"name": "TEXT", "age": "INTEGER"}
        """
        columns = ", ".join([
            f"{col} {dtype}" for col, dtype in schema.items()
        ])
        
        sql = f"CREATE TABLE IF NOT EXISTS {name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})"
        self.query(sql)
    
    def close(self):
        """Close database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None


class QueryBuilder:
    """Fluent query builder."""
    
    def __init__(self, db: Database, table: str):
        self.db = db
        self.table_name = table
        self._select = ["*"]
        self._where: list[tuple] = []
        self._order: list[tuple] = []
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None
    
    def select(self, *columns: str) -> "QueryBuilder":
        """Select specific columns."""
        self._select = list(columns)
        return self
    
    def where(self, column: str, operator: str = "=", value: Any = None) -> "QueryBuilder":
        """Add WHERE condition."""
        if value is None:
            value = operator
            operator = "="
        self._where.append((column, operator, value))
        return self
    
    def order_by(self, column: str, direction: str = "ASC") -> "QueryBuilder":
        """Add ORDER BY."""
        self._order.append((column, direction.upper()))
        return self
    
    def limit(self, count: int) -> "QueryBuilder":
        """Limit results."""
        self._limit = count
        return self
    
    def offset(self, count: int) -> "QueryBuilder":
        """Offset results."""
        self._offset = count
        return self
    
    def _build_query(self) -> tuple[str, list]:
        """Build the SQL query."""
        params = []
        
        # SELECT
        columns = ", ".join(self._select)
        sql = f"SELECT {columns} FROM {self.table_name}"
        
        # WHERE
        if self._where:
            conditions = []
            for col, op, val in self._where:
                conditions.append(f"{col} {op} ?")
                params.append(val)
            sql += " WHERE " + " AND ".join(conditions)
        
        # ORDER BY
        if self._order:
            orders = [f"{col} {dir}" for col, dir in self._order]
            sql += " ORDER BY " + ", ".join(orders)
        
        # LIMIT
        if self._limit:
            sql += f" LIMIT {self._limit}"
        
        # OFFSET
        if self._offset:
            sql += f" OFFSET {self._offset}"
        
        return sql, params
    
    def get(self) -> list[dict]:
        """Execute query and return results."""
        sql, params = self._build_query()
        return self.db.query(sql, params)
    
    def first(self) -> Optional[dict]:
        """Get first result."""
        self._limit = 1
        results = self.get()
        return results[0] if results else None
    
    def count(self) -> int:
        """Count results."""
        self._select = ["COUNT(*) as count"]
        result = self.first()
        return result["count"] if result else 0
    
    def insert(self, data: dict) -> int:
        """Insert a row."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = list(data.values())
        
        sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        
        return cursor.lastrowid
    
    def update(self, data: dict) -> int:
        """Update rows matching WHERE conditions."""
        sets = ", ".join([f"{col} = ?" for col in data.keys()])
        params = list(data.values())
        
        sql = f"UPDATE {self.table_name} SET {sets}"
        
        if self._where:
            conditions = []
            for col, op, val in self._where:
                conditions.append(f"{col} {op} ?")
                params.append(val)
            sql += " WHERE " + " AND ".join(conditions)
        
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        
        return cursor.rowcount
    
    def delete(self) -> int:
        """Delete rows matching WHERE conditions."""
        params = []
        sql = f"DELETE FROM {self.table_name}"
        
        if self._where:
            conditions = []
            for col, op, val in self._where:
                conditions.append(f"{col} {op} ?")
                params.append(val)
            sql += " WHERE " + " AND ".join(conditions)
        
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        
        return cursor.rowcount


class Model:
    """
    Base model class for ORM-style data access.
    
    Subclasses should be decorated with @dataclass:
    
        @dataclass
        class User(Model):
            name: str
            email: str
            age: int = 0
        
        # Create
        user = User(name="Alice", email="alice@example.com")
        user.save()
        
        # Query
        users = User.all()
        user = User.find(1)
        adults = User.where("age", ">=", 18)
        
        # Update
        user.name = "Alice Smith"
        user.save()
        
        # Delete
        user.delete()
    """
    
    id: int = None
    
    @classmethod
    def table_name(cls) -> str:
        """Get table name (lowercase class name + 's')."""
        return cls.__name__.lower() + "s"
    
    @classmethod
    def _db(cls) -> Database:
        """Get database instance."""
        return Database.get()
    
    @classmethod
    def _ensure_table(cls):
        """Create table if it doesn't exist."""
        schema = {}
        for f in fields(cls):
            if f.name == "id":
                continue
            
            # Map Python types to SQL types
            type_map = {
                str: "TEXT",
                int: "INTEGER",
                float: "REAL",
                bool: "INTEGER",
            }
            
            origin = getattr(f.type, "__origin__", None)
            if origin is not None:
                # Handle Optional[X]
                args = getattr(f.type, "__args__", ())
                for arg in args:
                    if arg is not type(None):
                        sql_type = type_map.get(arg, "TEXT")
                        break
                else:
                    sql_type = "TEXT"
            else:
                sql_type = type_map.get(f.type, "TEXT")
            
            schema[f.name] = sql_type
        
        cls._db().create_table(cls.table_name(), schema)
    
    @classmethod
    def all(cls: Type[T]) -> list[T]:
        """Get all records."""
        cls._ensure_table()
        rows = cls._db().table(cls.table_name()).get()
        instances = []
        for row in rows:
            row.pop("id", None)
            instance = cls(**row)
            instances.append(instance)
        return instances
    
    @classmethod
    def find(cls: Type[T], id: int) -> Optional[T]:
        """Find by ID."""
        cls._ensure_table()
        row = cls._db().table(cls.table_name()).where("id", id).first()
        if row:
            row.pop("id", None)
            instance = cls(**row)
            instance.id = id
            return instance
        return None
    
    @classmethod
    def where(cls: Type[T], column: str, operator: str = "=", value: Any = None) -> list[T]:
        """Query with conditions."""
        cls._ensure_table()
        rows = cls._db().table(cls.table_name()).where(column, operator, value).get()
        instances = []
        for row in rows:
            row_id = row.pop("id", None)
            instance = cls(**row)
            instance.id = row_id
            instances.append(instance)
        return instances
    
    @classmethod
    def create(cls: Type[T], **kwargs) -> T:
        """Create and save a new record."""
        instance = cls(**kwargs)
        instance.save()
        return instance
    
    def save(self):
        """Save the model (insert or update)."""
        self._ensure_table()
        
        data = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        model_id = data.pop("id", None)
        
        if model_id:
            # Update
            self._db().table(self.table_name()).where("id", model_id).update(data)
        else:
            # Insert
            new_id = self._db().table(self.table_name()).insert(data)
            self.id = new_id
    
    def delete(self):
        """Delete the model."""
        if self.id:
            self._db().table(self.table_name()).where("id", self.id).delete()
            self.id = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
    
    def to_json(self) -> str:
        """Convert to JSON."""
        return json.dumps(self.to_dict())
    
    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
