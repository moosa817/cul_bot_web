from flask import Flask,render_template,request,session,redirect,url_for
import os
from flask_files.file_index import index_page
from flask_files.index_edit import delete_img,delete_name,edit_name
from flask_files.admin_edit import log_page
from flask_files.file_admin import admin_page
from flask_files.file_txt import txt_page
from flask_files.txt_edit import edit_txt_name,delete_txt_name,edit_txt_txt
UPLOAD_FOLDER = '/tmp'
b = os.getcwd()
print(os.listdir())
UPLOAD_FOLDER = os.path.join(b, UPLOAD_FOLDER) 
# print(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = set(['png','jpg', 'jpeg', 'gif','webp','tiff'])


# Initialize our app and the bot itself
app = Flask(__name__)

app.register_blueprint(index_page)


app.register_blueprint(edit_name)
app.register_blueprint(delete_img)
app.register_blueprint(delete_name)

app.register_blueprint(admin_page)
app.register_blueprint(log_page)

app.register_blueprint(txt_page)
app.register_blueprint(edit_txt_name)
app.register_blueprint(delete_txt_name)
app.register_blueprint(edit_txt_txt)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

app.secret_key = "super secret key"
app.url_map.strict_slashes = False

@app.before_request
def make_session_permanent():
    session.permanent = True 




@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index_page.index"))


@app.route("/surprise",methods=["GET","POST"])
def prank():
    return render_template("prank.html")

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
