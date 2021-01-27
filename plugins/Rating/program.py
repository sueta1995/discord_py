@bot.command()
async def rt(ctx):
    if ctx.message.channel.name == 'команды':
        f = open('plugins/Rating/rating.txt').readlines()
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


@bot.listen()
async def on_message(msg):
    if not msg.author.bot:
        isExist = False
        f = open('plugins/Rating/rating.txt').readlines()
        for i in range(len(f)):
            if f[i].split('\t')[1] == str(msg.author):
                f[i] = str(int(f[i].split('\t')[0]) + 1) + '\t' + f[i].split('\t')[1] + '\t\n'
                isExist = True
        if not isExist:
            f.append('1' + '\t' + str(msg.author) + '\t\n')
        os.remove('plugins/Rating/rating.txt')
        open('plugins/Rating/rating.txt', 'w', encoding='utf-8').writelines(f)