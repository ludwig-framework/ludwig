"""
Ludwig AI - Natural language automation
"""

from typing import Any, Callable, Optional
import re
from datetime import datetime


class Automator:
    """
    Natural language automation engine.
    
    Define automation rules in plain English.
    
    Example:
        auto = Automator()
        
        # Define context (devices, sensors, etc.)
        auto.context = {
            "lights": home.all_lights,
            "temperature": living.temperature,
            "ac": home.device("ac"),
        }
        
        # Add rules in natural language
        auto.add_rule("Turn off all lights at midnight")
        auto.add_rule("If temperature > 28, turn on AC")
        auto.add_rule("When motion detected, turn on lights for 5 minutes")
        auto.add_rule("Send daily summary email at 8am")
        
        auto.run()
    """
    
    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.context: dict[str, Any] = {}
        self._rules: list[dict] = []
        self._schedules: list[tuple[str, Callable]] = []
        self._running = False
        self._openai = None
    
    def _get_openai(self):
        """Get OpenAI client."""
        if self._openai is None:
            try:
                from openai import OpenAI
                self._openai = OpenAI()
            except ImportError:
                return None
        return self._openai
    
    def add_rule(self, rule: str):
        """
        Add an automation rule in natural language.
        
        The AI will parse and convert to executable logic.
        """
        parsed = self._parse_rule(rule)
        self._rules.append({
            "text": rule,
            "parsed": parsed,
        })
        print(f"✓ Rule added: {rule}")
    
    def _parse_rule(self, rule: str) -> dict:
        """
        Parse natural language rule into structured format.
        
        Returns dict with:
        - trigger: "time", "condition", "event"
        - condition: Optional condition to check
        - action: What to do
        """
        rule_lower = rule.lower()
        
        # Time-based triggers
        time_patterns = [
            (r"at (\d{1,2}(?::\d{2})?\s*(?:am|pm)?)", "time"),
            (r"at (midnight|noon|sunrise|sunset)", "time"),
            (r"every (\d+)\s*(hour|minute|second|day)s?", "interval"),
            (r"daily at (\d{1,2}(?::\d{2})?)", "daily"),
        ]
        
        for pattern, trigger_type in time_patterns:
            match = re.search(pattern, rule_lower)
            if match:
                return {
                    "trigger": trigger_type,
                    "value": match.group(1),
                    "action": self._extract_action(rule),
                }
        
        # Condition-based triggers
        condition_patterns = [
            (r"if (.+?),\s*(.+)", "condition"),
            (r"when (.+?),\s*(.+)", "event"),
        ]
        
        for pattern, trigger_type in condition_patterns:
            match = re.search(pattern, rule_lower)
            if match:
                return {
                    "trigger": trigger_type,
                    "condition": match.group(1),
                    "action": match.group(2),
                }
        
        # Default: treat as immediate action
        return {
            "trigger": "immediate",
            "action": rule,
        }
    
    def _extract_action(self, rule: str) -> str:
        """Extract action from rule."""
        # Remove time-related prefix
        patterns = [
            r"at \d{1,2}(?::\d{2})?\s*(?:am|pm)?\s*,?\s*",
            r"at (?:midnight|noon|sunrise|sunset)\s*,?\s*",
            r"every \d+\s*(?:hour|minute|second|day)s?\s*,?\s*",
            r"daily at \d{1,2}(?::\d{2})?\s*,?\s*",
        ]
        
        action = rule
        for pattern in patterns:
            action = re.sub(pattern, "", action, flags=re.IGNORECASE)
        
        return action.strip()
    
    def _check_condition(self, condition: str) -> bool:
        """Evaluate a condition using AI or pattern matching."""
        condition_lower = condition.lower()
        
        # Temperature checks
        match = re.search(r"temperature\s*([<>=]+)\s*(\d+)", condition_lower)
        if match:
            op, value = match.group(1), int(match.group(2))
            temp = self.context.get("temperature", 0)
            if callable(temp):
                temp = temp()
            
            if op == ">":
                return temp > value
            elif op == "<":
                return temp < value
            elif op in ("=", "=="):
                return temp == value
            elif op == ">=":
                return temp >= value
            elif op == "<=":
                return temp <= value
        
        # Motion detected
        if "motion" in condition_lower and "detected" in condition_lower:
            motion = self.context.get("motion")
            if motion and callable(motion):
                return motion()
            return bool(motion)
        
        # Time of day
        if "after sunset" in condition_lower or "dark" in condition_lower:
            hour = datetime.now().hour
            return hour >= 18 or hour < 6
        
        if "daytime" in condition_lower:
            hour = datetime.now().hour
            return 6 <= hour < 18
        
        return False
    
    def _execute_action(self, action: str):
        """Execute an action using AI or pattern matching."""
        action_lower = action.lower()
        
        print(f"⚡ Executing: {action}")
        
        # Turn on/off patterns
        if "turn on" in action_lower or "switch on" in action_lower:
            for key in ["lights", "light", "ac", "fan", "heater"]:
                if key in action_lower:
                    device = self.context.get(key)
                    if device:
                        if callable(device):
                            device()
                        elif hasattr(device, 'on'):
                            device.on()
                        elif hasattr(device, '__iter__'):
                            for d in device:
                                if hasattr(d, 'on'):
                                    d.on()
                    return
        
        if "turn off" in action_lower or "switch off" in action_lower:
            for key in ["lights", "light", "ac", "fan", "heater"]:
                if key in action_lower:
                    device = self.context.get(key)
                    if device:
                        if hasattr(device, 'off'):
                            device.off()
                        elif hasattr(device, '__iter__'):
                            for d in device:
                                if hasattr(d, 'off'):
                                    d.off()
                    return
        
        # Send notifications
        if "send" in action_lower:
            if "email" in action_lower:
                print(f"📧 [Would send email]")
            elif "sms" in action_lower:
                print(f"📱 [Would send SMS]")
            elif "notification" in action_lower:
                print(f"🔔 [Would send notification]")
            return
        
        # If we can't handle it, try AI
        self._execute_with_ai(action)
    
    def _execute_with_ai(self, action: str):
        """Use AI to figure out how to execute action."""
        client = self._get_openai()
        if not client:
            print(f"   Could not execute: {action}")
            return
        
        # Build context description
        context_desc = "\n".join([
            f"- {name}: {type(obj).__name__}"
            for name, obj in self.context.items()
        ])
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"""You are a home automation assistant.
Available devices/context:
{context_desc}

Convert the user's action into Python code that uses these objects.
Only output the Python code, nothing else."""},
                {"role": "user", "content": action}
            ]
        )
        
        code = response.choices[0].message.content
        print(f"   Generated: {code}")
        
        # Execute the generated code (careful!)
        try:
            exec(code, self.context)
        except Exception as e:
            print(f"   Error: {e}")
    
    def _check_time(self, time_spec: str) -> bool:
        """Check if it's the specified time."""
        now = datetime.now()
        
        if time_spec == "midnight":
            return now.hour == 0 and now.minute == 0
        elif time_spec == "noon":
            return now.hour == 12 and now.minute == 0
        elif time_spec == "sunrise":
            return now.hour == 6 and now.minute == 0
        elif time_spec == "sunset":
            return now.hour == 18 and now.minute == 0
        
        # Parse HH:MM or H am/pm
        match = re.match(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", time_spec)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2) or 0)
            ampm = match.group(3)
            
            if ampm == "pm" and hour < 12:
                hour += 12
            elif ampm == "am" and hour == 12:
                hour = 0
            
            return now.hour == hour and now.minute == minute
        
        return False
    
    # === Run Loop ===
    
    def run(self):
        """Start automation engine."""
        self._running = True
        print(f"🤖 Automator running with {len(self._rules)} rules...")
        
        import time
        last_triggered = {}
        
        try:
            while self._running:
                now_ts = time.time()
                
                for rule in self._rules:
                    parsed = rule["parsed"]
                    rule_id = id(rule)
                    
                    # Prevent re-triggering within 60 seconds
                    if rule_id in last_triggered:
                        if now_ts - last_triggered[rule_id] < 60:
                            continue
                    
                    should_execute = False
                    
                    if parsed["trigger"] == "time":
                        should_execute = self._check_time(parsed["value"])
                    
                    elif parsed["trigger"] == "condition":
                        should_execute = self._check_condition(parsed["condition"])
                    
                    elif parsed["trigger"] == "event":
                        should_execute = self._check_condition(parsed["condition"])
                    
                    if should_execute:
                        self._execute_action(parsed["action"])
                        last_triggered[rule_id] = now_ts
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🤖 Automator stopped")
    
    def stop(self):
        """Stop automation."""
        self._running = False
    
    def evaluate(self, prompt: str) -> str:
        """
        Evaluate a natural language query about the system.
        
        Example:
            result = auto.evaluate("Is it too hot in the living room?")
        """
        client = self._get_openai()
        if not client:
            return "AI not available"
        
        # Build context
        context_data = {}
        for name, obj in self.context.items():
            if callable(obj):
                context_data[name] = obj()
            else:
                context_data[name] = str(obj)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"""You are a home automation assistant.
Current state:
{context_data}

Answer the user's question based on this data."""},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
    
    def __repr__(self):
        return f"Automator(rules={len(self._rules)})"
