from flask import Flask, render_template, request, flash
from werkzeug.exceptions import HTTPException
import os
from dotenv import load_dotenv
import Train as model
import spotify as sp
import PySign as snup

app = Flask(__name__)

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('key')
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Custom error handler for all HTTP errors
@app.errorhandler(HTTPException)
def handle_http_error(error):
    return render_template('error.html', error_description=error.description), error.code

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('login.html')

    mail = request.form.get('email')
    passw = request.form.get('password')

    message = snup.login(mail,passw)
    if 'Retry' in message:
        flash('Incorrect password. Please retry.', 'error')
        return render_template('login.html')
    elif 'exist' in message:
        flash("Account doesn't exist. Please sign up.", 'error')
        return render_template('login.html')
    else:
        return render_template('index.html')



@app.route('/signup', methods=['POST', 'GET'] )
def mainsignup():
    if request.method == 'GET':
        return render_template('signup.html')

    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    password = request.form.get('password')
    signup_flag = snup.signup_func(firstname,lastname,email,password)
    if signup_flag:
        flash('Account created successfully. Please login.', 'success')
        return render_template('login.html')
    else:
        flash('Email already exists. Please login.', 'error')
        return render_template('signup.html')


@app.route('/landing')
def landing():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    musicfile = request.files['music-file']
    filename = musicfile.filename
    musicfile.save(f"uploads/{filename}")

    # processing
    genre = model.predict_genre(f"uploads/{filename}")
    recommend_list = sp.recommend(genre)
    new_genres = snup.new_ones()
    new_recommendations = sp.new_recommend(new_genres)
    snup.update_preferences(genre)
    os.remove(f"uploads/{filename}")
    return render_template('result.html', genre=genre, recommend_list=recommend_list, new_recommendations=new_recommendations)


if __name__ == '__main__':
    app.run()
