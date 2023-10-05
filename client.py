from aiogram import types
import g4f

from create_bot import dp

#from openaihosted import Completion

async def do_start(msg: types.Message):
    await msg.answer("Спросите меня о чём-нибудь.")


async def do_help(msg: types.Message):
    await msg.answer("Напишите свой вопрос. Я отвечу сразу как только освобожусь.")


# @dp.message_handler()
async def do_reply(msg: types.Message):
    if msg.text.startswith('/'):
        await msg.reply(text="Вопрос не должен начинаться с /")

    try:
        msg1 = await msg.reply(text="Уже пишу. \N{feather}")
        resp = await g4f.ChatCompletion.create_async(model='gpt-3.5-turbo', provider=g4f.Provider.FreeGpt, messages=[{"role": "user", "content": msg.text}])
        await msg.reply(resp)
        await msg1.delete()
    except Exception as e:
        await msg.reply(text="Ошибка: "+str(e))


def register_client_handlers():
    dp.register_message_handler(do_start, commands=['start'])
    dp.register_message_handler(do_help, commands=['help'])
    dp.register_message_handler(do_reply)
