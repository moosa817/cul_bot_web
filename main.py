
# Note: You really should not use this.
# You can easily convert your app
# to use Quart by using async+await
# and then use loop.create_task(bot.start(...))
# before using app.run.
import config
from threading import Thread
from flask import Flask,render_template,request,session
from functools import partial
from discord.ext import commands
import discord
import os
# Initialize our app and the bot itself
app = Flask(__name__)

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
@app.route("/")
def hello():
    return "Hello from {}".format(bot.user.name)

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