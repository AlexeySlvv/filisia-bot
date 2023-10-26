import time
import json
import os
from typing import Literal

from aiogram import types

from create_bot import dp
from gigachat import get_token, get_models, get_reply


t_key = Literal["access_token", "expires_at"]
m_key = Literal["id", "object", "owned_by"]


async def do_start(msg: types.Message):
    await msg.answer("Спросите меня о чём-нибудь.")


async def do_help(msg: types.Message):
    await msg.answer("Напишите свой вопрос. Я отвечу сразу как только освобожусь.")


# @dp.message_handler()
async def do_reply(msg: types.Message):
    if msg.text.startswith('/'):
        await msg.reply(text="Вопрос не должен начинаться с /")
    else:
        resp = "Извините, сейчас я занята и не могу ответить. Попробуйте позже."
        try:
            msg1 = await msg.reply(text="Уже пишу. \N{feather}")

            token_path = os.path.join("/tmp", ".token.json")
            token, expat = None, None
            token_exist = os.path.exists(token_path)
            if token_exist:
                with open(token_path, mode="r") as t_in:
                    t: dict[t_key, str] = json.loads(t_in.read())
                    token, expat = t.get("access_token"), t.get("expires_at")

            ts = time.time() * 1000
            time_expired = bool(expat) and int(ts) > int(expat)

            if not token_exist or time_expired or not token:
                t: dict[t_key, str] = get_token()
                token, expat = t.get("access_token"), t.get("expires_at")

                if token is None and expat is None:
                    raise Exception("No access_token and expires_at")

                with open(token_path, mode="w+") as t_out:
                    json.dump(t, t_out, ensure_ascii=False, indent=4)

            models: list[dict[m_key, str]] = get_models(token=token).get("data")
            if models:
                # just using the very first model
                model = models[0]["id"]
                answ = get_reply(token=token, model=model, prompt=msg.text)
                resp = answ["choices"][0]["message"]["content"] 

            await msg.reply(resp)
            await msg1.delete()
        except Exception as e:
            await msg.reply("Извините, случилась внезапная оказия.")
            await msg.answer(text=str(e))
        finally:
            if msg1:
                await msg1.delete()


def register_client_handlers():
    dp.register_message_handler(do_start, commands=['start'])
    dp.register_message_handler(do_help, commands=['help'])
    dp.register_message_handler(do_reply)
