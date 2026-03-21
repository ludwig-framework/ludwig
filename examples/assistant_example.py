"""
Voice Assistant Example
Requires: pip install ludwig[ai]
Set OPENAI_API_KEY environment variable.
"""

from ludwig.ai import Assistant

assistant = Assistant(
    name="Ludwig",
    model="gpt-4o",
    voice="alloy",
)


@assistant.on_wake("Hey Ludwig")
def handle_wake():
    command = assistant.listen()
    response = assistant.think(command)
    assistant.speak(response)


@assistant.on_command("turn on lights")
def lights_on():
    assistant.speak("Lights are on")


if __name__ == "__main__":
    print("🎙️ Voice Assistant")
    print("Say 'Hey Ludwig' to start...")
    assistant.run()
