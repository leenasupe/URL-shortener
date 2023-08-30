from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import string
import random
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)
class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500))
    short_url = db.Column(db.String(10), unique=True)

    def __init__(self, original_url, short_url):
        self.original_url = original_url
        self.short_url = short_url

db.create_all()
def shorten_url():
    characters = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(random.choices(characters, k=6))
        url = Url.query.filter_by(short_url=short_url).first()
        if not url:
            return short_url

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']
        short_url = shorten_url()
        new_url = Url(original_url=original_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()
        return redirect('/')
    else:
        urls = Url.query.all()
        return render_template('index.html', urls=urls)

@app.route('/<string:short_url>')
def redirect_to_url(short_url):
    url = Url.query.filter_by(short_url=short_url).first()
    if url:
        return redirect(url.original_url)
    else:
        return 'Invalid URL'
