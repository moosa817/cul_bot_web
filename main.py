
# Note: You really should not use this.
# You can easily convert your app
# to use Quart by using async+await
# and then use loop.create_task(bot.start(...))
# before using app.run.
import config
import requests
from threading import Thread
from flask import Flask,render_template,request,session,redirect,url_for,jsonify
from functools import partial
from discord.ext import commands
import discord
import os
import sqlite3
# Initialize our app and the bot itself
app = Flask(__name__)


app.secret_key = "super secret key"
app.url_map.strict_slashes = False

@app.before_request
def make_session_permanent():
    session.permanent = True 

def mixedCase(*args):
  """
  Gets all the mixed case combinations of a string

  This function is for in-case sensitive prefixes
  """
  total = []
  import itertools
  for string in args:
    a = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in       string)))
    for x in list(a): total.append(x)

  return list(total)


intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=config.prefix,intents=intents)



@bot.tree.command(name="hello")
async def hello(interaction:discord.Interaction):
    await interaction.response.send_message("i need badge")






@bot.event
async def on_ready():
    print("bot ready?")
    for filename in os.listdir("./cogs"):
        if filename.endswith('.py'):
            print(f"{filename } loaded ")
            await bot.load_extension(f'cogs.{filename[:-3]}')
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print(e)



# Set up the 'index' route
@app.route("/",methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("name"):
            username = request.form["name"]
            pwd = request.form["pwd"]

            def login(username, password):
                session["username"] = username
                session["password"] = password
                name = []
                img = []
                conn = sqlite3.connect("stuff.db")
                cur = conn.cursor()   
                cur.execute("SELECT name,img FROM `img_stuff`")
                conn.commit()
                result = cur.fetchall()
                conn.close()
                for i in range(len(result)):
                    name.append(result[i][0])
                    img.append(result[i][1])

                imgs = []
                for f in img:
                    if f is not None:
                        imgs.append(f.split(","))

                session["names"] = name
                session["imgs"] = imgs
                return render_template("index.html",login=True,name=name,imgs=imgs)


            if username == "cul" and pwd=="cul":
                return login(username,pwd)
            else:
                # print("render 1")
                return render_template("index.html",stuff="error")

        elif request.form.get("key"):
            key = request.form["key"]
            conn = sqlite3.connect("stuff.db")
            cur = conn.cursor()   
            cur.execute("SELECT name,img FROM `img_stuff` WHERE name = :orignal_input", {"orignal_input":key})
            conn.commit()
            result = cur.fetchall()
            conn.close()
            
            if result:
                return render_template("index.html",login=True,name=session["names"],imgs=session["imgs"],stuff_error="Already exists")

            elif len(key) >50:
                return render_template("index.html",login=True,name=session["names"],imgs=session["imgs"],stuff_error="Too Long")
            else:
                conn = sqlite3.connect("stuff.db")
                cur = conn.cursor()   
                cur.execute("INSERT INTO `img_stuff` (name,img) VALUES ( :orignal_input ,:b )", {"orignal_input":key,"b":""})
                conn.commit()
                conn.close()
                session["names"].append(key)
                return render_template("index.html",login=True,name=session["names"],imgs=session["imgs"])

        elif request.form.get("thumbnail"):
            img_url = request.form["thumbnail"]
            name = request.form["name-url"]
            def is_url_image(image_url):
                try:
                    image_formats = ("image/png", "image/jpeg", "image/jpg","image/gif","image/webp")
                    r = requests.head(image_url)
                    # print(r.headers["content-type"])
                    if r.headers["content-type"] in image_formats:
                        return True
                    return False
                except:
                    return False

            # print(is_url_image(img_url))
            if is_url_image(img_url) and name:
                # print("here")
                conn = sqlite3.connect("stuff.db")
                cur = conn.cursor()  
                index = session["names"].index(name)
                session["imgs"][index].append(img_url)
                s = session["imgs"][index]
                a = ",".join(s)

                cur.execute("UPDATE img_stuff SET img = :new_input WHERE name= :orignal_input",{"new_input":a, "orignal_input":name})
                conn.commit()
                conn.close()


                return render_template("index.html",login=True,name=session["names"],imgs=session["imgs"])

                
            else:
                # print("not here")
                return render_template("index.html",login=True,name=session["names"],imgs=session["imgs"])


    if session.get('username'):
        name = []
        img = []
        conn = sqlite3.connect("stuff.db")
        cur = conn.cursor()   
        cur.execute("SELECT name,img FROM `img_stuff`")
        conn.commit()
        result = cur.fetchall()
        conn.close()
        for i in range(len(result)):
            name.append(result[i][0])
            img.append(result[i][1])

        imgs = []

        for f in img:
            if f is not None:
                imgs.append(f.split(","))

        session["names"] = name
        session["imgs"] = imgs

        return render_template("index.html",login=True,name=name,imgs=imgs)
    else:
        # print("render 2")
        return render_template("index.html",login=False)



@app.route("/edit_name",methods=["POST","GET"])
def edit_name():
    if request.method == "POST":
        input1 = request.form["input1"]
        input2 = request.form["input2"]
       
        new_input = input1
        original_input = input2
        index = session["names"].index(original_input)
        session["names"][index] = new_input



        # add new input to database replacing it with original input
        conn = sqlite3.connect("stuff.db")
        cur = conn.cursor()
        cur.execute("UPDATE img_stuff SET name = :new_input WHERE name= :orignal_input",{"new_input":new_input, "orignal_input":original_input})

        conn.commit()
        conn.close()
        return jsonify({"success":"renamed successfully"})


@app.route("/delete_name",methods=["POST"])
def delete_name():
    if request.method == "POST":
        delete_input = request.form["delete_input"]
        try:
            session["names"].remove(delete_input)
            conn = sqlite3.connect("stuff.db")
            cur = conn.cursor()

            cur.execute("DELETE FROM img_stuff WHERE name = :orignal_input", {"orignal_input":delete_input})
            conn.commit()
            conn.close()
            return jsonify({"success":True})
        except:
            return jsonify({"success": False})


@app.route("/del_img",methods=["POST"])
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
            conn = sqlite3.connect("stuff.db")
            cur = conn.cursor()

            cur.execute("UPDATE img_stuff SET img = :a WHERE name = :orignal_input", {"a":a,"orignal_input":name})
            # result = cur.fetchall()
            # print(result)
            conn.commit()
            conn.close()


            return jsonify({"success":True})
        except Exception as e:
            print(e)
            return jsonify({"success": False})




@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# Make a partial app.run to pass args/kwargs to it
partial_run = partial(app.run, host="0.0.0.0", debug=True, use_reloader=False)

# Run the Flask app in another thread.
# Unfortunately this means we can't have hot reload
# (We turned it off above)
# Because there's no signal support.

t = Thread(target=partial_run)
t.start()

# Run the bot
bot.run(config.auth)

# Now, you can visit your localhost or your VPS' IP in your browser and you should see a message!