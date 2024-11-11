from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    response = None
    if request.method == 'POST':
        text= request.form.get('text','').strip()
        if text:
            count = len(text.split())
            response = (f"Word count: {count}")
        else:
            response = "No text provided"
    return render_template('main.html', response=response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
    