from flask import Flask, make_response, jsonify, request, render_template
import time


app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    time.sleep(7)
    return render_template('main.html')

app.run(debug=True, host="0.0.0.0", port="8080")
