from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage

import argparse

import gigachat

parser = argparse.ArgumentParser(description='Filisia telegram bot')
parser.add_argument('-t', '--token', help='Filisia token file')
parser.add_argument('-a', '--auth', help='Filisia auth file')

args = parser.parse_args()

# token
try:
    with open(args.token, mode='r') as t_f:
        TOKEN = t_f.read().strip()
        bot = Bot(token=TOKEN)
        storage = MemoryStorage()
        dp = Dispatcher(bot, storage=storage)
except Exception as e:
    print('Token file error:', str(e))
    exit()


# auth
try:
    with open(args.auth, mode='r') as a_f:
        gigachat.authority = a_f.read().strip()
except Exception as e:
    print('Authority file error:', str(e))
    exit()