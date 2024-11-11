import logging
from logs import logger
from flask import Flask, request, render_template
import requests
import re

app = Flask(__name__)

email_pattern = r'^[\w\.-]+@[a-zA-Z\d-]+\.[a-zA-Z]{2,}$'

@app.route('/', methods=['GET', 'POST'])
def main ():
    logger.debug('main() called')
    alert= None
    email = request.form.get('email', None)
    
    if email is None or not re.match(email_pattern, email):
        logger.error('Invalid email')
        alert = 'Invalid email'
    else:
        logger.debug(f'Email: {email}')
        alert = 'Thank you for your feedback!'
        logger.debug(f'Writing email to file: {email}')
        with open('email.txt', 'a') as f:
            f.write(f'{email}\n')
      
    return render_template('main.html', alert=alert)  




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)