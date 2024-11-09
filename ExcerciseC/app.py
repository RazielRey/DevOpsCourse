from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    result = None  # הגדרת תוצאה כברירת מחדל
    status_code = 'FAILED'  # ברירת מחדל לסטטוס

    if request.method == 'POST':
        url = request.form['url']
        result = {'url': url, 'status_code': 'FAILED'}
        
        try:
            # בדיקה אם ה-URL חי
            response = requests.get(f'http://{url}', timeout=1)
            if response.status_code == 200:
                result['status_code'] = 'OK'
        except requests.exceptions.RequestException:
            result['status_code'] = 'FAILED'

        # הגדרת status_code לפי התוצאה
        status_code = result['status_code']

    # החזרת הטופס עם התוצאה והתראה אם יש צורך
    return render_template('main.html', result=result, status_code=status_code)

app.run(debug=True, host="0.0.0.0", port=8080)
