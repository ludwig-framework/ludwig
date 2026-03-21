"""
Ludwig AI - Voice assistant
"""

from typing import Callable, Optional
import os


class Assistant:
    """
    AI voice assistant.
    
    Example:
        assistant = Assistant(
            name="Ludwig",
            model="gpt-4o",
            voice="alloy",
        )
        
        @assistant.on_wake("Hey Ludwig")
        def handle():
            command = assistant.listen()
            response = assistant.think(command)
            assistant.speak(response)
        
        # Or just chat
        response = assistant.chat("What's the weather like?")
        print(response)
        
        assistant.run()
    """
    
    def __init__(
        self,
        name: str = "Assistant",
        model: str = "gpt-4o",
        voice: str = "alloy",
        wake_word: str = None,
        instructions: str = None,
    ):
        self.name = name
        self.model = model
        self.voice = voice
        self.wake_word = wake_word or f"Hey {name}"
        self.instructions = instructions or f"You are {name}, a helpful voice assistant."
        
        self._messages = []
        self._callbacks: dict[str, list[Callable]] = {}
        self._running = False
        
        # Lazy-loaded clients
        self._openai = None
        self._speech_recognizer = None
    
    def _get_openai(self):
        """Get OpenAI client."""
        if self._openai is None:
            try:
                from openai import OpenAI
                self._openai = OpenAI()
            except ImportError:
                print("Install openai: pip install openai")
                return None
        return self._openai
    
    def _get_speech_recognizer(self):
        """Get speech recognition engine."""
        if self._speech_recognizer is None:
            try:
                import speech_recognition as sr
                self._speech_recognizer = sr.Recognizer()
            except ImportError:
                print("Install speech_recognition: pip install SpeechRecognition")
                return None
        return self._speech_recognizer
    
    # === Chat ===
    
    def chat(self, message: str) -> str:
        """Send a message and get a response."""
        client = self._get_openai()
        if not client:
            return "[AI not available]"
        
        self._messages.append({"role": "user", "content": message})
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.instructions},
                *self._messages
            ]
        )
        
        reply = response.choices[0].message.content
        self._messages.append({"role": "assistant", "content": reply})
        
        return reply
    
    def think(self, prompt: str) -> str:
        """Alias for chat()."""
        return self.chat(prompt)
    
    def clear_history(self):
        """Clear conversation history."""
        self._messages = []
    
    # === Voice ===
    
    def listen(self, timeout: int = 5) -> str:
        """Listen for voice input."""
        recognizer = self._get_speech_recognizer()
        if not recognizer:
            # Fallback to text input
            return input(f"{self.name} is listening: ")
        
        import speech_recognition as sr
        
        with sr.Microphone() as source:
            print(f"🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                audio = recognizer.listen(source, timeout=timeout)
                text = recognizer.recognize_google(audio)
                print(f"   You: {text}")
                return text
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                print("   Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"   Speech recognition error: {e}")
                return ""
    
    def speak(self, text: str):
        """Speak text using TTS."""
        print(f"🔊 {self.name}: {text}")
        
        client = self._get_openai()
        if not client:
            return
        
        try:
            response = client.audio.speech.create(
                model="tts-1",
                voice=self.voice,
                input=text,
            )
            
            # Play audio
            import tempfile
            import subprocess
            
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                f.write(response.content)
                temp_path = f.name
            
            # Platform-specific playback
            import platform
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["afplay", temp_path], check=True)
            elif platform.system() == "Linux":
                subprocess.run(["mpg123", "-q", temp_path], check=True)
            
            os.unlink(temp_path)
            
        except Exception as e:
            print(f"   TTS error: {e}")
    
    def detect_wake_word(self, audio_text: str) -> bool:
        """Check if wake word was spoken."""
        return self.wake_word.lower() in audio_text.lower()
    
    # === Events ===
    
    def on(self, event: str):
        """Register event handler."""
        def decorator(func: Callable):
            if event not in self._callbacks:
                self._callbacks[event] = []
            self._callbacks[event].append(func)
            return func
        return decorator
    
    def on_wake(self, wake_word: str = None):
        """Handler for wake word detection."""
        if wake_word:
            self.wake_word = wake_word
        return self.on("wake")
    
    def on_command(self, command: str):
        """
        Handler for specific commands.
        
        Example:
            @assistant.on_command("turn on lights")
            def lights_on():
                home.all_lights_on()
        """
        return self.on(f"command:{command.lower()}")
    
    # === Run Loop ===
    
    def run(self, continuous: bool = True):
        """
        Start listening for wake word.
        
        Args:
            continuous: Keep listening after handling command
        """
        self._running = True
        print(f"🎤 {self.name} listening for '{self.wake_word}'...")
        
        try:
            while self._running:
                text = self.listen(timeout=10)
                
                if text and self.detect_wake_word(text):
                    # Trigger wake handlers
                    for handler in self._callbacks.get("wake", []):
                        handler()
                    
                    # Check for specific commands
                    for event, handlers in self._callbacks.items():
                        if event.startswith("command:"):
                            cmd = event[8:]
                            if cmd in text.lower():
                                for handler in handlers:
                                    handler()
                    
                    if not continuous:
                        break
                
        except KeyboardInterrupt:
            print(f"\n🎤 {self.name} stopped")
    
    def stop(self):
        """Stop listening."""
        self._running = False
    
    def __repr__(self):
        return f"Assistant(name={self.name}, model={self.model})"
