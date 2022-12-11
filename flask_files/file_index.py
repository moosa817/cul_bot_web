from flask import Blueprint,render_template,redirect,request,session,flash
from werkzeug.utils import secure_filename
import os
import config
import requests
import mysql.connector
from flask import current_app


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','webp','tiff'])



index_page = Blueprint('index_page', __name__, template_folder='templates')
@index_page.route('/',methods=['GET','POST'])
def index():
    os.chdir('/tmp')
    print(os.listdir())
    # await send_msg("pinged")
    if request.method == "POST":
        if request.form.get("name"):
            username = request.form["name"]
            pwd = request.form["pwd"]

            def login(username, password):
                session["username"] = username
                session["password"] = password
                name = []
                img = []
                conn = mysql.connector.connect(
                    host=config.db_host,
                    user=config.db_user,
                    passwd=config.db_pwd,
                    database=config.db_database)
                cur = conn.cursor()   
                cur.execute("SELECT name,img FROM `img_stuff`")
               
                result = cur.fetchall()
                conn.close()
                for i in range(len(result)):
                    name.append(result[i][0])
                    img.append(result[i][1])

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
            conn = mysql.connector.connect(
                host=config.db_host,
                user=config.db_user,
                passwd=config.db_pwd,
                database=config.db_database)
            cur = conn.cursor()  


            sql = "SELECT name,img FROM `img_stuff` WHERE name = '%s'"
            val = (key)
            cur.execute(sql % val)
           


            result = cur.fetchall()
            conn.close()
            
            if result:
                return render_template("index.html",login=True,name=session["names"],imgs=session["imgs"],stuff_error="Already exists")

            elif len(key) >50:
                return render_template("index.html",login=True,name=session["names"],imgs=session["imgs"],stuff_error="Too Long")
            else:
                conn = mysql.connector.connect(
                    host=config.db_host,
                    user=config.db_user,
                    passwd=config.db_pwd,
                    database=config.db_database)
                cur = conn.cursor()  
                sql = "INSERT INTO `img_stuff` (name,img) VALUES ('%s' ,'%s')"
                val = (key,"")
                cur.execute(sql % val)
                conn.commit()
                conn.close()
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
                conn = mysql.connector.connect(
                    host=config.db_host,
                    user=config.db_user,
                    passwd=config.db_pwd,
                    database=config.db_database)
                cur = conn.cursor()  
                index = session["names"].index(name)
                session["imgs"][index].append(img_url)
                s = session["imgs"][index]
                a = ",".join(s)
                sql = "UPDATE img_stuff SET img = '%s' WHERE name= '%s'"
                val = (a, name)
                cur.execute(sql % val)
                conn.commit()
                conn.close()


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
                conn = mysql.connector.connect(
                host=config.db_host,
                user=config.db_user,
                passwd=config.db_pwd,
                database=config.db_database)
                cur = conn.cursor()  
                index = session["names"].index(name)
                session["imgs"][index].append(filename)
                s = session["imgs"][index]
                a = ",".join(s)

                sql = "UPDATE img_stuff SET img = '%s' WHERE name= '%s'"
                val = (filename, name)
                cur.execute(sql % val)
                conn.commit()
                conn.close()


                return render_template("index.html",login=True,name=session["names"],imgs=session["imgs"])
    
    
    if session.get('username'):
        name = []
        img = []
        conn = mysql.connector.connect(
        host=config.db_host,
        user=config.db_user,
        passwd=config.db_pwd,
        database=config.db_database)
        cur = conn.cursor()   
        cur.execute("SELECT name,img FROM `img_stuff`")
        result = cur.fetchall()
        conn.close()
        for i in range(len(result)):
            name.append(result[i][0])
            img.append(result[i][1])

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


