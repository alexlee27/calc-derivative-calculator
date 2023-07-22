from flask import Flask, render_template, request, jsonify
import main


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/differentiate', methods=['POST'])
def differentiate():
    input_text = request.form['input_text']
    expand_str = request.form['expand']
    print(expand_str)
    if expand_str == 'true':
        expand_bool = True
    else:
        expand_bool = False
    print(expand_bool)
    print(input_text)
    input_simplified, differentiated = main.differentiate(input_text, expand=expand_bool)
    return jsonify({"input_simplified": input_simplified, "differentiated_result": differentiated})

@app.route('/input_preview', methods=['POST'])
def input_preview():
    input_text = request.form['input_text']
    result = main.input_preview(input_text)
    return jsonify({"preview_result": result})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
    # debug=True for live changes
