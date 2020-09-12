from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from mysql import connector

websiteTitle, author, mailid, fbURL, gitURL, instaURL, linkinURL, user_Mail = None, None, None, None, None, None, None, None
with open('details.json', 'r') as fileHandle:
    jsonFile = json.load(fileHandle)
    websiteTitle = jsonFile['siteData']['webTitle']
    author = jsonFile['siteData']['authorName']
    mailid = jsonFile['authorDetails']['mailAddr']
    fbURL = jsonFile['authorDetails']['fbProf']
    gitURL = jsonFile['authorDetails']['gitProf']
    instaURL = jsonFile['authorDetails']['instaProf']
    linkinURL = jsonFile['authorDetails']['linkinProf']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = jsonFile['metadata']['db_uri']
db = SQLAlchemy(app)
app.secret_key = 'super-secret-key'

class Logindata(db.Model):
    __tablename__ = 'logindata'
    mailid = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50), nullable=False)


class Userdata(db.Model):
    __tablename__ = 'userdata'
    entryno = db.Column(db.Integer(), primary_key=True)
    mailid = db.Column(db.String(50), nullable=False)
    itemname = db.Column(db.String(50), nullable=False)
    itemunits = db.Column(db.Integer(), nullable=False)
    itemprice = db.Column(db.Float(), nullable=False)
    date = db.Column(db.String(20), nullable=False)


@app.route('/home')
@app.route('/')
@app.route('/logout')
def home():
    session['user'] = None
    global user_Mail
    user_Mail = None
    return render_template('homePage.html', authorName=author, webTitle=websiteTitle, mailAddr=mailid, gitProf=gitURL, fbProf=fbURL, instaProf=instaURL, linkinProf=linkinURL)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_Mail
    if user_Mail in session and session['user'] == user_Mail:
        return render_template('service.html', authorName=author, webTitle=websiteTitle, mailAddr=mailid, gitProf=gitURL, fbProf=fbURL, instaProf=instaURL, linkinProf=linkinURL)
    elif request.method == 'POST':
        user_Mail = request.form.get('userMail')
        user_Pass = request.form.get('password')
        flag = False
        logins = Logindata.query.all()
        for login in logins:
            if user_Mail == login.mailid and user_Pass == login.password:
                flag = True
                break
        if flag:
            return render_template('service.html', authorName=author, webTitle=websiteTitle, mailAddr=mailid, gitProf=gitURL, fbProf=fbURL, instaProf=instaURL, linkinProf=linkinURL)
        else:
            entry = Logindata(mailid=user_Mail, password=user_Pass)
            db.session.add(entry)
            db.session.commit()
            session['user'] = user_Mail
            return render_template('service.html', authorName=author, webTitle=websiteTitle, mailAddr=mailid, gitProf=gitURL, fbProf=fbURL, instaProf=instaURL, linkinProf=linkinURL)
    else:
        return render_template('login.html', authorName=author, webTitle=websiteTitle, mailAddr=mailid, gitProf=gitURL, fbProf=fbURL, instaProf=instaURL, linkinProf=linkinURL)


@app.route('/freeService')
def freeService():
    return render_template('freeServe.html', authorName=author, webTitle=websiteTitle, mailAddr=mailid, gitProf=gitURL, fbProf=fbURL, instaProf=instaURL, linkinProf=linkinURL)


@app.route('/premiumService', methods=['GET', 'POST'])
def premiumService():
    if request.method == 'GET':
        if user_Mail in session and session['user'] == user_Mail:
            return render_template('service.html', authorName=author, webTitle=websiteTitle, mailAddr=mailid, gitProf=gitURL,
                               fbProf=fbURL, instaProf=instaURL, linkinProf=linkinURL)
        else:
            return render_template('login.html', authorName=author, webTitle=websiteTitle, mailAddr=mailid,
                                   gitProf=gitURL,
                                   fbProf=fbURL, instaProf=instaURL, linkinProf=linkinURL)
    elif request.method == 'POST':
        if user_Mail in session and session['user'] == user_Mail:
            itemName = request.form.get('iname')
            itemUnit = request.form.get('iunits')
            itemPrice = request.form.get('iprice')
            print(itemName)
            entry = Userdata(mailid=user_Mail, itemname=itemName, itemunits=itemUnit, itemprice=itemPrice,
                             date=datetime.now())
            db.session.add(entry)
            db.session.commit()
            session['user'] = user_Mail
            return render_template('service.html', authorName=author, webTitle=websiteTitle, mailAddr=mailid,
                                   gitProf=gitURL, fbProf=fbURL, instaProf=instaURL, linkinProf=linkinURL)
        else:
            itemName = request.form.get('iname')
            itemUnit = request.form.get('iunits')
            itemPrice = request.form.get('iprice')
            entry = Userdata(mailid=user_Mail, itemname=itemName, itemunits=itemUnit, itemprice=itemPrice,
                             date=datetime.now())
            db.session.add(entry)
            db.session.commit()
            session['user'] = user_Mail
            return render_template('service.html', authorName=author, webTitle=websiteTitle, mailAddr=mailid,
                                   gitProf=gitURL, fbProf=fbURL, instaProf=instaURL, linkinProf=linkinURL)
    else:
        pass


@app.route('/menu')
def menu():
    userdata = Userdata.query.filter_by(mailid=user_Mail)
    return render_template('menu.html', authorName=author, webTitle=websiteTitle, mailAddr=mailid,
                           gitProf=gitURL, fbProf=fbURL, instaProf=instaURL, linkinProf=linkinURL, userData=userdata)


app.run(debug=True)