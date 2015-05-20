from flask import Flask, request, render_template
from application import Application

app = Flask(__name__)
app.debug = True
search_app = Application()


@app.route('/', methods=['GET', 'POST'])
def index():
    question = ""
    answers = []
    if request.method == 'GET':
        return render_template('index.html', answers=answers, question=question)

    try:
        question = request.form['question']
    except KeyError as e:
        return str(e)

    answers = search_app.get_answer(question)
    return render_template('index.html', answers=answers, question=question)

if __name__ == '__main__':
    app.run(host='0.0.0.0')