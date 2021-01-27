import time
import os
import json

VERSION = '0.1.0'
COMMAND = None

print('[' + time.ctime() + '] DiscordCore v' + VERSION)
print('[' + time.ctime() + '] Введите -?, чтобы посмотреть доступный список команд')

while COMMAND != '-launch':
    if COMMAND == '-chckplgns':
        print('[' + time.ctime() + '] Плагины: ' + str(len(os.listdir('plugins'))))
        for file in os.listdir('plugins'):
            try:
                JSON_DATA = json.loads(open('plugins/' + file + '/config.json', 'r').read())
                print('[' + time.ctime() + '] Название: ' + JSON_DATA["Name"] + ', Автор: ' + JSON_DATA["Author"] +
                      ', Версия: ' + JSON_DATA['Version'])
                open('plugins/' + file + '/program.py', 'r').close()
                if JSON_DATA["CoreVersion"] == VERSION:
                    print('[' + time.ctime() + '] ' + JSON_DATA["Name"] + ' готов к использованию!')
                else:
                    print('[' + time.ctime() + '] Ошибка версий')

            except Exception:
                print('[' + time.ctime() + '] Ошибка: отсутствуют файлы в директрии ' + file + ' или неверный конфиг!')

    elif COMMAND == '-?':
        print('[' + time.ctime() + '] -chckplgns - проверить список доступных плагинов')
        print('[' + time.ctime() + '] -launch - запустить бота')

    else:
        if COMMAND is not None:
            print('[' + time.ctime() + '] Данной команды нет!')

    COMMAND = input('>> ').lower()

print('[' + time.ctime() + '] Запуск бота...')

xf = open('discord_core.pyw', encoding='utf-8').readlines()
for file in os.listdir('plugins'):
    try:
        JSON_DATA = json.loads(open('plugins/' + file + '/config.json', 'r').read())
        f = open('plugins/' + file + '/program.py', 'r', encoding='utf-8').readlines()
        if JSON_DATA["CoreVersion"] == VERSION:
            xf += f
            print('[' + time.ctime() + '] ' + JSON_DATA["Name"] + ' подключен!')
        else:
            print('[' + time.ctime() + '] Ошибка версий')

    except Exception:
        print('[' + time.ctime() + '] Ошибка: отсутствуют файлы в директрии ' + file + ' или неверный конфиг!')

i = 0
while i != len(xf):
    if 'bot.run(TOKEN)' in xf[i]:
        del xf[i]
    i += 1

xf.append('bot.run(TOKEN)')

exec('\n'.join(xf))
