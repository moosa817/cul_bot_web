import config
from flask import request,jsonify,Blueprint
import datetime
from pymongo import MongoClient

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



    client = MongoClient(config.mongo_str)
    db = client.get_database('cul_bot')
    records = db.logs
    

    records.insert_one({"time":final_time,"ip":ip})
    return jsonify({"success": True})