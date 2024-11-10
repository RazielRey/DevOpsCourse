from flask import Flask, request, render_template
import requests


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main ():
    number1 = request.form.get('num1', None)
    number2 = request.form.get('num2', None)
    operation = request.form.get('operation', None)
    try:
        if operation == 'add':
            result = (int(number1) + int(number2))
        elif operation == 'subtract':
            result = (int(number1) - int(number2))
        elif operation == 'multiply':
            result = (int(number1) * int(number2))
        elif operation == 'divide':
            if number2 == 0:
                result = "We can't divide by zero"
            result = (int(number1) / int(number2))
        else:
            result = "invalid operation"
    except Exception as e:
        result = ("Error: " + str(e))


    return render_template('main.html', result=result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
