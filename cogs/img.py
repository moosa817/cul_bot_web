import discord
from discord.ext import commands
import os
import random
import sqlite3
# <33
conn = sqlite3.connect("stuff.db")
cur = conn.cursor()

class img(commands.Cog):
    def __init__(self,client):
        
        self.client = client


    @commands.Cog.listener()
    async def on_message(self,message):
        result = cur.execute("SELECT * FROM `img_stuff`")
        results = result.fetchall()
        names = []
        imgs = []
        og_image = ""
        for i in results:
            names.append(i[1])
            imgs.append(i[2])

        for name in names:
            if message.content.startswith(name) or message.content.startswith(name.upper()) or message.content.startswith(name.lower()) or message.content.startswith(name.capitalize()):
                index = names.index(name)
                image = imgs[index]


                images = []
                for k in image.split(","):
                    images.append(k)

                
                og_image = random.choice(images)
                
                try:
                    a,b = og_image.split("/")
                    if a == "imgs":
                        is_img = True
                except:
                    is_img = False
                
                if is_img:
                    await message.channel.send(file=discord.File(og_image))
                else:
                    await message.channel.send(og_image)
                
           

async def setup(client):
    await client.add_cog(img(client))