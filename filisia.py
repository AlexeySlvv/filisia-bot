from aiogram.utils import executor

from create_bot import dp

import client


async def on_startup(_):
    print('Filisia is ready to work')


if __name__ == '__main__':
    client.register_client_handlers()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
