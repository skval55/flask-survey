from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


responses = []

survey = surveys.satisfaction_survey

@app.route('/')
def homepage():
    """home page to start survey"""
    if len(responses) == len(survey.questions):
        return redirect(f'/question/{len(responses) + 1}') 

    # responses.clear() 
    return render_template("home.html", msg=survey.instructions)


@app.route("/answer", methods=["POST"])
def to_next_question():
    """appends users choice to response list"""
    choice = request.form['question']

    responses.append(choice)
    return redirect(f'/question/{len(responses) + 1}') 


@app.route('/question/<question_num>')
def question(question_num):
    """takes you to the correct question user is on"""
    if int(question_num) -1 != len(responses):
        flash("hey dummy dumb stop trying to play with the url!")
        return redirect(f'/question/{len(responses) + 1}') 
    if len(survey.questions) < int(question_num):

        return render_template('thank_you.html', msg=responses)
    question = survey.questions[len(responses)]
    return render_template('question0.html', msg=question.question, choices=question.choices)

    