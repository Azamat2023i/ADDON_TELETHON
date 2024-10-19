# -*- coding: utf-8 -*-
from telethon import TelegramClient, events
from config import *
from addon import CustomMarkdown

client = TelegramClient("my_account", api_id=api_id, api_hash=api_hash, system_version='4.16.30-vxCUSTOM')

test_text = """_~_class Descriptor:_~_
    **def \__get\__(self, instance, owner):**
        __return instance._value__

    **def \__set\__(self, instance, value):**
        if value < 0:
            raise ValueError("Значение должно быть положительным!")
        instance._value = value

_~_class MyClass:_~_
    value = Descriptor()

    def \__init\__(self, value):
        self.value = value

obj = MyClass(10)
print(obj.value)  # 10
obj.value = -5    # Ошибка: Значение должно быть положительным"""


async def main():
    await client.start(phone=phone_number)
    client.parse_mode = CustomMarkdown()
    await client.send_message(1359387573, f"Это пример использования касторного markdown:\n**Жирный**\n__Курсив__\n~~Зачеркнутый~~\n`Капирующийся`\n```Код```\n_~_Подчеркнутый_~_\n||Спойлер||\n[Ссылка](https://github.com)\n[❤️](emoji/10002345) - кастомная эмоция (нужен тг премиум)\n\n\n[{test_text}](blockquote/False)\n\n\n[{test_text}](blockquote/True)")


client.loop.run_until_complete(main())
