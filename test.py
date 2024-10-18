# -*- coding: utf-8 -*-
from telethon import TelegramClient, events
from config import *
from addon import CustomMarkdown

client = TelegramClient("my_account", api_id=api_id, api_hash=api_hash, system_version='4.16.30-vxCUSTOM')


async def main():
    await client.start(phone=phone_number)
    client.parse_mode = CustomMarkdown()
    await client.send_message(1359387573, "Это пример использования касторного markdown:\n**Жирный**\n__Курсив__\n~~Зачеркнутый~~\n`Капирующийся`\n```Код```\n_~_Подчеркнутый_~_\n||Спойлер||\n[Ссылка](https://github.com)\n[❤️](emoji/10002345) - кастомная эмоция (нужен тг премиум)\n[Цитата](blockquote/True) - Скрывающаяся (наглядно с большим обьемом текста)\n[Цитата](blockquote/False) - Полная (наглядно с большим обьемом текста)")
    await client.run_until_disconnected()


client.loop.run_until_complete(main())
