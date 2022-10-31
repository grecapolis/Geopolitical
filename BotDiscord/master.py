### Truc à améliorer :
#faille potentielle au niveau du $stopbot (si quelqu'un arrive à avoir accès au terminal)

#Dans le $resume, le bote a le hocquet

### Pour les données :

from data.dataHandler import Database_Handler

database_handler = Database_Handler("database.db")

### Le code :

import random
import fonction
import discord
import time
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix = "$", description = "Je vais peut-être vous hacker.")

@bot.event
async def on_ready():
    print("Démarrage effectué")

@bot.command()
@commands.is_owner()
async def stopbot(ctx):
    alp = "azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN1234567890&#{"
    security_code = ""
    for i in range(50):
        security_code = security_code + random.choice(alp)
    print(security_code)

    def check(message):
        return message.author == ctx.message.author and ctx.channel == message.channel
    
    await ctx.send("Une clé de sécurité a été envoyée, veuiller me la redonner.")
    respond = await bot.wait_for("message", check = check)
    respond = str(respond.content)

    if respond == security_code :
        exit()
    else:
        await ctx.send("Clé de sécurité erronée.")

@bot.command()
async def inscription(ctx):
    if fonction.verifpv(str(ctx.message.author)):

        user_id = str(ctx.message.author)

        if database_handler.test_inscription(user_id):
            await ctx.send("Vous êtes déjà enregistré.")
    
        else:
            database_handler.register(user_id)
            await ctx.send("Vous avez bien été enregistré")
    else:
        await ctx.send("Veuillez retirer le ';' de votre pseudo.")

@bot.command()
async def set(ctx):
    if fonction.verifpv(str(ctx.message.author)):
        await ctx.send("**ATTENTION** : Modifier votre budget retardera de 24h le perception des impôts")
        listparametre = ["economique", "social", "diplomatique", "militaire", "renseignement"]
        if database_handler.test_inscription(str(ctx.message.author)):
            message = ctx.message.content
            message = fonction.sepmess(message)
            if len(message)==3:
                message[2] = int(message[2])

                if message[1] in listparametre and type(message[2]) == int and message[2]>=0:
                    parametre = message[1]
                    new_value = message[2]
                    discord_id = str(ctx.message.author)
                    database_handler.modification(parametre, new_value, discord_id)
                    await ctx.send("Paramètre modifié.")

                else :
                    await ctx.send("Les paramètres de la commande sont faux.")
                    await ctx.send("Il faut entrer $set <parametre> <nouvelle_valeur (forcément un entier positif)>")
                    await ctx.send("Les paramètres possibles sont : economique, social, diplomatique, militaire et renseignement")
            else:
                await ctx.send("Les paramètres de la commande sont faux. *")
                await ctx.send("Il faut entrer $set <parametre> <nouvelle_valeur (forcément un entier positif)>")
                await ctx.send("Les paramètres possibles sont : economique, social, diplomatique, militaire et renseignement")
    
        else:
            await ctx.send("Vous n'êtes pas enregistré, faites un $inscription")
    
    else:
        await ctx.send("Veuillez retirer le ';' de votre pseudo.")

@bot.command()
async def resume(ctx):
    if fonction.verifpv(str(ctx.message.author)):
        if database_handler.test_inscription(str(ctx.message.author)):
            data = database_handler.selectall(str(ctx.message.author))
            #on collecte le revenu du pays

            ###################################################################################################################################            
            #Ici l'argent
            argentsup = int((25*data['population'])*data['niveau de développement'])*(data['economique']/20)
            if (time.time() - data['date_last_taxes']) >= 86400:
                ti = time.time() - data['date_last_taxes']
                a=0
                while ti >= 86400:
                    ti -= 86400
                    a += 1
                
                argentsup = argentsup - argentsup * ((data['economique'] + data['social'] + data['diplomatique'] + data['renseignement'] + data['militaire']) / 100)
                argentsup = argentsup * a
                database_handler.salary(argentsup, str(ctx.message.author))
            
            argentsup = ((25*data['population'])*data['niveau de développement'])*(data['economique']/20)
            ###################################################################################################################################
            #Ici la Pop
            popsup = int(data['population'] * (data['social']/20) * (21 - data['niveau de développement']))
            if (time.time() - data['date_last_taxes']) >= 86400:
                ti = time.time() - data['date_last_taxes']
                a = 0
                while ti >= 86400:
                    ti -= 86400
                    a = a + 1
                
                print(a)
                for i in range(a):
                    database_handler.newhab(popsup, str(ctx.message.author))
            ###################################################################################################################################

            data = database_handler.selectall(str(ctx.message.author))

            #Ligne ULTRA LONGUE, mais sinon, le bot a le hocquet
            #ça change pas grand chose en fait
            message = f"----------- Résumé -----------\nVous êtes le leader de la **{data['nom']}** \nVotre pays est de niveau **{data['niveau de développement']}/20** en terme de développement\nIl y a **{data['population']}** habitants de votre pays\nVous avez actuellement {data['argent']} ¤ dans votre tésorerie\nVous avez un revenu Brut de {argentsup} ¤ toutes les 24h\n-----Budget-----\néconomique : {data['economique']}\ndiplomatique : {data['diplomatique']}\nsocial : {data['social']}\nmilitaire : {data['militaire']}\nAu renseignement : {data['renseignement']}\n\nVous dépensez donc {(data['economique'] + data['social'] + data['diplomatique'] + data['renseignement'] + data['militaire'])} % de votre revenu Brut."

            print(message)
            await ctx.send(message)
 
        else:
            await ctx.send("Vous n'êtes pas enregistré, faites un $inscription")
    else :
        await ctx.send("Veuillez retirer le ';' de votre pseudo.")

@bot.command()
async def name(ctx):
    if fonction.verifpv(str(ctx.message.author)):
        if database_handler.test_inscription(str(ctx.message.author)):
            
            message = fonction.sepmess(ctx.message.content)
            
            if fonction.verifpv(str(message[1])):
                database_handler.setname(message[1], str(ctx.message.author))
                await ctx.send(f"Bonjour camarade {message[1]} !!!")
            
            else:
                await ctx.send("Veuillez retirer le ';' de votre pseudo.")
        else:
            await ctx.send("Vous n'êtes pas enregistré, faites un $inscription")
    else :
        await ctx.send("Veuillez retirer le ';' de votre pseudo.")

@bot.command()
async def listepays(ctx):
    listebrut = database_handler.listpays()
    message = "Les best des best :"

    for i in listebrut:
        message = message + f"\n- {i}"

    await ctx.send(message)


@bot.command()
async def coucou(ctx):
    print("coucou")
    await ctx.send("Bonjour camarade !")


### On lance le Bot

bot.run("MTAzNDg2MjIzMDg3OTA4NDY2NQ.Gch9U5.gBLYkHlK42mS1CrH_gnA5ZB6nhwa6BCZxBMqIw")