import config
from flask import Flask,render_template,request,session,redirect,url_for,jsonify,Blueprint
from werkzeug.utils import secure_filename
import os
import datetime
import mysql.connector
from flask_files.file_index import index_page
from flask_files.index_edit import edit_name,delete_img,delete_name


admin_page = Blueprint('admin_page', __name__, template_folder='templates')


@admin_page.route("/admin",methods=["GET","POST"])
def admin():
    if request.method == "POST":
        if request.form.get("name"):
            username = request.form["name"]
            pwd = request.form["pwd"]


            if username == config.admin and pwd==config.admin_pwd:
                session["admin_login"] = True
               

                ips = []
                time = []
                conn = mysql.connector.connect(
                    host=config.db_host,
                    user=config.db_user,
                    passwd=config.db_pwd,
                    database=config.db_database)
                cur = conn.cursor()  
                sql = "SELECT ip_address,time from `logs` "

                cur.execute(sql)
                result = cur.fetchall()
                conn.close()

                for i in result:
                    ips.append(i[0])
                    time.append(i[1])

                return render_template("admin.html",login=True,ips=ips,times=time)
            else:
                # print("render 1")
                return render_template("admin.html",stuff=True)
    elif session.get("admin_login"):
        ips = []
        time = []
        conn = mysql.connector.connect(
                    host=config.db_host,
                    user=config.db_user,
                    passwd=config.db_pwd,
                    database=config.db_database)
        cur = conn.cursor()  
        sql = "SELECT ip_address,time from `logs` "

        cur.execute(sql)
        result = cur.fetchall()
        conn.close()

        for i in result:
            ips.append(i[0])
            time.append(i[1])
        return render_template("admin.html",login=True,ips=ips,times=time)
    return render_template("admin.html")
