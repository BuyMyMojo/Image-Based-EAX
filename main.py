import discord
from discord.ext import commands
import requests
import cv2 as cv
from PIL import Image as pil_img
from PIL import ImageChops as pil_img_chops
import os



bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f"Bot is ready")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Using EAX on images"))
    
    
# This command sends back the arguments given as one message
@bot.command()
async def foo(ctx, *, arg):
    await ctx.send(arg)

# Generates an image displaying the difference between two images (RGB 8bit)
@bot.command()
async def ImgDif(ctx, img1: str, img2: str):
    download_temp_file(img1, "dif_img_1")
    download_temp_file(img2, "dif_img_2")
    
    get_img_dif("dif_img_1", "dif_img_2")
    
    delete_temp_file("dif_img_1")
    delete_temp_file("dif_img_2")
    
    await ctx.send(file=discord.File('./temp/difference.png'))
    
    delete_temp_file("difference.png")

# Downloads file into ./temp/     
def download_temp_file(file, name):
    response = requests.get(file)
    file = open("./temp/" + name, "wb")
    file.write(response.content)
    file.close()
    
# Deletes file from ./temp/
def delete_temp_file(name):
    os.remove("./temp/"+ name)

# Generates difference img
def get_img_dif(name1, name2):
    imgA = pil_img.open("./temp/" + name1)
    imgB = pil_img.open("./temp/" + name2)
    
    imgA_convert = imgA.convert("RGB")
    imgB_convert = imgB.convert("RGB")
    
    difference = pil_img_chops.difference(imgA_convert, imgB_convert)
    difference.save("./temp/difference.png")
    
    
    
    
    
        
bot.run('ODYwNzg5MDAwMDYxODQ1NTE0.YOAWOg.ThcPFf4dg1v7IJrOH7n2GrueNiw')
