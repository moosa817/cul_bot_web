from flask import Blueprint,request,session,jsonify
import config
from pymongo import MongoClient

edit_name = Blueprint('edit_name', __name__, template_folder='templates')

delete_name = Blueprint('delete_name', __name__,template_folder='templates')

delete_img = Blueprint('delete_img', __name__, template_folder='templates')




@edit_name.route('/edit_name',methods=['GET','POST'])
def edit_nam():
    if request.method == "POST":
        input1 = request.form["input1"]
        input2 = request.form["input2"]
       
        new_input = input1
        original_input = input2
        index = session["names"].index(original_input)
        session["names"][index] = new_input



        # add new input to database replacing it with original input
        client = MongoClient(config.mongo_str)
        db = client.get_database('cul_bot')
        records = db.img_stuff
        records.update_one({"name":original_input},{"$set":{"nae":new_input}})

        return jsonify({"success":"renamed successfully"})


@delete_name.route("/delete_name",methods=["POST"])
def del_name():
    if request.method == "POST":
        delete_input = request.form["delete_input"]
        try:
            session["names"].remove(delete_input)

            client = MongoClient(config.mongo_str)
            db = client.get_database('cul_bot')
            records = db.img_stuff
            
            records.delete_one({"name":delete_input})

            return jsonify({"success":True})
        except:
            return jsonify({"success": False})


@delete_img.route("/del_img",methods=["POST"])
def del_img():
    if request.method == "POST":
        row_no = request.form["row_no"]
        img_no = request.form["img_no"]

        

        row_no = int(row_no)
        img_no = int(img_no)


        name = session["names"][row_no]
        try:
            session["imgs"][row_no][img_no] = ""
            img_row = session["imgs"][row_no]
            # print(img_row)


            img_copy = list(filter(None, img_row))
            a = ",".join(img_copy)
            # print(a)
            client = MongoClient(config.mongo_str)
            db = client.get_database('cul_bot')
            records = db.img_stuff
                
            records.update_one({"name":name},{"$set":{"img":a}})


            return jsonify({"success":True})
        except Exception as e:
            print(e)
            return jsonify({"success": False})
