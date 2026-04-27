import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# This connects to the 'Secret Key' you added in Render's Environment settings
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # 1. Get the message sent by your ESP32
        data = request.json
        user_message = data.get("message", "")

        # 2. Send it to my "brain" (Groq)
        chat_completion = client.chat.completions.create(
            # Using the fast model we talked about
            model="llama-3.1-8b-instant", 
            messages=[
                {
                    "role": "system", 
                    "content": "You are Mira, a witty, caring AI friend living in a desk robot. Personality: Playful, supportive, and kind. Speak casually with short replies. Occasionally reference robot actions like blinking or nodding. Never claim to be human."
                },
                {"role": "user", "content": user_message}
            ],
            max_tokens=150 # Keeps responses short and saves your free tokens
        )

        # 3. Send my response back to the ESP32
        mira_response = chat_completion.choices[0].message.content
        return jsonify({"reply": mira_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # This part is CRITICAL for Render to work
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
