from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('postquote.html')

@app.route('/home')
def home_feed():
    return render_template('postquote.html')

@app.route('/explore')
def explore():
    return render_template('feed.html')

@app.route('/myshelf')
def myshelf():
    return render_template('myshelf.html')

if __name__ == '__main__':
    app.run(debug=True)