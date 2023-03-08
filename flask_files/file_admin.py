import config
from flask import render_template,request,session,Blueprint
from pymongo import MongoClient

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

                
                client = MongoClient(config.mongo_str)
                db = client.get_database('cul_bot')
                records = db.logs
                
                result = records.find({})

                for i in result:
                    ips.append(i.get("ip_address"))
                    time.append(i.get("time"))


                return render_template("admin.html",login=True,ips=ips,times=time)
            else:
                # print("render 1")
                return render_template("admin.html",stuff=True)
    elif session.get("admin_login"):
        ips = []
        time = []

        client = MongoClient(config.mongo_str)
        db = client.get_database('cul_bot')
        records = db.logs

        result = records.find()


        for i in result:
            ips.append(i.get("ip_address"))
            time.append(i.get("time"))


        return render_template("admin.html",login=True,ips=ips,times=time)
    return render_template("admin.html")
