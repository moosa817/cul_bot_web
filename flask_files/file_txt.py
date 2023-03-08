from flask import Blueprint,render_template,redirect,request,session,redirect,url_for
import config
from pymongo import MongoClient

txt_page = Blueprint('txt_page', __name__, template_folder='templates')



@txt_page.route("/text",methods=["GET","POST"])
def text():
    if request.form.get("key"):
            key = request.form["key"]
            client = MongoClient(config.mongo_str)
            db = client.get_database('cul_bot')
            records = db.text_stuff
            result = records.find_one({"name":key})    

            if result:
                return render_template("index.html",login=True,name=session["names"],imgs=session["imgs"],stuff_error="Already exists")

            elif len(key) >50:
                return render_template("index.html",login=True,name=session["names"],imgs=session["imgs"],stuff_error="Too Long")
            else:
                client = MongoClient(config.mongo_str)
                db = client.get_database('cul_bot')
                records = db.text_stuff
                
                records.insert_one({"name":key,"text":""})

                session["txt_name"].append(key)
                session["txt_text"].append("")
                return render_template("text.html",login=True,name=session["txt_name"] ,txt=session["txt_text"])

    if session.get("username"):
        client = MongoClient(config.mongo_str)
        db = client.get_database('cul_bot')
        records = db.text_stuff

        result = records.find({})        
        txt_name = []
        txt = []
        for i in result:        
            txt_name.append(i.get("name"))
            txt.append(i.get("text"))

        # print(txt_name,txt)
        session["txt_name"] = txt_name
        session["txt_text"] = txt


        return render_template("text.html",login=True,name=session["txt_name"] ,txt=session["txt_text"])
    else:
        return redirect(url_for("index"))