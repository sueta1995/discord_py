from discord.ext import commands
from discord.ext.commands import CommandNotFound
import discord
import os
import asyncio
import time

TOKEN = 'NjkzNDYxNzIwNjY4MzA3NTE5.Xn9ajg.Rnq9RPUYoXXzY214SBky4rrG-1k'
intents = discord.Intents(messages=True, guilds=True, members=True, guild_messages=True, )
bot = commands.Bot(intents=intents, command_prefix='!')


async def checkUpdate():
    while True:
        for ctgr in bot.guilds[0].categories:
            if ctgr.name == '🤖Бот':
                for v_ch in ctgr.voice_channels:
                    if len(v_ch.members) == 0:
                        f = open('user_channels.txt', encoding='utf-8').readlines()
                        for i in range(len(f)):
                            if int(f[i].split()[1]) == v_ch.id:
                                del f[i]
                        os.remove('user_channels.txt')
                        open('user_channels.txt', 'w', encoding='utf-8').writelines(f)
                        for t_ch in ctgr.text_channels:
                            if t_ch.name == '↓↓бот-комнаты↓↓':
                                await t_ch.send('**:information_source: Канал `' + v_ch.name + '` удален, так как в '
                                                                                               'него долгое время не '
                                                                                               'заходили!**')
                                await v_ch.delete()
        await asyncio.sleep(300)


@bot.event
async def on_ready():
    bot.loop.create_task(checkUpdate())
    print('[' + time.ctime() + '] Успешно подключен к серверу!')


@bot.event
async def on_message(msg):
    print('[' + time.ctime() + '] ' + '(#' + msg.channel.name + ') ' + str(msg.author) + ': ' + msg.content)
    f = open('logs.txt', encoding='utf-8').readlines()
    f.append('[' + time.ctime() + '] ' + '(#' + msg.channel.name + ') ' + str(msg.author) + ': ' + msg.content + '\n')
    os.remove('logs.txt')
    open('logs.txt', 'w', encoding='utf-8').writelines(f)
    if not msg.author.bot:
        isExist = False
        f = open('rating.txt').readlines()
        for i in range(len(f)):
            if f[i].split('\t')[1] == str(msg.author):
                f[i] = str(int(f[i].split('\t')[0]) + 1) + '\t' + f[i].split('\t')[1] + '\t\n'
                isExist = True
        if not isExist:
            f.append('1' + '\t' + str(msg.author) + '\t\n')
        os.remove('rating.txt')
        open('rating.txt', 'w', encoding='utf-8').writelines(f)

    await bot.process_commands(msg)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        print('[' + time.ctime() + '] Ignoring the command...')


@bot.command()
async def crt(ctx):
    if ctx.message.channel.name == '↓↓бот-комнаты↓↓':
        f, ch_author = open('user_channels.txt', encoding='utf-8').readlines(), False
        for user in f:
            if user.split()[0] == str(ctx.message.author):
                ch_author = True
        if len(ctx.message.content.split()) >= 2 and not ch_author:
            ch_name = ctx.message.content.split()
            del ch_name[0]
            ch_name, ch_exist = ' '.join(ch_name), False
            for ch in ctx.message.channel.category.voice_channels:
                if ch_name == ch.name:
                    ch_exist = True
            if ch_exist:
                await ctx.message.delete()
                await ctx.send('**:x: Канал с данным названием уже существует!**')
            else:
                await ctx.message.channel.category.create_voice_channel(name=ch_name)
                for ch in ctx.message.channel.category.voice_channels:
                    if ch_name == ch.name:
                        await ch.set_permissions(ctx.message.author, mute_members=True, deafen_members=True,
                                                 move_members=True, )
                await ctx.message.delete()
                await ctx.send('**:white_check_mark: Создан голосовой канал `' + ch_name + '`**.')
                f1 = open('user_channels.txt', 'w', encoding='utf-8')
                for ch in ctx.message.channel.category.voice_channels:
                    if ch.name == ch_name:
                        f.append(str(ctx.message.author) + ' ' + str(ch.id) + '\n')
                        f1.writelines(f)
        elif len(ctx.message.content.split()) >= 2 and ch_author:
            await ctx.send('**:x: Вы уже создали канал!**')
            await ctx.message.delete()
        else:
            await ctx.message.delete()
            await ctx.send('**:x: Неверные аргументы команды!**')


@bot.command()
async def dlt(ctx):
    if ctx.message.channel.name == '↓↓бот-комнаты↓↓':
        f, ch_author, ch_id = open('user_channels.txt', encoding='utf-8').readlines(), False, 0
        for user in f:
            if user.split()[0] == str(ctx.message.author):
                ch_author, ch_id = True, int(user.split()[1])
        if ch_author:
            ch_exist = False
            for ch in ctx.message.channel.category.voice_channels:
                if ch.id == ch_id:
                    ch_name = ''
                    await ch.delete()
                    for i in range(len(f)):
                        if f[i].split()[0] == str(ctx.message.author):
                            ch_name = ch.name
                            del f[i]
                    os.remove('user_channels.txt')
                    open('user_channels.txt', 'tw', encoding='utf-8').writelines(f)
                    await ctx.message.delete()
                    await ctx.send('**:white_check_mark: Удален голосовой канал `' + ch_name + '`**.')
        else:
            await ctx.message.delete()
            await ctx.send('**:x: Вы не создавали канал!**')


@bot.command()
async def rt(ctx):
    if ctx.message.channel.name == 'команды':
        f = open('rating.txt').readlines()
        f.sort()
        f.reverse()
        if len(f) < 3:
            await ctx.send('**:information_source: Невозможно получить список, так как он состоит из недостаточного '
                           'количества участников!**')
        else:
            await ctx.send('**:information_source: Список самых активных участников:\n\n:first_place: `'
                           + f[0].split('\t')[1]
                           + '` - `' + f[0].split('\t')[0] + '` сообщений' + '\n\n:second_place: `' + f[1].split('\t')[
                               1]
                           + '` - `' + f[1].split('\t')[0] + '` сообщений' + '\n\n:third_place: `' + f[2].split('\t')[
                               1] +
                           '` - `' + f[2].split('\t')[0] + '` сообщений**')
        await ctx.message.delete()


@bot.command()
async def mt(ctx):
    user_admin = False
    for i in range(len(ctx.message.author.roles)):
        if ctx.message.author.roles[i].name == 'Старейшина' or ctx.message.author.roles[i].name == 'Верховный жрец':
            user_admin = True
    if user_admin and ctx.message.channel.name == 'команды' and len(ctx.message.content.split()) > 1:
        user_name, f = ctx.message.content.split(), open('blacklist.txt').readlines()
        del user_name[0]
        user_name, user_exist, user, user_bklt = ' '.join(user_name), False, None, False
        for member in ctx.guild.members:
            if str(member) == user_name:
                user_exist = True
                user = member
        for i in range(len(f)):
            if user_name in f[i]:
                user_bklt = True
        if not user_exist:
            await ctx.send('**:x: Данного пользователя нет на сервере!**')
        elif user_bklt:
            await ctx.send('**:x: Данный участник уже получил ограничение!**')
        elif user_exist and not user_bklt:
            for i in range(len(ctx.message.guild.text_channels)):
                await ctx.message.guild.text_channels[i].set_permissions(user, send_messages=False)
            await ctx.send('**:white_check_mark: Участник `' + str(user) + '` получил мут от администратора `' +
                           str(ctx.message.author) + '`**')
            f.append(str(user) + '\n')
            os.remove('blacklist.txt')
            open('blacklist.txt', 'w').writelines(f)
        await ctx.message.delete()


@bot.command()
async def nmt(ctx):
    user_admin = False
    for i in range(len(ctx.message.author.roles)):
        if ctx.message.author.roles[i].name == 'Старейшина' or ctx.message.author.roles[i].name == 'Верховный жрец':
            user_admin = True
    if user_admin and ctx.message.channel.name == 'команды' and len(ctx.message.content.split()) > 1:
        user_name, f = ctx.message.content.split(), open('blacklist.txt').readlines()
        del user_name[0]
        user_name, user_exist, user, user_bklt = ' '.join(user_name), False, None, False
        for member in ctx.guild.members:
            if str(member) == user_name:
                user_exist = True
                user = member
        for i in range(len(f)):
            if user_name in f[i]:
                user_bklt = True
                del f[i]
        if not user_exist:
            await ctx.send('**:x: Данного пользователя нет на сервере!**')
        elif not user_bklt:
            await ctx.send('**:x: Данный участник еще не получил ограничение!**')
        elif user_exist and user_bklt:
            for i in range(len(ctx.message.guild.text_channels)):
                await ctx.message.guild.text_channels[i].set_permissions(user, overwrite=None)
            await ctx.send('**:white_check_mark: Участник `' + str(user) + '` освобожден от мута администратором `' +
                           str(ctx.message.author) + '`**')
            os.remove('blacklist.txt')
            open('blacklist.txt', 'w').writelines(f)
        await ctx.message.delete()


bot.run(TOKEN)
