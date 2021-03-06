#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/3/25 下午 00:53
# @Author : condal36
# @Site :
# @Version: v1.0.2.2
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
HelpMessage=''
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='=')      
songlist=[]

def updatesonglist():
    mypath = "mp3/"
    files = os.listdir(mypath)
    titlelist=[]
    totaltile=""
    x=""
    for f in files:
      x+=f[:-5]+','
      if(len(x)>50):
        x+='\n'
        titlelist.append(x)
        x=""
    titlelistlen=len(titlelist)-1
    for titlestring in titlelist:
        if(len(totaltile+titlestring)>=2000):
            songlist.append(totaltile)
            totaltile=""
        totaltile+=titlestring
        if(titlestring==titlelist[-1]):
            songlist.append(totaltile)
#mian..
def ParameterSplit(inputpara):
    return inputpara.split(",")
def play_next(ctx):
    if len(song_queue) >= 1:
        vc = get(bot.voice_clients, guild=ctx.guild)
        vc.play(FFmpegPCMAudio(song_queue.pop(0)), after=lambda e: play_next(ctx))
        vc.is_playing()
    else:
	    return
def play_repeat(ctx, audio, msg, n):    
    if 0!=n:
        voice = get(bot.voice_clients, guild=ctx.guild)
        rct(msg.edit(content=f'Finished playing the song, {n} more to go.'), bot.loop)
        voice.play(FFmpegPCMAudio(audio), after=lambda e: play_repeat(ctx, audio, msg, n-1))
        voice.is_playing()
    else:
        rct(msg.delete(), bot.loop)


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
    if not 'dj' in [y.name.lower() for y in ctx.message.author.roles]:
        return
    """ Skip the song currently playing. """
    voice=get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
@bot.command(aliases=['qn','insert'])
async def QueueNext(ctx,title):
    if not 'dj' in [y.name.lower() for y in ctx.message.author.roles]:
        return
    audio=f'mp3/{title}.3gpp'
    voice=get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
      if not song_queue:
        song_queue.append(audio)
      else:
        song_queue.insert(0,audio)
    else:
      return await(ctx.send(f'Isn\'t Played!'))

@bot.command(aliases=['skip'])
async def skip_song(ctx):
    if not 'dj' in [y.name.lower() for y in ctx.message.author.roles]:
        return
    print(f"Before Skip Queue is {song_queue}")
    """ Skip the song currently playing. """
    voice=get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
        voice.play(FFmpegPCMAudio(song_queue(0)),after=lambda e: play_next(ctx))
    print(f"After Skip Queue is {song_queue}")
@bot.command(aliases=['skip2'])
async def skip_song_to(ctx,n):
    if not 'dj' in [y.name.lower() for y in ctx.message.author.roles]:
        return
    n=int(n)
    if(n>=len(song_queue)):
        return await(ctx.send('Invalid input'))
    i=1;
    while(i<n):
        i+=1
        song_queue.pop(0)
    """ Skip the song currently playing. """
    voice=get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
        voice.play(FFmpegPCMAudio(song_queue(0)),after=lambda e: play_next(ctx))

@bot.command(aliases=['g'])
async def grab(ctx,url,title):
    YouTube(url).streams.first().download(output_path='mp3/', filename=f'{title}.3gpp')
    audio=f'mp3/{title}.3gpp'
    voice=get(bot.voice_clients, guild=ctx.guild)
    song_queue.append(audio)
    channel = ctx.message.author.voice.channel
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if voice.is_playing():
        await(ctx.send(f'Download {title} ok,Queued!'))
    else:
        await(ctx.send(f'Download {title} ok, start to play!'))
        song_queue.pop(0)
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
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if voice.is_playing():
        return await(ctx.send(f'{song} Queued!'))
    else:
        song_queue.pop(0)
        voice.play(FFmpegPCMAudio(audio), after=lambda e: play_next(ctx))
@bot.command(aliases=['aq'])
async def AddQueue(ctx,*AddQue):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    print(AddQue)
    for StrSong in AddQue:
        song_queue.append(f'mp3/{StrSong}.3gpp')
        print(StrSong+"now queue is ")
        print(song_queue)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if voice.is_playing():
        return await(ctx.send(f'SongList Queued!'))
    else:
        voice.play(FFmpegPCMAudio(song_queue.pop(0)), after=lambda e: play_next(ctx))
        return await(ctx.send(f'SongList Played!'))
@bot.command(aliases=['pl'])
async def AddPlayList(ctx,playlist):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    for StrSong in ParameterSplit(playlist):
        song_queue.append(f'mp3/{StrSong}.3gpp')
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if voice.is_playing():
        return await(ctx.send(f'SongList Queued!'))
    else:
        voice.play(FFmpegPCMAudio(song_queue.pop(0)), after=lambda e: play_next(ctx))
        return await(ctx.send(f'SongList Played!'))
@bot.command(aliases=['q'])
async def Queue(ctx):
    SongQueueList=""
    if song_queue:
        tmp=0
        for x in song_queue:
            if (tmp % 5)==4:
                tmp += 1
                SongQueueList+=f"{tmp}."+x[4:-5]+"\n"
            else:
                tmp += 1
                SongQueueList+=f"{tmp}."+x[4:-5]+"  "
        await ctx.send(SongQueueList)
    else:
        await ctx.send('Nothing')
@bot.command(aliases=['rm'])
async def Remove(ctx,n):
    n=int(n)-1
    if(n<0):
        await ctx.send('invalid input')
    else:
    	if song_queue[n]:
            song_queue.pop(n)
    	else:
            await ctx.send('Nothing at n!')
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
async def jwalk(ctx):
    updatesonglist()
    global songlist
    while songlist:
        await ctx.send(songlist.pop(0))
    
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
    HelpMessage = '```'
    HelpMessage +='\n=greet     :  Gives a nice greet message  Example:=greet'
    HelpMessage +='\n=cat       :  Gives a cute cat gif to lighten up the mood.  Example:=cat'
    HelpMessage +='\n=info      :  Gives a little info about the bot  Example:=info'
    HelpMessage +='\n=grabe     :  Grabe a song(=g)  Example:=g url songTitle'
    HelpMessage +='\n=play      :  play song or queue while playing(=p,=np)  Example:=play song'
    HelpMessage +='\n=jwalk     :  列出免下載清單  Example:=jwalk'
    HelpMessage +='\n=stop      :  Stop Singing(DJ role)  Example:=stop'
    HelpMessage +='\n=skip      :  Skip nowplaying song(DJ role)  Example:=skip'
    HelpMessage +='\n=skip2     :  Skip nowplaying song to n(DJ role)  Example:=skip2 n'
    HelpMessage +='\n=help      :  Gives this message  Example:=help'
    HelpMessage +='\n=Queue     :  Show Queued(=q)  Example:=Queue'
    HelpMessage +='\n=AddQueue  :  Add Queued(=aq)  Example:=AddQueue song1 song2 ...'
    HelpMessage +='\n=Remove    :  Remove the n\'th song in the Queue(=rm)  Example:=Remove n'
    HelpMessage +='\n=QueueNext    :  Play the song after now playing(=qn)(DJ role)  Example:=QueueNext song'
    HelpMessage += '```'
    await ctx.send(HelpMessage)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)