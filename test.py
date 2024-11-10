# -*- coding: utf-8 -*-
from telethon import TelegramClient, events
from config import *
from addon import CustomMarkdown

client = TelegramClient("my_account", api_id=api_id, api_hash=api_hash, system_version='4.16.30-vxCUSTOM')

test_text = """Это пример использования касторного markdown:
<strong>Жирный</strong>
<em>Курсив</em>
<del>Зачеркнутый</del>
<code>Капирующийся</code>
<pre><code class='language-'>Код{}</code></pre>
<u>Подчеркнутый</u>
<spoiler>Спойлер</spoiler>
<a href="https://github.com/">Ссылка</a>
❤️ - кастомная эмоция (нужен тг премиум)


<blockquote collapsed="False"><u>class Descriptor:</u>
    <strong>def __get__(self, instance, owner):
 </strong>       <em>return instance._value</em>

    <strong>def __set__(self, instance, value):
 </strong>       if value &lt; 0:
            raise ValueError(&quot;Значение должно быть положительным!&quot;)
        instance._value = value

<u>class MyClass:</u>
    value = Descriptor()

    def __init__(self, value):
        self.value = value

obj = MyClass(10)
print(obj.value)  # 10
obj.value = -5    # Ошибка: Значение должно быть положительным</blockquote>


<blockquote collapsed="True"><u>class Descriptor:</u>
    <strong>def __get__(self, instance, owner):
 </strong>       <em>return instance._value</em>

    <strong>def __set__(self, instance, value):
 </strong>       if value &lt; 0:
            raise ValueError(&quot;Значение должно быть положительным!&quot;)
        instance._value = value

<u>class MyClass:</u>
    value = Descriptor()

    def __init__(self, value):
        self.value = value

obj = MyClass(10)
print(obj.value)  # 10
obj.value = -5    # Ошибка: Значение должно быть положительным</blockquote>"""


async def main():
    await client.start(phone=phone_number)
    client.parse_mode = CustomMarkdown()
    await client.send_message(1359387573, f"{test_text}", link_preview=False)


client.loop.run_until_complete(main())
