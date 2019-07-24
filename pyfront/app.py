from flask import Flask, escape, request, url_for, render_template
# from dotenv import  load_dotenv
# load_dotenv()

app = Flask(__name__)

#url_for('static', filename="static")


@app.route('/')
def index():
    return render_template('index.html')
