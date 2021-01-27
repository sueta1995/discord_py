@bot.command()
async def mt(ctx):
    user_admin = False
    for i in range(len(ctx.message.author.roles)):
        if ctx.message.author.roles[i].name == 'Старейшина' or ctx.message.author.roles[i].name == 'Верховный жрец':
            user_admin = True
    if user_admin and ctx.message.channel.name == 'команды' and len(ctx.message.content.split()) > 1:
        user_name, f = ctx.message.content.split(), open('plugins/MuteMember/blacklist.txt').readlines()
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
            os.remove('plugins/MuteMember/blacklist.txt')
            open('plugins/MuteMember/blacklist.txt', 'w').writelines(f)
        await ctx.message.delete()


@bot.command()
async def nmt(ctx):
    user_admin = False
    for i in range(len(ctx.message.author.roles)):
        if ctx.message.author.roles[i].name == 'Старейшина' or ctx.message.author.roles[i].name == 'Верховный жрец':
            user_admin = True
    if user_admin and ctx.message.channel.name == 'команды' and len(ctx.message.content.split()) > 1:
        user_name, f = ctx.message.content.split(), open('plugins/MuteMember/blacklist.txt').readlines()
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
            os.remove('plugins/MuteMember/blacklist.txt')
            open('plugins/MuteMember/blacklist.txt', 'w').writelines(f)
        await ctx.message.delete()