from flask import Blueprint,request,session,jsonify
import config
import mysql.connector

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



        # add new input to database replacing it with original input
        conn = mysql.connector.connect(
        host=config.db_host,
        user=config.db_user,
        passwd=config.db_pwd,
        database=config.db_database)
        cur = conn.cursor()

        sql = "UPDATE text_stuff SET name = '%s' WHERE name= '%s'"
        val = (new_input, original_input)
        cur.execute(sql % val)

        conn.commit()
        conn.close()
        return jsonify({"success":"renamed successfully"})


@delete_txt_name.route("/delete_txt_name",methods=["POST"])
def del_name():
    if request.method == "POST":
        delete_txt_input = request.form["delete_input"]
        try:
            session["txt_name"].remove(delete_txt_input)
            
            conn = mysql.connector.connect(
                host=config.db_host,
                user=config.db_user,
                passwd=config.db_pwd,
                database=config.db_database)
            cur = conn.cursor()
            sql = "DELETE FROM text_stuff WHERE name = '%s'"
            val = (delete_txt_input)
            cur.execute(sql % val)
            conn.commit()
            conn.close()
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



        # add new input to database replacing it with original input
        conn = mysql.connector.connect(
        host=config.db_host,
        user=config.db_user,
        passwd=config.db_pwd,
        database=config.db_database)
        cur = conn.cursor()

        # print("here editing",input1,input2)
        sql = "UPDATE text_stuff SET text = '%s' WHERE text= '%s'"
        val = (new_input, original_input)
        cur.execute(sql % val)

        conn.commit()
        conn.close()
        return jsonify({"success":"renamed successfully"})