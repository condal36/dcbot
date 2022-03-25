#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/19 下午 07:27
# @Author : condal36
# @Site :
# @Version: v1.0.1.3
# @File : enlinebot_command.py
# @Software: PyCharm
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from asyncio import run_coroutine_threadsafe as rct
from pytube import YouTube
import asyncio

song_queue=[]
HelpMessage=''
load_dotenv()
TOKEN = os.getenv('DISCORD_TEST')
bot = discord.Bot(command_prefix='=')      
guilds_id=[]
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
@bot.slash_command(guild_ids=guilds_id,aliases=['stop'])
async def stop_play(ctx):
    if not 'dj' in [y.name.lower() for y in ctx.message.author.roles]:
        return
    """ Skip the song currently playing. """
    voice=get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
@bot.slash_command(guild_ids=guilds_id,aliases=['qn','insert','cutin'])
async def cutinsong(ctx,title):
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
      return await(ctx.respond(f'Isn\'t Played!'))

@bot.slash_command(guild_ids=guilds_id,aliases=['skip'])
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
@bot.slash_command(guild_ids=guilds_id,aliases=['skip2'])
async def skip_song_to(ctx,n):
    if not 'dj' in [y.name.lower() for y in ctx.message.author.roles]:
        return
    n=int(n)
    if(n>=len(song_queue)):
        return await(ctx.respond('Invalid input'))
    i=1;
    while(i<n):
        i+=1
        song_queue.pop(0)
    """ Skip the song currently playing. """
    voice=get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
        voice.play(FFmpegPCMAudio(song_queue(0)),after=lambda e: play_next(ctx))

@bot.slash_command(guild_ids=guilds_id)
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
        await(ctx.respond(f'Download {title} ok,Queued!'))
    else:
        await(ctx.respond(f'Download {title} ok, start to play!'))
        song_queue.pop(0)
        voice.play(FFmpegPCMAudio(audio), after=lambda e: play_next(ctx))

@bot.slash_command(guild_ids=guilds_id,pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.respond("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
@bot.slash_command(guild_ids=guilds_id)
async def repeat(ctx, title, n):
    channel = ctx.message.author.voice.channel
    n=int(n)
    voice = get(bot.voice_clients, guild=ctx.guild)
    audio=f'mp3/{title}.3gpp'
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    msg = await ctx.respond(f'Started playing video {n} times')
    voice.play(FFmpegPCMAudio(audio), after=lambda e: play_repeat(ctx, audio, msg, n-1))
    voice.is_playing()
@bot.slash_command(guild_ids=guilds_id,aliases=['p','newplay','np'])
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
        return await(ctx.respond(f'{song} Queued!'))
    else:
        song_queue.pop(0)
        voice.play(FFmpegPCMAudio(audio), after=lambda e: play_next(ctx))
@bot.slash_command(guild_ids=guilds_id,aliases=['aq'])
async def addqueue(ctx,*addque):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    print(addque)
    for StrSong in addque:
        song_queue.append(f'mp3/{StrSong}.3gpp')
        print(StrSong+"now queue is ")
        print(song_queue)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if voice.is_playing():
        return await(ctx.respond(f'SongList Queued!'))
    else:
        voice.play(FFmpegPCMAudio(song_queue.pop(0)), after=lambda e: play_next(ctx))
        return await(ctx.respond(f'SongList Played!'))
@bot.slash_command(guild_ids=guilds_id,aliases=['pl'])
async def addplaylist(ctx,playlist):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    for StrSong in ParameterSplit(playlist):
        song_queue.append(f'mp3/{StrSong}.3gpp')
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    if voice.is_playing():
        return await(ctx.respond(f'SongList Queued!'))
    else:
        voice.play(FFmpegPCMAudio(song_queue.pop(0)), after=lambda e: play_next(ctx))
        return await(ctx.respond(f'SongList Played!'))
@bot.slash_command(guild_ids=guilds_id,aliases=['q'])
async def showqueue(ctx):
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
        await ctx.respond(SongQueueList)
    else:
        await ctx.respond('Nothing')
@bot.slash_command(guild_ids=guilds_id,aliases=['rm'])
async def removequeue(ctx,n):
    n=int(n)-1
    if(n<0):
        await ctx.respond('invalid input')
    else:
    	if song_queue[n]:
            song_queue.pop(n)
    	else:
            await ctx.respond('Nothing at n!')

@bot.slash_command(guild_ids=guilds_id)
async def greet(ctx):
    await ctx.respond(":smiley: :wave: Hello, there!")

@bot.slash_command(guild_ids=guilds_id)
async def cat(ctx):
    await ctx.respond("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")
@bot.slash_command(guild_ids=guilds_id)
async def jwalk(ctx):
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
    for titlestring in titlelist:
        totaltile+=titlestring
    await ctx.respond(totaltile)
@bot.slash_command(guild_ids=guilds_id)
async def info(ctx):
    embed = discord.Embed(title="enlinBot", description="嬰靈會唱歌", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="王蟲四竄北南")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite this bot to their server
    embed.add_field(name="Invite", value="[Invitelink]https://discord.com/api/oauth2/authorize?client_id=944498354530942976&permissions=8&scope=bot")

    await ctx.respond(embed=embed)

@bot.slash_command(guild_ids=guilds_id)
async def hello(ctx):
    await ctx.respond("Hello!")

@bot.slash_command(guild_ids=guilds_id,)
async def helptest(ctx):
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
    await ctx.respond(HelpMessage)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)


