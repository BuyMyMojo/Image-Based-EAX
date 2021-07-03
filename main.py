import discord
from discord.ext import commands
import requests
import cv2 as cv
from PIL import Image as pil_img
from PIL import ImageChops as pil_img_chops
from PIL import ImageFilter as pil_img_filter
import os
import time
import math
import deeppyer as dp

owner_id = "383507911160233985"

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f"Bot is ready")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Using EAX on images"))
    
    
# This command sends back the arguments given as one message
@bot.command()
async def foo(ctx, *, arg):
    await ctx.send(arg)
    
@bot.command()
async def censor(ctx, img: str):
    uid = str(ctx.message.author.id)
    download_temp_file(img, "censor_base_" + uid)
    
    imgA = pil_img.open("./temp/" + "censor_base_" + uid)
    
    blured_image = imgA.filter(pil_img_filter.BoxBlur(10))
    blured_image.save("./temp/censor_" + uid + ".png")
    
    await ctx.send(file=discord.File('./temp/censor_' + uid + '.png'))
    
    delete_temp_file("censor_base_" + uid)
    delete_temp_file("censor_" + uid + ".png")
    

@bot.command()
async def gaycensor(ctx, img: str):
    uid = str(ctx.message.author.id)
    download_temp_file(img, "gaycensor_base_" + uid)
    
    imgA = pil_img.open("./temp/" + "gaycensor_base_" + uid)
    flag = pil_img.open("./censorship_flag.png")
    
    flag_x_res = math.trunc(int(int(imgA.size[0]) * 0.75))
    flag_y_res = math.trunc(int(int(imgA.size[1]) * 0.75))
    
    flag = flag.resize((flag_x_res,flag_y_res), pil_img.ANTIALIAS)
    
    paste_x = math.trunc(int(int(imgA.size[0] - flag.size[0]) / 2))
    paste_y = math.trunc(int(int(imgA.size[1] - flag.size[1]) / 2))
    
    imgA.paste(flag, (paste_x, paste_y), flag)
    imgA.save("./temp/gaycensor_" + uid + ".png")
    
    await ctx.send(file=discord.File('./temp/gaycensor_' + uid + '.png'))
    
    delete_temp_file("gaycensor_base_" + uid)
    delete_temp_file("gaycensor_" + uid + ".png")

# Generates an image displaying the difference between two images (RGB 8bit)
@bot.command()
async def imgdif(ctx, img1: str, img2: str):
    uid = str(ctx.message.author.id)
    download_temp_file(img1, "dif_img_1_" + uid)
    download_temp_file(img2, "dif_img_2_" + uid)
    
    get_img_dif("dif_img_1_" + uid, "dif_img_2_" + uid, ctx)
    
    delete_temp_file("dif_img_1_" + uid)
    delete_temp_file("dif_img_2_" + uid)
    
    await ctx.send(file=discord.File('./temp/difference_' + uid + '.png'))
    
    delete_temp_file("difference_" + uid + ".png")

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
def get_img_dif(name1, name2, ctx):
    imgA = pil_img.open("./temp/" + name1)
    imgB = pil_img.open("./temp/" + name2)
    
    imgA_convert = imgA.convert("RGB")
    imgB_convert = imgB.convert("RGB")
    
    difference = pil_img_chops.difference(imgA_convert, imgB_convert)
    difference.save("./temp/difference_" + str(ctx.message.author.id) + ".png")
    
@bot.command()
async def fry(ctx, img: str, colour="red"):
    uid = str(ctx.message.author.id)
    download_temp_file(img, "fry_base_" + uid)
    
    imgA = pil_img.open("./temp/" + "fry_base_" + uid)
    if colour == "red":
        imgB = await dp.deepfry(imgA, colours=dp.DefaultColours.red, flares=False)
    elif colour == "blue":
        imgB = await dp.deepfry(imgA, colours=dp.DefaultColours.blue, flares=False)
    else:
        imgB = await dp.deepfry(imgA, colours=dp.DefaultColours.red, flares=False)
    imgB.save("./temp/fry_" + uid + ".png")
    
    await ctx.send(file=discord.File('./temp/fry_' + uid + '.png'))
    
    delete_temp_file("fry_base_" + uid)
    delete_temp_file("fry_" + uid + ".png")

@bot.command()
async def uid(ctx):
    await ctx.send("Your ID is: " + str(ctx.message.author.id))
    
    
@bot.command()
async def stop(ctx):
    if str(ctx.message.author.id) == owner_id:
        await bot.change_presence(status=discord.Status.offline)
        time.sleep(5)
        await bot.close()
    else:
        await ctx.send("You are now the bot owner")
    
    
        
bot.run('ODYwNzg5MDAwMDYxODQ1NTE0.YOAWOg.ThcPFf4dg1v7IJrOH7n2GrueNiw')
