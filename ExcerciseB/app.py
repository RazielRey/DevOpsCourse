from flask import Flask, make_response, jsonify, request, render_template
import time
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main ():
    if request.method == 'POST':
        url = request.form['url']
        result = {'url': url, 'status_code': 'FAILED'}
        try:
            response = requests.get(f'http://{url}', timeout=1)
            if response.status_code == 200:
                result['status_code'] = 'OK'
        except requests.exceptions.RequestException:
            result['status_code'] = 'FAILED'
    
    return render_template('main.html', result=result, status_code=result['status_code'])


app.run(debug=True, host="0.0.0.0", port="8080")