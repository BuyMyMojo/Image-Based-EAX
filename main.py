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
    
# simple addition, adds two numbers together
@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)

# simple addition, adds two numbers together but done in a seperate function
@bot.command()
async def funcadd(ctx, a: int, b: int):
    await ctx.send(adding(a, b))

def adding(a: int, b: int):
    return(a+b)

@bot.command()
async def ImgDif(ctx, img1: str, img2: str):
    download_temp_image(img1, "dif_img_1")
    download_temp_image(img2, "dif_img_2")
    
    get_img_dif("dif_img_1", "dif_img_2")
    
    delete_temp_file("dif_img_1")
    delete_temp_file("dif_img_2")
    
    await ctx.send(file=discord.File('./temp/difference.png'))
    
    delete_temp_file("difference.png")
        
def download_temp_image(img, name):
    response = requests.get(img)
    file = open("./temp/" + name, "wb")
    file.write(response.content)
    file.close()
    
def delete_temp_file(name):
    os.remove("./temp/"+ name)

def get_img_dif(name1, name2):
    imgA = pil_img.open("./temp/" + name1)
    imgB = pil_img.open("./temp/" + name2)
    
    imgA_convert = imgA.convert("RGB")
    imgB_convert = imgB.convert("RGB")
    
    difference = pil_img_chops.difference(imgA_convert, imgB_convert)
    difference.save("./temp/difference.png")
    
    
    
    
    
        
bot.run('ODYwNzg5MDAwMDYxODQ1NTE0.YOAWOg.ThcPFf4dg1v7IJrOH7n2GrueNiw')
