from flask import Flask, request, url_for,redirect, make_response, jsonify
from .annotate import annotate
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='index.html'))

@app.route('/annotate', methods=['POST'])
def annotate_text():
    if request.method == 'POST':
        data = json.loads(request.data)
        text = data['text']
        out = annotate(text)
        return make_response(jsonify({"annotation": out}), 200)
