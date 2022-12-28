from flask import Flask, render_template, request, redirect, make_response, send_from_directory, session, jsonify
from datetime import datetime, timezone
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
import bcrypt
from bson.json_util import dumps
import requests
from requests.auth import HTTPBasicAuth
from base64 import b64encode
from http.client import HTTPSConnection


app = Flask(__name__)
app.config['SECRET_KEY'] = '364S1947RO713085892N7LO'
client = MongoClient("mongodb://localhost:27017/")
partansdb = client["partansdb"]
db_users = partansdb["users"]                   #Contiene dati utenti - collegato a post
db_categories = partansdb["categories"]         #Contiene i corsi divisi per anni - collegati a post (post divisi per materia quindi divisi per anno)
db_posts = partansdb["posts"]                   #Contiene i post scritti dagli utenti - appartiene ad una categoria ed è scritto da un utente



#PROVA CANCELLARE



#FINE PROVA

def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


@app.route('/', methods=['GET'])
def index():
    categories = None
    if db_categories.count() > 0:
        categories = db_categories.find()

    return render_template('index.html', categories = categories)
      

@app.route('/profile', methods=['GET'])
def profile():
    if 'username' in session:
        login_user = db_users.find_one({'username': session['cf']})
        return render_template('profile.html',login_user=login_user)
    return redirect('/sign_in')



@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        login_user = db_users.find_one({'username': username})
        if login_user:
            if bcrypt.checkpw(password.encode('utf-8'), login_user['password']):
                session['username'] = login_user["user"]["firstName"].title()
                session['cf'] = username
                session['user_level'] = login_user['user_level']
                return jsonify("Utente trovato, Bentornato!"),200
            else:
                return jsonify("Password sbagliata!"),400
        elif not login_user:
            headers = { 'Authorization' : basic_auth(username, password) }
            while True:
                r = requests.get('https://api.uniparthenope.it/UniparthenopeApp/v1/login', headers=headers)
                if r.status_code == 200:
                    user = r.json()['user']
                    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    db_users.insert_one({'username': username, 'password': hashed_pass, 'user_level': 0, 'user': user})
                    session['username'] = login_user["user"]["firstName"].title()
                    session['user_level'] = login_user['user_level']
                    return jsonify("Utente trovato, Benvenuto!"),200
                else:
                    return jsonify("Credenziali Sbagliate!"),401
    return render_template('sign_in.html')

@app.route('/sign_out', methods=['GET', 'POST'])
def sign_out():
    session.pop('username')
    session.pop('user_level')   
    return redirect('/profile')

@app.route('/create_cat', methods=['POST'])
def create_cat() :
    if request.method == 'POST':
        cat_name = request.form.get('cat_name')
        cat_desc = request.form.get('cat_desc')
        existing_cat = db_categories.find_one({'cat_name': cat_name})
        if not existing_cat:
            db_categories.insert_one({'cat_name': cat_name, 'cat_desc': cat_desc})
            return "success"
        return "Category already exists!"
    return render_template('create_cat.html')



@app.route('/sw.js', methods=['GET'])
def sw():
    response = make_response(send_from_directory('static', 'sw.js'))
    response.headers['Content-Type'] = 'application/javascript'
    return response



@app.route('/view_post/<string:subject>')
def view_post(subject):
    print(subject)
    posts = db_posts.find({'subject': subject })
    logged_in = False
    if 'username' in session:
        logged_in = True
    return render_template('posts.html', logged_in=logged_in, posts=posts)

@app.route('/view_subc/<string:id>')
def view_subc(id):
    print("Id view: ",id)
    subc = db_categories.find_one({"_id": ObjectId(id)})
    subjects = subc['subject']
    return render_template('subject.html', subjects=subjects)

@app.route('/update_subj/<string:id>', methods=['GET','POST'])
def update_subj(id):
    print("Id update:",id)
    if request.method == 'POST':
        print("TEST")
        new_subj = request.form.get('new_subj')
        print(new_subj)
        existing_subj = db_categories.find_one({'subject': new_subj})
        if not existing_subj:
            db_categories.update_one({'_id': ObjectId(id)}, {'$push': {'subject': new_subj}}, upsert = True)
            return "success"
        return "Subject already exists!"
    return render_template('update_subj.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        title = request.form['title']
        query = {}
        if not title:
            query["title"] = {"$regex": title, "$options": 'i'}
        posts = db_posts.find(query).sort("date", -1)
    else:
        posts = db_posts.find().sort("date", -1)
    return render_template('/search.html', posts=posts)




if __name__ == "__main__":
    app.run(debug=True)
