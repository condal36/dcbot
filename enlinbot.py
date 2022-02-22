#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/19 下午 03:46
# @Author : condal36
# @Site : 
# @File : enlinbot.py
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

def next_play(ctx, source):
    if len(song_queue) >= 1:
        del song_queue[0]
        vc = get(bot.voice_clients, guild=ctx.guild)
        vc.play(discord.FFmpegPCMAudio(source=source, after=lambda e: next_play(ctx, source)))
        asyncio.run_coroutine_threadsafe(ctx.send("No more songs in queue."))

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
GUILD = os.getenv('DISCORD_GUILD')
song_queue = []

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    game = discord.Game('機...油..好...難...喝...逼逼逼逼')
    await bot.change_presence(status=discord.Status.idle, activity=game)
    print('------')
@bot.command(aliases=['g'])
async def grab(ctx,url,title):
    YouTube(url).streams.first().download(output_path='mp3/', filename=f'{title}.3gpp')
    await ctx.send(f'download {title} ok!')
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
    source = FFmpegPCMAudio(r'mp3/Sora no Kiseki the 3rd Evolution [BGM RIP] - Cry for your Eternity.3gpp')
    while True:
        voice.play(source)
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
@bot.command(aliases=['p'])
async def play(ctx, song):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    audio=f'mp3/{song}.3gpp'
    song_queue.append(audio)
    if voice.is_playing():
        return await(ctx.send('send to queue!'))
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    voice.play(FFmpegPCMAudio(audio), after=lambda e: play_next(ctx))

@bot.command()
async def queue(ctx):
    return await(ctx.send(song_queue))
@bot.command()
async def multiply(ctx, a: eval, b: eval):
    await ctx.send(a*b)

@bot.command()
async def greet(ctx):
    await ctx.send(":smiley: :wave: Hello, there!")

@bot.command()
async def cat(ctx):
    await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="島邊機器人", description="一個不起眼的島邊機器人", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="王蟲四竄北南")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite this bot to their server
    embed.add_field(name="Invite", value="[Invite link](DO NOT SUPPORT)")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="nice bot", description="A Very Nice bot. List of commands are:", color=0xeee657)

    embed.add_field(name="=add X Y", value="Gives the addition of **X** and **Y**", inline=False)
    embed.add_field(name="=multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
    embed.add_field(name="=greet", value="Gives a nice greet message", inline=False)
    embed.add_field(name="=cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
    embed.add_field(name="=info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="=help", value="Gives this message", inline=False)

    await ctx.send(embed=embed)
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)