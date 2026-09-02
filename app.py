import firebase_admin
from firebase_admin import credentials, auth
from flask import session
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")

cred = credentials.Certificate(
    "bookquotes-app-861fa-firebase-adminsdk-fbsvc-776560ef3e.json"
)

firebase_admin.initialize_app(cred)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# TEMPORARY DATABASE
quotes = []
likes = []
saved = []
my_posts = []
current_user = "gdg.reads"

#LOGIN
@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()
    id_token = data.get('token')

    try:
        decoded_token = auth.verify_id_token(id_token)

        session['user'] = {
            'uid': decoded_token['uid'],
            'email': decoded_token.get('email')
        }

        return jsonify({
            'success': True
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 401
    
#LOGOUT
@app.route('/logout', methods=['POST'])
def logout():

    session.pop('user', None)

    return jsonify({
        'success': True
    })

# HOME PAGE
@app.route("/")
@app.route("/home")
def home():
    return render_template("postquote.html")


# EXPLORE PAGE
@app.route("/explore")
def explore():
    return render_template("feed.html", quotes=quotes)


# MY SHELF PAGE
@app.route('/myshelf')
def myshelf():

    # count moods from posted quotes
    mood_count = {}

    for q in my_posts:

        mood = q['mood']

        if mood in mood_count:
            mood_count[mood] += 1
        else:
            mood_count[mood] = 1

    # find most common mood
    favourite_mood = "None"

    if mood_count:
        favourite_mood = max(
            mood_count,
            key=mood_count.get
        )

    return render_template(

        'myshelf.html',

        saved=saved,

        my_posts=my_posts,

        posted_count=len(my_posts),

        saved_count=len(saved),

        favourite_mood=favourite_mood,

        current_user=current_user
    )


# POST A QUOTE
@app.route('/postquote', methods=['POST'])
def post_quote():

    # must be logged in
    if 'user' not in session:

        return jsonify({
            'success': False,
            'error': 'Unauthorized'
        }), 401

    data = request.get_json()

    current_user = session['user']['email']

    new_quote = {

        'id': len(quotes) + 1,

        'quote': data['quote'],

        'book': data['book'],

        'author': data['author'],

        'mood': data['mood'],

        'username': current_user,

        'likes': 0,

        'timestamp': datetime.now().strftime('%B %d, %Y')
    }

    # add to explore page
    quotes.append(new_quote)

    # add to user's shelf/profile
    my_posts.append(new_quote)

    return jsonify({
        'success': True,
        'quote': new_quote
    })


# LIKE QUOTE
@app.route("/like", methods=["POST"])
def like_quote():

    quote_id = request.json.get('id')

    for q in quotes:

        if q['id'] == quote_id:

            q['likes'] += 1

            return jsonify({
                'likes': q['likes']
            })

    return jsonify({
        'error': 'Quote not found'
    }), 404


# SAVE QUOTE
@app.route("/save", methods=["POST"])
def save_quote():

    quote_id = request.json.get('id')

    for q in quotes:

        if q['id'] == quote_id:

            # prevents duplicate saves
            already_saved = any(
                saved_q['id'] == quote_id
                for saved_q in saved
            )

            if not already_saved:
                saved.append(q)

            return jsonify({
                'message': 'Quote saved successfully'
            })

    return jsonify({
        'error': 'Quote not found'
    }), 404


# AI MOOD SUGGESTION
# AI MOOD SUGGESTION
@app.route("/suggest-mood", methods=["POST"])
def suggest_mood():

    try:

        data = request.get_json()

        quote = data.get("quote")

        prompt = f"""
Classify the emotional mood of this quote.

ONLY reply with ONE word from this list:
sad
hopeful
romantic
powerful

Quote:
{quote}
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=prompt
        )

        mood = response.text.strip().lower()

        if "sad" in mood:
            mood = "sad"

        elif "romantic" in mood:
            mood = "romantic"

        elif "powerful" in mood:
            mood = "powerful"

        else:
            mood = "hopeful"

        return jsonify({
            "mood": mood
        })

    except Exception as e:

        print("GEMINI ERROR:", e)

        return jsonify({
            "mood": "hopeful"
        })

# DELETE QUOTE
@app.route('/delete', methods=['POST'])
def delete_quote():

    quote_id = request.json.get('id')

    global quotes
    global my_posts
    global saved

    # remove from explore feed
    quotes = [
        q for q in quotes
        if q['id'] != quote_id
    ]

    # remove from user's posts
    my_posts = [
        q for q in my_posts
        if q['id'] != quote_id
    ]

    # remove from saved too
    saved = [
        q for q in saved
        if q['id'] != quote_id
    ]

    return jsonify({
        'message': 'Quote deleted'
    })


# 404 PAGE
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# RUN APP
if __name__ == "__main__":
    app.run(debug=True)