import math
import os
import time

import deeppyer as dp
import discord
import requests
# import cv2 as cv
from PIL import Image as pil_img
from PIL import ImageChops as pil_img_chops
from PIL import ImageFilter as pil_img_filter
from discord.ext import commands

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
    user_id = str(ctx.message.author.id)
    download_temp_file(img, "censor_base_" + user_id)
    
    img_a = pil_img.open("./temp/" + "censor_base_" + user_id)
    
    blurred_image = img_a.filter(pil_img_filter.BoxBlur(10))
    blurred_image.save("./temp/censor_" + user_id + ".png")
    
    await ctx.send(file=discord.File('./temp/censor_' + user_id + '.png'))
    
    delete_temp_file("censor_base_" + user_id)
    delete_temp_file("censor_" + user_id + ".png")
    

@bot.command()
async def gaycensor(ctx, img: str):
    user_id = str(ctx.message.author.id)
    download_temp_file(img, "gaycensor_base_" + user_id)
    
    img_a = pil_img.open("./temp/" + "gaycensor_base_" + user_id)
    flag = pil_img.open("./censorship_flag.png")
    
    flag_x_res = math.trunc(int(int(img_a.size[0]) * 0.75))
    flag_y_res = math.trunc(int(int(img_a.size[1]) * 0.75))
    
    flag = flag.resize((flag_x_res,flag_y_res), pil_img.ANTIALIAS)
    
    paste_x = math.trunc(int(int(img_a.size[0] - flag.size[0]) / 2))
    paste_y = math.trunc(int(int(img_a.size[1] - flag.size[1]) / 2))
    
    img_a.paste(flag, (paste_x, paste_y), flag)
    img_a.save("./temp/gaycensor_" + user_id + ".png")
    
    await ctx.send(file=discord.File('./temp/gaycensor_' + user_id + '.png'))
    
    delete_temp_file("gaycensor_base_" + user_id)
    delete_temp_file("gaycensor_" + user_id + ".png")


# Generates an image displaying the difference between two images (RGB 8bit)
@bot.command()
async def imgdif(ctx, img1: str, img2: str):
    user_id = str(ctx.message.author.id)
    download_temp_file(img1, "dif_img_1_" + user_id)
    download_temp_file(img2, "dif_img_2_" + user_id)
    
    get_img_dif("dif_img_1_" + user_id, "dif_img_2_" + user_id, ctx)
    
    delete_temp_file("dif_img_1_" + user_id)
    delete_temp_file("dif_img_2_" + user_id)
    
    await ctx.send(file=discord.File('./temp/difference_' + user_id + '.png'))
    
    delete_temp_file("difference_" + user_id + ".png")


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
    img_a = pil_img.open("./temp/" + name1)
    img_b = pil_img.open("./temp/" + name2)
    
    img_a_convert = img_a.convert("RGB")
    img_b_convert = img_b.convert("RGB")
    
    difference = pil_img_chops.difference(img_a_convert, img_b_convert)
    difference.save("./temp/difference_" + str(ctx.message.author.id) + ".png")


@bot.command()
async def fry(ctx, img: str, colour="red"):
    user_id = str(ctx.message.author.id)
    download_temp_file(img, "fry_base_" + user_id)
    
    img_a = pil_img.open("./temp/" + "fry_base_" + user_id)
    if colour == "red":
        img_b = await dp.deepfry(img_a, colours=dp.DefaultColours.red, flares=False)
    elif colour == "blue":
        img_b = await dp.deepfry(img_a, colours=dp.DefaultColours.blue, flares=False)
    else:
        img_b = await dp.deepfry(img_a, colours=dp.DefaultColours.red, flares=False)
    img_b.save("./temp/fry_" + user_id + ".png")
    
    await ctx.send(file=discord.File('./temp/fry_' + user_id + '.png'))
    
    delete_temp_file("fry_base_" + user_id)
    delete_temp_file("fry_" + user_id + ".png")


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
