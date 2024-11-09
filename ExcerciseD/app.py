from flask import Flask, request, render_template
import requests


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    original_deg = request.form.get('original_deg', None)
    if original_deg is None or original_deg.strip() == "":
        return render_template('main.html', alert="Please enter a valid temperature.")
    converted_deg = (float(original_deg) * 9/5) + 32
    return render_template('main.html', original_deg=original_deg, converted_deg=converted_deg)
 

app.run(debug=True, host="0.0.0.0", port=8080)

