from flask import Flask
import render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import os
import pandas as pd 
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from wtforms.fields import EmailField
#import facebook
import joblib

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Config MySQL
mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testing_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize the app for use with this MySQL class
mysql.init_app(app)


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, *kwargs)
        else:
            flash('Unauthorized, Please logged in', 'danger')
            return redirect(url_for('login'))
    return wrap


def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            flash('Unauthorized, You logged in', 'danger')
            return redirect(url_for('index'))
        else:
            return f(*args, *kwargs)
    return wrap


@app.route('/')
def index():
    return render_template('home.html')


class LoginForm(Form):    # Create Message Form
    username = StringField('Username', [validators.length(min=1)], render_kw={'autofocus': True})


# User Login
@app.route('/login', methods=['GET', 'POST'])
@not_logged_in
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # GEt user form
        username = form.username.data
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username=%s", [username])

        if result > 0:
            # Get stored value
            data = cur.fetchone()
            password = data['password']
            uid = data['id']
            name = data['name']

            # Compare password
            if sha256_crypt.verify(password_candidate, password):
                # passed
                session['logged_in'] = True
                session['uid'] = uid
                session['s_name'] = name
                x = '1'
                cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
                flash('You are now logged in', 'success')

                return redirect(url_for('index'))

            else:
                flash('Incorrect password', 'danger')
                return render_template('login.html', form=form)

        else:
            flash('Username not found', 'danger')
            # Close connection
            cur.close()
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/out')
def logout():
    if 'uid' in session:

        # Create cursor
        cur = mysql.connection.cursor()
        uid = session['uid']
        x = '0'
        cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
        session.clear()
        flash('You are logged out', 'success')
        return redirect(url_for('index'))
    return redirect(url_for('login'))


class RegisterForm(Form):
    name = StringField('Name', [validators.length(min=3, max=200)], render_kw={'autofocus': True})
    username = StringField('Username', [validators.length(min=3, max=200)])
    email = EmailField('Email', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=200)])
    password = PasswordField('Password', [validators.length(min=3)])


@app.route('/register', methods=['GET', 'POST'])
@not_logged_in
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create Cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
                    (name, email, username, password))

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('You are now registered and can login', 'success')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)

token='EAAJBlNIzKkQBAEtE2Y6zHcvrQFzyc8bhKuBCQapSwj2XWr2I1gFshZARZAjpDhUg791TDbZA0wAo8TB2yk3mfiZB5YqhsiphAILu5i1vfpCsAx4JWuGMkZA8ZAzW2VJwRUMiRDcYdJBMWWBI1TPdIBsRNTWfft1QE56YZB2DFGlBVbkh6G6VRBBYoqdSL1o7uLVefe5NZCXQvwZDZD'
@app.route('/text')
def home():
	return render_template('homesus.html')


@app.route('/predict',methods=['POST'])
def predict():
    message=request.form['message']
    df=pd.read_csv("dataset_SE_Bangla.csv")
    X=df["Text"]
    cv=TfidfVectorizer()
    X=cv.fit_transform(X)
    infile = open('suspicious_model','rb')
    model = joblib.load(infile)
    data=[message]
    vecct=cv.transform(data).toarray()
    _prediction = int(model.predict(vecct))
    if _prediction ==0:
        message="✅"+message
    else:
        message="❌"+message
    page_access_token = token
    graph = facebook.GraphAPI(page_access_token)
    facebook_page_id = '101432762410121'
    graph.put_object(facebook_page_id, "feed", message=message)
    return render_template('homesus.html',message=message,prediction=_prediction)

def get_text_of_post():
    try:
        graph=facebook.GraphAPI(access_token=token,version=3.1)
        posts=graph.request('101432762410121/posts')['data']
        d={}
        i=0
        for dic in posts:
            newlist=[]
            newlist.append(dic['message'])
            newlist.append(dic['id'])
            d[i]=newlist
            i=i+1
        return d
    except Exception as e:
        return 0

@app.route('/dashboard',methods=['GET','POST'])
def post_table():
    # newlist=['আমাদের তথাকথিত জাগ্রত ভাইদের মধ্যে পোস্ট পড়ে তারা যা দেখছে তা না দেখা পর্যন্ত ইহুদিরা আমাদের কতটা বোকা মনে করে তাতে আমি অপমানিত','পশ্চিমা সভ্যতার ইহুদিবাদী-ইঞ্জিনিয়ার্ড ইচ্ছাকৃত ধ্বংসের উপর একটি রঙিন চিত্রিত একশো বত্রিশ পৃষ্ঠার ই-বুক বিনামূল্যে ডাউনলোডের জন্য নীচে ক্লিক করুন','বর্তমান সময়ে টিকে থাকা প্রচুর কঠিন','আমি এই পেজটি খুলেছি কিছু নতুন করে শিক্ষার আশায়']
    newlist={}
    newlist=get_text_of_post()
    if newlist==0:
        print("check the facebook access")
    else:
        df=pd.read_csv("dataset_SE_Bangla.csv")
        X=df["Text"]
        cv=TfidfVectorizer()
        X=cv.fit_transform(X)
        #predict_from_file with joblib
        #joblib.dump(clf, 'suspicious_model')
        d={}
        infile = open('suspicious_model','rb')
        model = joblib.load(infile)
        for i in range(0,len(newlist)):
            li=[]
            data=[newlist[i][0]]
            li.append(newlist[i][0])
            li.append(newlist[i][1])
            vecct=cv.transform(data).toarray()
            
            _prediction = int(model.predict(vecct))
            li.append(_prediction)
            d[i]=li
    return render_template('post_list.php',newlist=d)

if __name__ == '__main__':
    app.run(debug=True)


