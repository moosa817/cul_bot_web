from flask import Blueprint,render_template,redirect,request,session,flash
from werkzeug.utils import secure_filename
import os
import config
import requests
from flask import current_app
from pymongo import MongoClient


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','webp','tiff'])



index_page = Blueprint('index_page', __name__, template_folder='templates')
@index_page.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        if request.form.get("name"):
            username = request.form["name"]
            pwd = request.form["pwd"]

            def login(username, password):
                session["username"] = username
                session["password"] = password
                name = []
                img = []
                
                client = MongoClient(config.mongo_str)
                db = client.get_database('cul_bot')
                records = db.img_stuff


                result = records.find({})
               
                for i in result:
                    name.append(i.get("name"))
                    img.append(i.get("img"))

                imgs = []
                for f in img:
                    if f is not None:
                        imgs.append(f.split(","))

                session["names"] = name
                session["imgs"] = imgs
                return render_template("index.html",login=True,name=name,imgs=imgs)


            if username == config.user and pwd==config.pwd:
                return login(username,pwd)
            else:
                # print("render 1")
                return render_template("index.html",stuff="error")

        elif request.form.get("key"):
            key = request.form["key"]
            client = MongoClient(config.mongo_str)
            db = client.get_database('cul_bot')
            records = db.img_stuff

            result = records.find_one({"name":key})
           
            
            if result:
                return render_template("index.html",login=True,name=session["names"],imgs=session["imgs"],stuff_error="Already exists")

            elif len(key) >50:
                return render_template("index.html",login=True,name=session["names"],imgs=session["imgs"],stuff_error="Too Long")
            else:

                records.insert_one({"name":key,"img":""})  
                
                session["names"].append(key)

                return render_template("index.html",login=True,name=session["names"],imgs=session["imgs"])

        elif request.form.get("thumbnail"):
            img_url = request.form["thumbnail"]
            name = request.form["name-url"]
            def is_url_image(image_url):
                try:
                    image_formats = ("image/png", "image/jpeg", "image/jpg","image/gif","image/webp","image/tiff","image/vnd.microsoft.icon","image/x-icon","image/vnd.djvu","image/svg+xml")
                    r = requests.head(image_url)
                    # print(r.headers["content-type"])
                    if r.headers["content-type"] in image_formats:
                        return True
                    return False
                except:
                    return False

            # print(is_url_image(img_url))
            if is_url_image(img_url) and name:
                # print("here")

                client = MongoClient(config.mongo_str)
                db = client.get_database('cul_bot')
                records = db.img_stuff
                
                index = session["names"].index(name)
                session["imgs"][index].append(img_url)
                s = session["imgs"][index]
                a = ",".join(s)

                records.update_one({"name":name},{"$set":{"img":a}})

                return render_template("index.html",login=True,name=session["names"],imgs=session["imgs"])

                
            else:
                # print("not here")
                return render_template("index.html",login=True,name=session["names"],imgs=session["imgs"])


        elif 'file' in request.files:
            # print("here")
            def allowed_file(filename):     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


            file = request.files['file']
            name = request.form["name-upload"]
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                # print("here")
                
                

                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))   
                
                filename = "static/imgs/" + filename

                client = MongoClient(config.mongo_str)
                db = client.get_database('cul_bot')
                records = db.img_stuff

            

                index = session["names"].index(name)
                

                session["imgs"].append([])


                session["imgs"][index].append(filename)
                s = session["imgs"][index]
                a = ",".join(s)


                sql = "UPDATE img_stuff SET img = '%s' WHERE name= '%s'"
                records.update_one({"name":name},{"$set":{"img":filename}})

                return render_template("index.html",login=True,name=session["names"],imgs=session["imgs"])
    
    
    if session.get('username'):
        name = []
        img = []

        client = MongoClient(config.mongo_str)
        db = client.get_database('cul_bot')
        records = db.img_stuff
        
        result = records.find({})


        for i in result:
            name.append(i.get("name"))
            img.append(i.get("img"))

        imgs = []

        for f in img:
            if f is not None:
                imgs.append(f.split(","))

        session["names"] = name
        session["imgs"] = imgs

        return render_template("index.html",login=True,name=name,imgs=imgs)
    else:
        # print("render 2")
        return render_template("index.html",login=False)


