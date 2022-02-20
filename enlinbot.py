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

source = FFmpegPCMAudio(r'mp3/Sora no Kiseki the 3rd Evolution [BGM RIP] - Cry for your Eternity.3gpp')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD=os.getenv('DISCORD_GUILD')
client=discord.Client()

@client.event
async def on_ready():
    f'{client.user} is connected to the following guild:\n'
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})')
    game=discord.Game('機...油..好...難...喝...逼逼逼逼')
    await client.change_presence(status=discord.Status.idle, activity=game)
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')
    if '雞' in message.content.lower():
        await message.channel.send('母雞好可愛<3')
    if '胖' in message.content.lower():
        await message.channel.send('真的超胖')
    if '機器人' in message.content.lower():
        await message.channel.send('機...油..好...難...喝...逼逼逼逼')
@client.event
async def play(ctx):
    await ctx.channel.purge(limit=1)
    channel = ctx.author.voice.channel
    voice = get(client.bot.voice_clients, guild=ctx.guild)

    def repeat(guild, voice, audio):
        voice.play(audio, after=lambda e: repeat(guild, voice, audio))
        voice.is_playing()

    if channel and not voice.is_playing():
        audio = discord.FFmpegPCMAudio('audio.mp3')
        voice.play(audio, after=lambda e: repeat(ctx.guild, voice, audio))
        voice.is_playing()
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'你好啊 {member.name}, 歡迎來到島邊!'
    )
@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

client.run(TOKEN)