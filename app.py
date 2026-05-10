from flask import Flask, render_template, request, jsonify
from datetime import datetime
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# TEMPORARY DATABASE
quotes = []
likes = []
saved = []
my_posts = []


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

        favourite_mood=favourite_mood
    )


# POST A QUOTE
@app.route("/post-quote", methods=["POST"])
def post_quote():

    data = request.get_json()

    quote = data.get('quote', '').strip()
    book = data.get('book', '').strip()
    author = data.get('author', '').strip()
    mood = data.get('mood', '').strip()

    # make sure fields aren't empty
    if not quote or not book or not author or not mood:

        return jsonify({
            'error': 'Missing required fields'
        }), 400

    new_quote = {

        'id': len(quotes),

        'quote': quote,
        'book': book,
        'author': author,
        'mood': mood,

        'likes': 0,

        'timestamp': datetime.now().strftime("%b %d, %I:%M %p")
    }

    # adds newest quote to top of feed and myshelf
    quotes.insert(0, new_quote)
    my_posts.insert(0, new_quote)

    return jsonify({
        'message': 'Quote posted successfully! 🎉'
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
@app.route("/suggest-mood", methods=["POST"])
def suggest_mood():

    try:
        quote = request.json.get("quote")

        prompt = f"""
        What mood best fits this quote?
        Only answer with ONE word:
        sad, hopeful, romantic, or powerful.

        Quote:
        {quote}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        mood = response.text.strip().lower()

        return jsonify({
            "mood": mood
        })

    except Exception as e:
        print(e)

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