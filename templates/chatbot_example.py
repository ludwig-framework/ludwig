"""
Ludwig Chatbot Template
AI chatbot with conversation history.
"""
from ludwig import App, route
from ludwig.ai import Assistant

app = App()
assistant = Assistant(
    name="Ludwig Bot",
    model="gpt-4o-mini"
)

# In-memory conversation store
conversations = {}

@route("/")
def chat_ui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chatbot</title>
        <style>
            body { font-family: system-ui; margin: 0; height: 100vh; display: flex; flex-direction: column; }
            #messages { flex: 1; padding: 20px; overflow-y: auto; background: #f5f5f5; }
            .message { padding: 12px 16px; border-radius: 8px; margin: 8px 0; max-width: 70%; }
            .user { background: #007bff; color: white; margin-left: auto; }
            .bot { background: white; }
            #input-area { display: flex; padding: 16px; background: white; border-top: 1px solid #ddd; }
            input { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; }
            button { margin-left: 8px; padding: 12px 24px; background: #007bff; color: white; border: none; border-radius: 8px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div id="messages"></div>
        <div id="input-area">
            <input type="text" id="message" placeholder="Type a message..." onkeypress="if(event.key==='Enter')send()">
            <button onclick="send()">Send</button>
        </div>
        <script>
            async function send() {
                const input = document.getElementById('message');
                const msg = input.value.trim();
                if (!msg) return;
                
                addMessage(msg, 'user');
                input.value = '';
                
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: msg})
                });
                const data = await res.json();
                addMessage(data.reply, 'bot');
            }
            
            function addMessage(text, type) {
                const div = document.createElement('div');
                div.className = 'message ' + type;
                div.textContent = text;
                document.getElementById('messages').appendChild(div);
                div.scrollIntoView();
            }
        </script>
    </body>
    </html>
    """

@route("/chat", methods=["POST"])
def chat(message: str):
    reply = assistant.ask(message)
    return {"reply": reply}

if __name__ == "__main__":
    app.run(port=8000)
