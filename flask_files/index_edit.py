from flask import Blueprint,request,session,jsonify
import config
import mysql.connector

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
        conn = mysql.connector.connect(
        host=config.db_host,
        user=config.db_user,
        passwd=config.db_pwd,
        database=config.db_database)
        cur = conn.cursor()

        sql = "UPDATE img_stuff SET name = '%s' WHERE name= '%s'"
        val = (new_input, original_input)
        cur.execute(sql % val)

        conn.commit()
        conn.close()
        return jsonify({"success":"renamed successfully"})


@delete_name.route("/delete_name",methods=["POST"])
def del_name():
    if request.method == "POST":
        delete_input = request.form["delete_input"]
        try:
            session["names"].remove(delete_input)
            conn = mysql.connector.connect(
                host=config.db_host,
                user=config.db_user,
                passwd=config.db_pwd,
                database=config.db_database)
            cur = conn.cursor()
            sql = "DELETE FROM img_stuff WHERE name = '%s'"
            val = (delete_input)
            cur.execute(sql % val)
            conn.commit()
            conn.close()
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
            conn = mysql.connector.connect(
                host=config.db_host,
                user=config.db_user,
                passwd=config.db_pwd,
                database=config.db_database)
            cur = conn.cursor()
            sql = "UPDATE img_stuff SET img = '%s' WHERE name = '%s'"
            val = (a,name)
            cur.execute(sql % val)
            # result = cur.fetchall()
            # print(result)
            conn.commit()
            conn.close()


            return jsonify({"success":True})
        except Exception as e:
            print(e)
            return jsonify({"success": False})
