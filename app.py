import os
import logging
from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
from dotenv import load_dotenv
from markdown import markdown
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ Please set GEMINI_API_KEY in your .env file")

# ------------------------------
# Configure Gemini API
# ------------------------------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ------------------------------
# Flask App Setup
# ------------------------------
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for session storage

# ------------------------------
# Logging Setup
# ------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)

# ------------------------------
# Rate Limiter
# ------------------------------
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["20 per minute"]  # 20 requests per minute
)

# ------------------------------
# Routes
# ------------------------------
@app.route("/")
def index():
    # Initialize session chat history
    if "chat_history" not in session:
        session["chat_history"] = []
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
@limiter.limit("5 per 10 seconds")  # Prevent flooding
def ask():
    try:
        data = request.get_json()
        user_input = data.get("question", "").strip()

        if not user_input:
            return jsonify({"error": "⚠️ Question cannot be empty"}), 400

        logging.info(f"User asked: {user_input}")

        # Append user message to history
        session.setdefault("chat_history", []).append({"role": "user", "text": user_input})

        # Send prompt with conversation history
        chat_input = "\n".join(
            f"{msg['role'].capitalize()}: {msg['text']}"
            for msg in session["chat_history"]
        )

        # Call Gemini API
        response = model.generate_content(chat_input)

        if not response or not hasattr(response, "text") or not response.text.strip():
            raise ValueError("⚠️ Empty response from Gemini API")

        answer_text = response.text.strip()

        # Append bot reply to history
        session["chat_history"].append({"role": "assistant", "text": answer_text})
        session.modified = True  # Save session changes

        # Convert markdown to HTML for better formatting
        answer_html = markdown(answer_text)

        return jsonify({"answer": answer_html})

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/clear", methods=["POST"])
def clear_history():
    session.pop("chat_history", None)
    return jsonify({"message": "Chat history cleared ✅"})

# ------------------------------
# Run Server
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
