from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)
app.config['SECRET_KEY'] = "my_password"
debug = DebugToolbarExtension(app)
app.config['SECRET_KEY'] = "my_password"
import surveys

# from flask_debugtoolbar import DebugToolbarExtension

# debug = DebugToolbarExtension(app)
# app.config['SECRET_KEY'] = "my_password"
app.debug = True

responses = []

#hard coded survey, for now
satisfaction_survey = surveys.satisfaction_survey

@app.route('/')
def home_page():
    return render_template("base.html")

@app.route('/question/<int:number>')
def user_question(number):
    num_questions = len(satisfaction_survey.questions)
    survey = satisfaction_survey

    #logic to prevent user from answering questions out of order
    if (number != len(responses)):
        flash("Please answer questions in order")
        return redirect(f'/question/{len(responses)}')
    
    #changes page to thank you page once all questions have been answered
    if (len(responses) == num_questions):
        return redirect("/end_survey")
    return render_template("question.html", survey=survey,num_questions=num_questions,number=number,responses=responses)



@app.route('/question/<int:number>/answer',methods=['POST'])
def answer(number):

#retrieve user answer from survey form, add the answer to the responses list
#number incremented to change page to next question on redirect
    answer = request.form.get(str(number))
    number += 1
    responses.append(answer)
    print(responses)
    return redirect(f'/question/{number}')

@app.route('/end_survey')
def thanks():
    return render_template("thanks.html",responses=responses,survey=satisfaction_survey)