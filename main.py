from distutils.log import Log
from multiprocessing.spawn import import_main_path
from pickle import TRUE
from tkinter import INSERT

from enum import unique
from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import  UserMixin
from sqlalchemy import true
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import  login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import json
#MY db coonection
local_server= True
app = Flask(__name__)
app.secret_key="GPC2222"

#this is for the login
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))
#app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/database_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/gpc'
db=SQLAlchemy(app)
#SQLALCHEMY_TRACK_MODIFICATIONS=override_system_checks

#here we will create db model


#class Users(db.Model):
    #name = db.Column(db.String(100))
    #emails = db.Column(db.String(100), primary_key=True)

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=true)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50))
    password=db.Column(db.String(1000))
    

@app.route("/")
def index():
    return render_template('index.html')
    
    #return render_template('index.html',username=current_user.username)
    

@app.route("/test")
def test():
    #a=User.query.all()
    #print(a)
    try:
        User.query.all()
        return "My db is connected"
    except:
        return "My db is not connected"
    return render_template('index.html')
    
    

@app.route("/GPC")
def gpc():
    return render_template('text.html')

@app.route("/Home")
def home():
    return "<h1>Welcome To GPC Home </h1>"

@app.route("/PAANS")
def paans():
    return render_template('PAANS.html')

@app.route("/baar")
def baar():
    return render_template('baar.html')   

@app.route("/choclates")
def choclates():
    return render_template('choclates.html')    
@app.route("/BEVERAGES")
def beverages():
    return render_template('BEVERAGES.html')
@app.route("/OTHERS")
def others():
    return render_template('OTHERS.html')


@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            #return render_template('PAANS.html')
            return redirect(url_for('index'))
        else:
            print("invalid credentials")
            return render_template('text.html') 
            #return "Invalid Credential"


    return render_template('login.html')

@app.route("/signup",methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            #flash("Email Already Exist","warning")
            return render_template('/login.html')
        encpassword=generate_password_hash(password)

        new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        # newuser=User(username=username,email=email,password=encpassword)
        # db.session.add(newuser)
        # db.session.commit()
        print("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/display")
def display():
    return render_template('index.html')

app.run(debug=True)

#for order taking
#if not User.is_authenticated:
    #return render_template('login.html')
    #else:
        #return render_template('index.html',username=current_user.username)

