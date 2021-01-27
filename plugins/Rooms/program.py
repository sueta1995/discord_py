@bot.listen()
async def on_ready():
    bot.loop.create_task(checkUpdate())


async def checkUpdate():
    while True:
        for ctgr in bot.guilds[0].categories:
            if ctgr.name == '🤖Боты':
                for v_ch in ctgr.voice_channels:
                    if len(v_ch.members) == 0:
                        f = open('plugins/Rooms/user_channels.txt', encoding='utf-8').readlines()
                        for i in range(len(f)):
                            if int(f[i].split()[1]) == v_ch.id:
                                del f[i]
                        os.remove('plugins/Rooms/user_channels.txt')
                        open('plugins/Rooms/user_channels.txt', 'w', encoding='utf-8').writelines(f)
                        for t_ch in ctgr.text_channels:
                            if t_ch.name == '↓↓бот-комнаты↓↓':
                                await t_ch.send('**:information_source: Канал `' + v_ch.name + '` удален, так как в '
                                                                                               'него долгое время не '
                                                                                               'заходили!**')
                                await v_ch.delete()
        await asyncio.sleep(300)


@bot.command()
async def crt(ctx):
    if ctx.message.channel.name == '↓↓бот-комнаты↓↓':
        f, ch_author = open('plugins/Rooms/user_channels.txt', encoding='utf-8').readlines(), False
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
                f1 = open('plugins/Rooms/user_channels.txt', 'w', encoding='utf-8')
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
        f, ch_author, ch_id = open('plugins/Rooms/user_channels.txt', encoding='utf-8').readlines(), False, 0
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
                    os.remove('plugins/Rooms/user_channels.txt')
                    open('plugins/Rooms/user_channels.txt', 'tw', encoding='utf-8').writelines(f)
                    await ctx.message.delete()
                    await ctx.send('**:white_check_mark: Удален голосовой канал `' + ch_name + '`**.')
        else:
            await ctx.message.delete()
            await ctx.send('**:x: Вы не создавали канал!**')