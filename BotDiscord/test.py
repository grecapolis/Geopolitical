import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix = "$", description = "Je vais peut-être vous hacker.")

@bot.event
async def on_ready():
    print("ME VOILAAAAAAAA")

@bot.command()
async def coucou(ctx):
    print("coucou")
    await ctx.send("Bonjour camarade !")


@bot.command()
async def Info(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    serverDescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name

    message = "Il y a " + str(numberOfPerson) + " personnes dans *" + serverName + "*"
    await ctx.send(message)

@bot.command()
async def bonjour(ctx):
    message = "Bonjour *camarade* ! Bienvenu, veut-tu m'aider à faire triompher le communisme dans *" + ctx.guild.name + "* ?" 
    await ctx.send(message)

@bot.command()
async def say(ctx, *texte):
    await ctx.send(" ".join(texte))

@bot.command()
async def cuisiner(ctx):
    await ctx.send("Balance ton plat :")

    def check(message):
        return message.author == ctx.message.author and ctx.channel == message.channel

    recette = await bot.wait_for("message", timeout = 10, check = check)
    
    respond = "Toi, t'aime les " + str(recette.content) + " je vas y ajouter de la vodka."
    message = await ctx.send(respond)
bot.run("MTAzNDg4MDgyMjA1NjA3NTI5NA.G2ZS5c.SwWHgcsZ5m1fFEtT1G-dx6yIZeRFpPMXxLMjd8")