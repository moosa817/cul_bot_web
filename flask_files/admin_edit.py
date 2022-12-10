import config
from flask import Flask,render_template,request,session,redirect,url_for,jsonify,Blueprint
from werkzeug.utils import secure_filename
import os
import datetime
import mysql.connector
from flask_files.file_index import index_page
from flask_files.index_edit import edit_name,delete_img,delete_name

log_page = Blueprint('log_page', __name__, template_folder='templates')

@log_page.route("/log",methods=["GET", "POST"])
def log():
# log stuff
    # print("logging")
    ip = request.form["ip"]
    now = datetime.datetime.now()
    utcnow = datetime.datetime.utcnow()
    diff = utcnow-now

    diff_hr = diff.total_seconds()/60/60
    diff_hr = "{:.1f}".format(diff_hr)

    diff_hr = float(diff_hr)
    diff_hr = int(diff_hr)
   
    
    

    def convert(seconds):
        min, sec = divmod(seconds, 60)
        hour, min = divmod(min, 60)
        return '%d:%02d:%02d' % (hour, min, sec)

    time_diff = convert(diff.total_seconds())

    if diff.total_seconds() < 0:
        final_time = now.strftime(f"%a %d %b %H:%M:%S{time_diff}")
    else:
        final_time = now.strftime(f"%a %d %b %H:%M:%S+{time_diff}")

    
    # f = open('logs.csv','a')
    # f.write(f'\n{ip},{final_time}')


    conn = mysql.connector.connect(
                    host=config.db_host,
                    user=config.db_user,
                    passwd=config.db_pwd,
                    database=config.db_database)
    cur = conn.cursor()  
    sql = "INSERT INTO `logs` (time,ip_address) VALUES ('%s' ,'%s')"
    val = (final_time,ip)
    cur.execute(sql % val)
    conn.commit()
    conn.close()
    return jsonify({"success": True})