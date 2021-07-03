import discord
from discord.ext import commands


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
    
        
bot.run('ODYwNzg5MDAwMDYxODQ1NTE0.YOAWOg.ThcPFf4dg1v7IJrOH7n2GrueNiw')
