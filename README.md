# 🌿AI Flask Web App

A sleek **Flask web application** powered by **Google's Gemini AI** (`gemini-1.5-flash` model) with a modern **green & black theme** interface.  
Users can ask questions, and the AI will respond instantly, all within a responsive, stylish UI.

---

## 📌 Features

- **Google Gemini AI Integration** – Uses the latest `gemini-1.5-flash` model for instant AI answers.
- **Flask Backend** – Lightweight, fast, and scalable.
- **Green & Black Modern UI** – Elegant theme with responsive design.
- **Environment Variable Support** – Secure API key handling with `.env` file.
- **JSON API Endpoint** – `/ask` endpoint returns AI responses in JSON format.

---

## 📂 Project Structure
Flask-App/
│── app.py # Main Flask application
│── templates/
│ └── index.html # Frontend HTML
│── static/
│ └── style.css # CSS styling
│── .env # API key storage (ignored by Git)
│── .gitignore # Ignore sensitive & unnecessary files
│── README.md # Project documentation

## 🚀 Running the Application
bash
Copy
Edit
python app.py
The app will run at:

cpp
Copy
Edit
http://127.0.0.1:5000