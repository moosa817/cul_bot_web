from flask import Blueprint,render_template,redirect,request,session,redirect,url_for
from werkzeug.utils import secure_filename
import os
import config
import requests
import mysql.connector
from flask import current_app

txt_page = Blueprint('txt_page', __name__, template_folder='templates')

@txt_page.route("/text",methods=["GET","POST"])
def text():
    if request.form.get("key"):
            key = request.form["key"]
            conn = mysql.connector.connect(
                host=config.db_host,
                user=config.db_user,
                passwd=config.db_pwd,
                database=config.db_database)
            cur = conn.cursor()  


            sql = "SELECT name,text FROM `text_stuff` WHERE name = '%s'"
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
                sql = "INSERT INTO `text_stuff` (name,text) VALUES ('%s' ,'%s')"
                val = (key,"")
                cur.execute(sql % val)
                conn.commit()
                conn.close()
                session["txt_name"].append(key)
                return render_template("text.html",login=True,name=session["txt_name"] ,txt=session["txt_text"])

    if session.get("username"):
        conn = mysql.connector.connect(
                    host=config.db_host,
                    user=config.db_user,
                    passwd=config.db_pwd,
                    database=config.db_database)
        cur = conn.cursor()   
        cur.execute("SELECT name,text FROM `text_stuff`")
               

        
        result = cur.fetchall()
        conn.close()
        txt_name = []
        txt = []
        for i in range(len(result)):
            txt_name.append(result[i][0])
            txt.append(result[i][1])

        # print(txt_name,txt)
        session["txt_name"] = txt_name
        session["txt_text"] = txt


        return render_template("text.html",login=True,name=session["txt_name"] ,txt=session["txt_text"])
    else:
        return redirect(url_for("index"))