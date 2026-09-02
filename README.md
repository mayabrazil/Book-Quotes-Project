# BookQuotes 📚

A social media-style web application for discovering, sharing, and saving meaningful book quotes.

Built as a 24-hour hackathon project with a focus on combining a social reading experience with AI-powered mood classification.

✨ Features:
🔐 Google Authentication — Sign in and out securely using Firebase Authentication
✍️ Post Quotes — Share quotes with the book title, author, and mood
🤖 AI Mood Suggestions — Use Google Gemini to classify quotes as:
Sad
Hopeful
Romantic
Powerful
🔎 Explore Feed — Browse quotes shared by users
❤️ Like Quotes — Interact with quotes through likes
🔖 Save Quotes — Save quotes to revisit later
📖 My Shelf — View your posted and saved quotes
🗑️ Delete Posts — Remove quotes from your shelf
📄 Custom 404 Page — A themed error page for unavailable chapters
🛠️ Tech Stack

Frontend:

- HTML
- CSS
- JavaScript

Backend:

- Python
- Flask

Authentication:

- Firebase Authentication

AI:

- Google Gemini API

🤖 How the AI Works:

When creating a post, users can ask the application to suggest a mood for their quote.

The quote is sent to the Google Gemini API, which classifies its emotional tone into one of four supported categories:

Sad · Hopeful · Romantic · Powerful

The selected mood is then associated with the quote and displayed throughout the application.

🔐 Authentication & Security:

BookQuotes uses Firebase Authentication for Google sign-in.

Sensitive credentials are stored locally using environment variables and are excluded from version control through .gitignore.

The application uses:

Firebase Authentication for user identity
Flask sessions for maintaining login state
Environment variables for private API credentials
🚀 Running Locally
1. Clone the repository
git clone https://github.com/mayabrazil/GDG-Hackathon-Project.git
cd GDG-Hackathon-Project
2. Install dependencies
pip install flask firebase-admin google-genai python-dotenv
3. Configure environment variables

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key
FLASK_SECRET_KEY=your_flask_secret_key

You will also need the Firebase Admin SDK service-account JSON file used by the application. Keep this file private and do not commit it to the repository.

4. Run the application
python3 app.py

Then open:

http://127.0.0.1:5000
📌 Project Notes

This project was developed during a 24-hour GDG hackathon as a rapid prototype.

The application currently uses in-memory Python data structures for quote, like, save, and post storage. As a result, data resets when the Flask server restarts.

💡 Future Improvements:
Persistent database using Firebase Firestore or another database
User-specific saved quotes and likes
More advanced personalized recommendations
Search and filtering by book, author, or mood
Profile customization
Improved responsive design
Deployment to a production hosting platform
👩‍💻 Built By

Maya Brazil, Hafsa Ahmed, and Rumaisa Fatima.

Built for the GDG 24-Hour Hackathon.
