from discord.ext import commands
from discord.ext.commands import CommandNotFound
import discord
import os
import asyncio
import time

TOKEN = input('[' + time.ctime() + '] Введите токен: ')
intents = discord.Intents(messages=True, guilds=True, members=True, guild_messages=True, )
bot = commands.Bot(intents=intents, command_prefix='!')


@bot.event
async def on_ready():
    print('[' + time.ctime() + '] Успешно подключен к серверу!')


@bot.event
async def on_message(msg):
    print('[' + time.ctime() + '] ' + '(#' + msg.channel.name + ') ' + str(msg.author) + ': ' + msg.content)
    f = open('logs.txt', encoding='utf-8').readlines()
    f.append('[' + time.ctime() + '] ' + '(#' + msg.channel.name + ') ' + str(msg.author) + ': ' + msg.content + '\n')
    os.remove('logs.txt')
    open('logs.txt', 'w', encoding='utf-8').writelines(f)

    await bot.process_commands(msg)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        print('[' + time.ctime() + '] Ignoring the command...')


bot.run(TOKEN)
