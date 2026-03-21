"""
Tests for Ludwig database module
"""

import pytest
import tempfile
import os
from dataclasses import dataclass
from ludwig.db import Database, Model, QueryBuilder


class TestDatabase:
    """Test Database class."""
    
    def test_database_creation(self):
        """Test creating a database."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        try:
            db = Database(db_path)
            assert db is not None
            db.close()
        finally:
            os.unlink(db_path)
    
    def test_create_table(self):
        """Test creating a table."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        try:
            db = Database(db_path)
            db.create_table("users", {"name": "TEXT", "age": "INTEGER"})
            
            # Table should exist
            result = db.query("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            assert len(result) == 1
            db.close()
        finally:
            os.unlink(db_path)
    
    def test_query_builder(self):
        """Test query builder."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        try:
            db = Database(db_path)
            db.create_table("items", {"name": "TEXT", "price": "REAL"})
            
            # Insert
            item_id = db.table("items").insert({"name": "Widget", "price": 9.99})
            assert item_id is not None
            
            # Select
            items = db.table("items").get()
            assert len(items) == 1
            assert items[0]["name"] == "Widget"
            
            # Update
            db.table("items").where("id", item_id).update({"price": 19.99})
            item = db.table("items").where("id", item_id).first()
            assert item["price"] == 19.99
            
            # Delete
            db.table("items").where("id", item_id).delete()
            items = db.table("items").get()
            assert len(items) == 0
            
            db.close()
        finally:
            os.unlink(db_path)


class TestModel:
    """Test Model class."""
    
    def test_model_crud(self):
        """Test Model CRUD operations."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        try:
            # Setup database
            db = Database(db_path)
            
            @dataclass
            class User(Model):
                name: str
                email: str
            
            # Create
            user = User.create(name="Alice", email="alice@test.com")
            assert user.id is not None
            assert user.name == "Alice"
            
            # Read
            found = User.find(user.id)
            assert found is not None
            assert found.name == "Alice"
            
            # Update
            found.name = "Alice Smith"
            found.save()
            
            updated = User.find(user.id)
            assert updated.name == "Alice Smith"
            
            # Delete
            updated.delete()
            deleted = User.find(user.id)
            assert deleted is None
            
            db.close()
        finally:
            os.unlink(db_path)
    
    def test_model_where(self):
        """Test Model.where query."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        try:
            db = Database(db_path)
            
            @dataclass
            class Product(Model):
                name: str
                price: float = 0.0
            
            Product.create(name="Widget", price=10.0)
            Product.create(name="Gadget", price=20.0)
            Product.create(name="Gizmo", price=15.0)
            
            # Query
            expensive = Product.where("price", ">=", 15.0)
            assert len(expensive) == 2
            
            db.close()
        finally:
            os.unlink(db_path)
