from flask import Flask, render_template, request
from main import differentiate


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/differentiate', methods=['POST'])
def differentiate():
    input_text = request.form['input_text']
    result = differentiate(input_text)
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
    # debug=True for live changes
