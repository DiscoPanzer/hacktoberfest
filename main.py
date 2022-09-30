import discord
from discord import message
from discord import colour
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound, BucketType, cooldown, CommandOnCooldown
from discord import Webhook, RequestsWebhookAdapter
from discord.ext.commands.core import check
from discord.utils import get
import logging
import random
import requests
import wikipedia
import asyncio
import time
import json
import sys
from PIL import Image
from io import BytesIO

client = commands.Bot(command_prefix= "*")
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="With Your Mom lol"))
    print(f"---> Logged in as : {client.user.name} , ID : {client.user.id}")
    print(f"---> Total Servers : {len(client.guilds)}\n")
    DiscordComponents(client)
    
    
@client.command()
async def button(ctx):
    await ctx.send("Bing bing bang", components = [Button( label= "Click for free Robux")])
    interaction = await client.wait_for("button_click", check= lambda i: i.component.label.startswith("Click"))
    await interaction.respond(content="Haha you've been hacked retard!")

@client.command(aliases=['bal', 'bl'])
async def balance(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    await open_account(ctx.author)

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f"{user}'s Balance",color = discord.Color.red())
    em.add_field(name="Wallet Balance: ", value=(f"{wallet_amt} TeriMummyCoins"))
    em.add_field(name='Bank Balance:',value=(f"{bank_amt} TeriMummyCoins"), inline=False)
    await ctx.send(embed= em)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        penis = "***You gotta chill out bruh...you can use this command in {:.2f} seconds***". format(error.retry_after)
        await ctx.reply(penis)



@client.command()
@commands.cooldown(1,15,commands.BucketType.member)
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    earnings = random.randrange(101)

    await ctx.send(f"{random.choice(ShitStuff)} donated {earnings} TeriMummyCoins!!")

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json",'w') as f:
        json.dump(users,f)
        
async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open('mainbank.json','w') as f:
        json.dump(users,f)

    return True

async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users

async def update_bank(user,change=0,mode = 'wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('mainbank.json','w') as f:
        json.dump(users,f)
    bal = users[str(user.id)]['wallet'],users[str(user.id)]['bank']
    return bal


@client.command(aliases=['wd'])
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,'bank')
    await ctx.send(f'{ctx.author.mention} You withdrew {amount} coins')
    
    
    
    
    
    
    client.run("TOKEN KEY")
