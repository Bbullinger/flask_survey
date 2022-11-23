from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "my_password"
debug = DebugToolbarExtension(app)
app.config["SECRET_KEY"] = "my_password"
import surveys

# from flask_debugtoolbar import DebugToolbarExtension

# debug = DebugToolbarExtension(app)
# app.config['SECRET_KEY'] = "my_password"
app.debug = True



@app.route("/", methods=["GET", "POST"])
def home_page():
    session['responses'] = []
    return render_template("base.html", surveys=surveys)


@app.route("/<quiz>/question/<int:number>",methods=["GET","POST"])
def user_question(quiz, number):
    if quiz == "personality_quiz":
        survey = surveys.personality_quiz
    if quiz == "satisfaction_survey":
        survey = surveys.satisfaction_survey


    num_questions = len(survey.questions)

    #logic to prevent user from answering questions post-survey completion
    if len(session["responses"]) == len(survey.questions):
     return redirect("/end_survey")

    # logic to prevent user from answering questions out of order
    if number != len(session["responses"]):
        flash("Please answer questions in order")
        return redirect(f"/{quiz}/question/{len(session['responses'])-1}")

    #Posts answer to session if this is the last question
    

    return render_template(
        "question.html",
        survey=survey,
        num_questions=num_questions,
        number=number,
        responses=session["responses"],
        quiz=quiz
    )


@app.route("/<quiz>/question/<int:number>/answer", methods=["POST"])
def answer(quiz, number):
    if quiz == "personality_quiz":
        survey = surveys.personality_quiz
    if quiz == "satisfaction_survey":
        survey = surveys.satisfaction_survey

    # retrieve user answer from survey form, add the answer to the session["responses"] list
    # number incremented to change page to next question on redirect
    answer = request.form.get(str(number))
    
    responses = session.get('responses')
    responses.append(answer)
    session['responses'] = responses
    number += 1

    # changes page to thank you page once all questions have been answered
    if len(session["responses"]) == len(survey.questions):
        return redirect("/end_survey")
    
    
    
    
    return redirect(f"/{quiz}/question/{number}")


@app.route("/end_survey")
def thanks():
    print(session["responses"])
    return render_template(
        "thanks.html", responses=session["responses"]
    )
