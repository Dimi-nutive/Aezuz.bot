import discord
from discord import Game
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import random
import os
import re
import asyncio
import json
import requests
from datetime import datetime, timedelta


bot = commands.Bot(command_prefix = commands.when_mentioned_or(">"), intents = discord.Intents.all())


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Aezuz", url="https://www.youtube.com/channel/UCvGrL7OlwM6yGTvOq8k4x1A"))
    print("Logged in as {}".format(bot.user.name))


@bot.event
async def on_member_join(member: discord.Member):
    channel = await bot.fetch_channel("909703685343436811")
    embed = discord.Embed(title = "Welcome !", color =0x9203ea, description=  f"{member.mention} Just joined ! \nWelcome to our server :partying_face: \nWe are glad to see you here !")
    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/909707408878764052/936470255700688956/logo.jpg")
    await channel.send(embed=embed)


@bot.command()
async def reply(ctx, user: discord.User, *, msg:str): # placing in args needed for specification of user and message sent through the bot to the user.
    if ctx.author.guild_permissions.administrator:
        try:
            mbed = discord.Embed(
                description=f'{msg}',
                color=0x2c2f33
            )
            mbed.set_footer(text=f'Message Sent By: {ctx.author}')

            await user.send(embed=mbed)
            return await ctx.send('Reply Sent!!')

        except Exception:
            return await ctx.send(f'Error when sending message to {user}.')
    
# notifier for modmail.

@bot.command()
async def giveaway(ctx, time= None, *, prize=None):
    if time == None:
        return await ctx.send('Please include a time!!')
    elif prize == None:
        return await ctx.send('Please include a prize!!')
    
    embed = discord.Embed(title = "GIveaway!", description = f"{ctx.author.mention}is hosting a giveaway for **{prize}**!!")
    time_convert = {"s": 1, "m":60, "h":3600, "d":86400}
    gawtime = int(time[0]) * time_convert[time[-1]]
    embed.set_footer(text =f'Giveaway ends in {time}')
    gaw_msg =await ctx.send(embed=embed)

    await gaw_msg.add_reaction("🎉")
    await asyncio.sleep(gawtime)

    new_gaw_msg =await ctx.channel.fetch_message(gaw_msg.id)

    users = await new_gaw_msg.reactions[0].users().flatten()
    users.pop(users.index(bot.user))

    winner = random.choice(users)

    await ctx.send(f"Hurray!! {winner.mention} has won the giveaway for **{prize}**")
    
@bot.command()
async def events(ctx):
    embed = discord.Embed(title= "EVENTS", color=discord.Color.from_rgb(random.randrange(0 , 255) , random.randrange(0 , 255) , random.randrange(0 , 255)))
    embed.add_field(name ="Past Events : " ,value = "No past events.", inline = False)
    embed.add_field(name ="Ongoing Events  : " ,value = "No ongoing events.", inline = False)
    embed.add_field(name ="Upcoming Events : " ,value = "Gaming tournament [Starting 15th of march]", inline = False)
    await ctx.send(embed = embed)

@bot.command()
async def confirm_event(ctx):
    def check(m):
        return len(m.content) >= 1 and m.author != bot.user
        
    await ctx.send("Upcoming event : Gaming tournament | Do you want to confirm your entry ?? ")
    entry = await bot.wait_for("message", check=check)
    channel_id =937577482033459240
    entry_channel = bot.get_channel(channel_id)

    if entry.content.lower() == "yes":
        embed = discord.Embed(title ="Confirmation" , olor=discord.Color.from_rgb(random.randrange(0 , 255) , random.randrange(0 , 255) , random.randrange(0 , 255)))
        embed.add_field(name =" User Confirmation for event: " ,value = f"{ctx.author.mention} confirmed their entry for the upcoming event", inline = False)
        embed.add_field(name = "Report: ", value = "If you didnt register please report this in [Aezuz Server](https://discord.gg/QYW5CXz22Z)")
        await ctx.send(embed=embed)
        await entry_channel.send(f'{ctx.author.name} confirmed their entry for upcoming event')



    else:
        await ctx.send("Try again later")




extensions = [ 'Cogs.modmail']

if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)


bot.run("TOKEN")
