from flask import Blueprint,request,session,jsonify
import config
from pymongo import MongoClient

edit_txt_name = Blueprint('edit_txt_name', __name__, template_folder='templates')

delete_txt_name = Blueprint('delete_txt_name', __name__,template_folder='templates')

delete_txt_img = Blueprint('delete_txt_img', __name__, template_folder='templates')

edit_txt_txt = Blueprint('edit_txt_txt', __name__, template_folder='templates')




@edit_txt_name.route('/edit_txt_name',methods=['GET','POST'])
def edit_txt_nam():
    if request.method == "POST":
        input1 = request.form["input1"]
        input2 = request.form["input2"]
       
        new_input = input1
        original_input = input2
        index = session["txt_name"].index(original_input)
        session["txt_name"][index] = new_input

        client = MongoClient(config.mongo_str)
        db = client.get_database('cul_bot')
        records = db.text_stuff
        
        records.update_one({"name":original_input},{"$set":{"name":new_input}})

        return jsonify({"success":"renamed successfully"})


@delete_txt_name.route("/delete_txt_name",methods=["POST"])
def del_name():
    if request.method == "POST":
        delete_txt_input = request.form["delete_input"]
        try:
            session["txt_name"].remove(delete_txt_input)

                
            client = MongoClient(config.mongo_str)
            db = client.get_database('cul_bot')
            records = db.text_stuff            

            records.delete_one({"name":delete_txt_input})
            return jsonify({"success":True})
        except:
            return jsonify({"success": False})


@edit_txt_txt.route('/edit_txt_txt',methods=['GET','POST'])
def edit_txt():
    if request.method == "POST":
        input1 = request.form["input1"]
        input2 = request.form["input2"]
       
        new_input = input1
        original_input = input2
        index = session["txt_text"].index(original_input)
        session["txt_text"][index] = new_input
        name = session["txt_name"][index]
        
        client = MongoClient(config.mongo_str)
        db = client.get_database('cul_bot')
        records = db.text_stuff


        records.update_one({"name":name,"text":original_input},{"$set":{"text":new_input}})

        return jsonify({"success":"renamed successfully"})