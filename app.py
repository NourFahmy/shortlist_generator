from flask import Flask, request, render_template
from model.generate import *
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    topic = getRelevantTopics(text)
    #processed_text = text.lower()
    return generate_shortlist(topic.lower())


app.run(host='0.0.0.0', port=5005)