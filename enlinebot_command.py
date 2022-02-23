#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/19 下午 07:27
# @Author : condal36
# @Site : 
# @File : enlinebot_command.py
# @Software: PyCharm
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get
from discord import FFmpegPCMAudio
from asyncio import run_coroutine_threadsafe as rct
from pytube import YouTube
import asyncio
song_queue=[]
def play_next(ctx, source):
    if len(song_queue) >= 1:
        vc = get(bot.voice_clients, guild=ctx.guild)
        vc.play(FFmpegPCMAudio(list.pop(0)), after=lambda e: next_play(ctx))
        vc.is_playing()
    else:
	    asyncio.run_coroutine_threadsafe(ctx.send("No more songs in queue."))
        return
        

def play_repeat(ctx, audio, msg, n):    
	if 0!=n:
        n = int(n)
        voice = get(bot.voice_clients, guild=ctx.guild)
        rct(msg.edit(content=f'Finished playing the song, {n} more to go.'), bot.loop)
        voice.play(FFmpegPCMAudio(audio), after=lambda e: play_repeat(ctx, audio, msg, n-1))
        voice.is_playing()
    else:
        rct(msg.delete(), bot.loop)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_DEV_BOT')
bot = commands.Bot(command_prefix='')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    game = discord.Game('機...油..好...難...喝...逼逼逼逼')
    await bot.change_presence(status=discord.Status.idle, activity=game)
    print('------')
@bot.command(aliases=['stop'])
async def stop_play(ctx):
    """ Skip the song currently playing. """
    voice=get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
@bot.command(aliases=['g'])
async def grab(ctx,url,title):
    YouTube(url).streams.first().download(output_path='mp3/', filename=f'{title}.3gpp')
    audio=f'mp3/{title}.3gpp'
    list.append(audio)
    if voice.is_playing():
        return await(ctx.send(f'Download {title} ok,Queued!'))
    else:
    song_queue.pop()
    voice.play(FFmpegPCMAudio(audio), after=lambda e: play_next(ctx))
@bot.command()
async def add(ctx, a:eval,b:eval):
    await ctx.send(a+b)
@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
@bot.command()
async def repeat(ctx, title, n):
    channel = ctx.message.author.voice.channel
    n=int(n)
    voice = get(bot.voice_clients, guild=ctx.guild)
    audio=f'mp3/{title}.3gpp'
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    msg = await ctx.send(f'Started playing video {n} times')
    voice.play(FFmpegPCMAudio(audio), after=lambda e: play_repeat(ctx, audio, msg, n-1))
    voice.is_playing()
@bot.command(aliases=['p','newplay','np'])
async def play(ctx, song):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    audio=f'mp3/{song}.3gpp'
    song_queue.append(audio)
    if voice.is_playing():
        return await(ctx.send(f'{song} Queued!'))
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    song_queue.pop()
    voice.play(FFmpegPCMAudio(audio), after=lambda e: play_next(ctx))

@bot.command(aliases=['q'])
async def Queue(ctx):
    stringa=""
    for x in song_queue:
        stringa+=x[4:-5]+"\n"
    await ctx.send(stringa)@bot.command()
async def multiply(ctx, a: eval, b: eval):
    await ctx.send(a*b)

@bot.command()
async def greet(ctx):
    await ctx.send(":smiley: :wave: Hello, there!")

@bot.command()
async def cat(ctx):
    await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")
@bot.command()
async def jwalk(ctx):
    mypath = "mp3/"
    files = os.listdir(mypath)
    x=""
    for f in files:
      x+=f[:-5]+"\n"
    await ctx.send(x)
@bot.command()
async def info(ctx):
    embed = discord.Embed(title="enlinBot", description="嬰靈會唱歌", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="王蟲四竄北南")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite this bot to their server
    embed.add_field(name="Invite", value="[Invitelink]https://discord.com/api/oauth2/authorize?client_id=944498354530942976&permissions=8&scope=bot")

    await ctx.send(embed=embed)
bot.remove_command('help')
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="nice bot", description="A Very Nice bot. List of commands are:", color=0xeee657)
    embed.add_field(name="=play song",value="play song or queue while playing(=p,=np)",inline=False)
    embed.add_field(name="=add X Y", value="Gives the addition of **X** and **Y**", inline=False)
    embed.add_field(name="=multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
    embed.add_field(name="=greet", value="Gives a nice greet message", inline=False)
    embed.add_field(name="=cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
    embed.add_field(name="=info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="=jwalk", value="列出免下載清單", inline=False)
    embed.add_field(name="=help", value="Gives this message", inline=False)
    embed.add_field(name="=Queue", value="Show Queued(=q)", inline=False)
    await ctx.send(embed=embed)
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)