from flask import Flask, render_template, request, jsonify
import main
from multiprocessing import Pool, TimeoutError


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/differentiate', methods=['POST'])
def differentiate():
    input_text = request.form['input_text']
    expand_str = request.form['expand']
    var_of_diff = request.form['var_of_diff']
    print(expand_str)
    if expand_str == 'true':
        expand_bool = True
        expand_str = 'false'
    else:
        expand_bool = False
        expand_str = 'true'
    print(expand_bool)
    print(input_text)

    with Pool(1) as pool:
        result = pool.apply_async(main.differentiate, (input_text, expand_bool, var_of_diff))
        try:
            input_simplified, differentiated, input_simplified_string, differentiated_string, steps_latex, steps_explanation, steps_explanation_latex = result.get(timeout=7)
            return jsonify({"input_simplified": input_simplified, "differentiated": differentiated,
                            "input_simplified_string": input_simplified_string,
                            "differentiated_string": differentiated_string,
                            "expand": expand_str, "steps_latex": steps_latex, "steps_explanation": steps_explanation,
                            "steps_explanation_latex": steps_explanation_latex})
        except TimeoutError:
            return jsonify({"input_simplified": "\\text{Timed out! Please try a less complex input.}", "differentiated": "\\text{Timed out! Please try a less complex input.}",
                             "input_simplified_string": "",
                             "differentiated_string": "",
                             "expand": "", "steps_latex": "", "steps_explanation": "",
                             "steps_explanation_latex": ""})


# @app.route('/simplify', methods=['POST'])
# def simplify():
#     original = request.form['original']
#     differentiated = request.form['differentiated']
#     expand_str = request.form['expand']
#     if expand_str == 'true':
#         expand_str = 'false'
#         expand_bool = False
#     else:
#         expand_str = 'true'
#         expand_bool = True
#     original_simplified_latex, original_simplified_str = main.simplify(original, expand_bool)
#     differentiated_simplified_latex, differentiated_simplified_str = main.simplify(differentiated, expand_bool)
#     return jsonify({"original_simplified_latex": original_simplified_latex,
#                     "differentiated_simplified_latex": differentiated_simplified_latex,
#                     "original_simplified_str": original_simplified_str,
#                     "differentiated_simplified_str": differentiated_simplified_str,
#                     "expand": expand_str})

@app.route('/input_preview', methods=['POST'])
def input_preview():
    input_text = request.form['input_text']
    var_of_diff = request.form['var_of_diff']
    result = main.input_preview(input_text, variable=var_of_diff)
    return jsonify({"preview_result": result})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
    # debug=True for live changes
