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

def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


@app.context_processor
def inject_today_date():
    return {'today_date': datetime.now().strftime("%Y-%m-%d %H:%M")}

@app.route('/', methods=['GET'])
def index():
    categories = None
    if db_categories.estimated_document_count() > 0:
        categories = list(db_categories.find())
        last_post=[]
        for category in categories:
                print(category["_id"])
                subc = db_categories.find_one({"_id": ObjectId(category["_id"])})
                subjects = subc['subject']
                i = 0
                max = None
                for subject in subjects:
                        temp = db_posts.find_one({'subject': subject}, sort=[('date',-1)])
                        if temp:
                            if i==0:
                                max = temp
                                i=1
                            elif temp["date"] > max["date"]:
                                max = temp 
                last_post.append(max)     
        return render_template('index.html', categories = categories, last_post=last_post)  
    else:
        return render_template('index.html', categories=None)
      

@app.route('/profile', methods=['GET'])
def profile():
    if 'username' in session:
        login_user = db_users.find_one({'username': session['cf']})
        return render_template('profile.html',login_user=login_user)
    return redirect('/sign_in')

@app.route('/show_profile/<string:id>')
def show_profile(id):
    user = db_users.find_one({"_id":ObjectId(id)})
    return render_template("profile.html", login_user=user)


@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        headers = { 'Authorization' : basic_auth(username, password) }
        login_user = db_users.find_one({'username': username})
        if login_user:
            if bcrypt.checkpw(password.encode('utf-8'), login_user['password']):
                session['username'] = login_user["user"]["firstName"].title() + " " + login_user["user"]["lastName"].title()
                session['cf'] = username
                session['user_level'] = login_user['user_level']
                session['_id'] = str(login_user["_id"])
                r = requests.get("https://api.uniparthenope.it/UniparthenopeApp/v2/students/myExams/"+str(login_user["user"]["trattiCarriera"][-1]["matId"]), headers=headers )                    
                db_users.update_one({"_id": login_user["_id"]}, {"$set": {"esami": r.json()}} )
                return jsonify("Utente trovato, Bentornato!"),200
            else:
                return jsonify("Password sbagliata!"),400
        elif not login_user:
            while True:
                r = requests.get('https://api.uniparthenope.it/UniparthenopeApp/v1/login', headers=headers)
                if r.status_code == 200:
                    user = r.json()['user']
                    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    db_users.insert_one({'username': username, 'password': hashed_pass, 'user_level': 0, 'user': user})
                    session['username'] = login_user["user"]["firstName"].title() + " " + login_user["user"]["lastName"].title()
                    session['user_level'] = login_user['user_level']
                    r = requests.get("https://api.uniparthenope.it/UniparthenopeApp/v1/students/exams/"+str(login_user["user"]["trattiCarriera"][-1]["stuId"])+"/5",headers=headers)
                    db_users.update_one({"_id": login_user["_id"]}, {"$set": {"esami": r.json()}} )
                    return jsonify("Utente trovato, Benvenuto!"),200
                else:
                    return jsonify("Credenziali Sbagliate!"),401
    return render_template('sign_in.html')

@app.route('/sign_out', methods=['GET', 'POST'])
def sign_out():
    session.pop('username')
    session.pop('user_level')   
    session.pop('_id')
    return redirect('/profile')

@app.route('/create_cat', methods=['POST'])
def create_cat() :
    if request.method == 'POST':
        cat_name = request.form.get('cat_name')
        cat_desc = request.form.get('cat_desc')
        existing_cat = db_categories.find_one({'cat_name': cat_name})
        if not existing_cat:
            db_categories.insert_one({'cat_name': cat_name, 'cat_desc': cat_desc,'subject': ["None"]})
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
    code = request.args.get('code')
    print(code)
    posts = list(db_posts.find({'subject': subject }))
    logged_in = False
    if 'username' in session:
        logged_in = True
    return render_template('posts.html', logged_in=logged_in, posts=posts, subject=subject, code=code)

@app.route('/view_subc/<string:id>')
def view_subc(id):
    print("Id view: ",id)
    subc = db_categories.find_one({"_id": ObjectId(id)})
    if subc['subject'][0] != None:
        subjects = subc['subject']
        code = subc['code']
        last_post=[]
        for subject in subjects:
            last_post.append(db_posts.find_one({'subject': subject}, sort=[('date',-1)]))
    else:
        subjects = None
        last_post = None

    return render_template('subject.html', subjects=subjects, last_post=last_post , code=code)

@app.route('/update_subj/<string:id>', methods=['GET','POST'])
def update_subj(id):
    if request.method == 'POST':
        new_subj = request.form.get('new_subj')
        new_subj_code = request.form.get('new_subj_code')
        existing_subj = db_categories.find_one({'subject': new_subj})
        if not existing_subj:
            test = db_categories.find_one({'_id': ObjectId(id)})
            if test["subject"] == ["None"]:
                db_categories.update({"_id": ObjectId(id)},{ "$set": { "subject.0" : new_subj } })
            else:    
                db_categories.update_one({'_id': ObjectId(id)}, {'$push': {'subject': new_subj,'code': new_subj_code}}, upsert = True)
            return "success"
        return "Subject already exists!"
    return render_template('update_subj.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search = request.form['search']
        select = request.form.get('id_search')
        print("Search: ", search)
        print("Select: ", select)

        if not search:
            return render_template('index.html')
        if  select == "topics":
            posts = list(db_posts.find({'title': {"$regex":search, "$options": "si" }}).sort("date", -1))
            print(posts)
            return render_template('search.html', posts=posts)
        else:
            
            posts = list(db_posts.find({'author': {"$regex":search, "$options": "si"  }}).sort("date", -1))
            print(posts)
            return render_template('search.html', posts=posts)
    return render_template('index.html')
    
    

@app.route('/create_posts/<string:subject>', methods=['GET','POST'])
def create_posts(subject):
    code = request.args.get('code')
    print("Id create_post", subject, code)
    if request.method == 'POST':
        esame_superato = False
        print("TEST")
        post_title = request.form.get('post_title')
        if not post_title:
            return "Title cannot be blank"    
        post_content = request.form.get('post_content')
        if not post_content:
            return "Content cannot be blank"
        login_user = db_users.find_one({'_id': ObjectId(session["_id"])})
        if login_user:
            esami = db_users.find_one({'_id': ObjectId(session["_id"])})
            for esame in esami["esami"]:
                print(code, esame["adsceID"], esame["status"]["esito"])
                if str(esame["adsceID"]) == str(code):
                    print("sono uguali")
                    if esame["status"]["esito"]=="S":
                        print("esame superato")
                        esame_superato = True
                        break
            
            if esame_superato:
                print("Esame Superato")
                db_posts.insert_one({'title': post_title, 'content': post_content,'authorId': session['_id'] ,'author': session['username'],'subject': subject,'adsceId':code, 'date': datetime.now().strftime("%Y-%m-%d %H:%M"), 'esame_superato': 1})
            else:
                db_posts.insert_one({'title': post_title, 'content': post_content,'authorId': session['_id'] ,'author': session['username'],'subject': subject,'adsceId':code, 'date': datetime.now().strftime("%Y-%m-%d %H:%M"), 'esame_superato': 0})
        return "success"
    return render_template('create_posts.html') 

@app.route('/comments/<string:id>', methods=['GET','POST'])
def comments(id):
    print("Id comments", id)
    post = db_posts.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        print("TEST")
        comments_content = request.form.get('comments_content')
        if not comments_content:
            return "comment cannot be blank"    
        db_posts.update_one({ '_id': ObjectId(id) }, { '$push': { 'replies': { 'author' : session['username'],'content' : comments_content, 'date' :  datetime.now().strftime("%Y-%m-%d %H:%M") } } } )
        return "success"
    return render_template('comments.html', post=post) 

@app.route('/developers', methods=['GET', 'POST'])
def developers():
    return render_template('developers.html')

@app.route('/link', methods=['GET', 'POST'])
def link():
    return render_template('link.html')

if __name__ == "__main__":
    app.run(debug=True)
