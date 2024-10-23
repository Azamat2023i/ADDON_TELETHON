# -*- coding: utf-8 -*-

import re
from telethon import types
import warnings
from telethon.helpers import add_surrogate, del_surrogate, within_surrogate, strip_text
from telethon.tl import TLObject
from telethon.tl.types import (
    MessageEntityBold, MessageEntityItalic, MessageEntityCode,
    MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName,
    MessageEntityStrike, MessageEntityCustomEmoji, MessageEntitySpoiler,
    MessageEntityBlockquote, MessageEntityUnderline
)

DEFAULT_DELIMITERS = {
    '**': MessageEntityBold,
    '__': MessageEntityItalic,
    '~~': MessageEntityStrike,
    '```': MessageEntityPre,
    '`': MessageEntityCode,
    '_~_': MessageEntityUnderline,
    '||': MessageEntitySpoiler
}


DEFAULT_URL_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
DEFAULT_URL_FORMAT = '[{0}]({1})'


def overlap(a, b, x, y):
    return max(a, x) < min(b, y)


class CustomMarkdown:
    @staticmethod
    def parse(message, delimiters=None, delimiters_backslash=None, url_re=None, l=0):
        if not message:
            return message, []

        if url_re is None:
            url_re = DEFAULT_URL_RE  # Если регулярное выражение для URL не задано, используем значение по умолчанию.
        elif isinstance(url_re, str):
            url_re = re.compile(url_re)  # Компилируем строку в регулярное выражение.

        if not delimiters:
            if delimiters is not None:
                return message, []  # Если разделители не заданы, возвращаем сообщение без изменений и пустой список.
            delimiters = DEFAULT_DELIMITERS  # Используем разделители по умолчанию.
            delimiters_backslash = {f'\\{key}': value for key, value in DEFAULT_DELIMITERS.items()}

        # Создаем регулярное выражение для эффективной проверки всех разделителей сразу.
        # Заметьте, что самый длинный разделитель должен быть первым, чтобы избежать неправильного разбора.
        delim_re = re.compile(r'(?<!\\)(' + '|'.join(re.escape(k) for k in sorted(delimiters, key=len, reverse=True)) + r')')
        delim_backslash_re = re.compile('|'.join('({})'.format(re.escape(k)) for k in sorted(delimiters_backslash, key=len, reverse=True)))

        # Не можем использовать цикл for, так как нужно пропустить некоторые индексы.
        result = []
        # Работаем на уровне байтов с кодировкой utf-16le для правильного получения смещений.
        # Смещение будет просто половиной индекса, который мы находим.
        message = add_surrogate(message)

        i = 0
        while i < len(message):
            m = delim_re.match(message, pos=i)  # Проверяем, нашли ли мы разделитель в позиции i.
            ml = delim_backslash_re.match(message, pos=i)  # Проверяем, нашли ли мы разделитель с \ в позиции i.
            mg = url_re.match(message, pos=i)  # Проверяем наличие URL в сообщении.
            if ml:
                delim = next(filter(None, ml.groups()))

                message = delim[1:].join((
                    message[:i],
                    message[i + len(delim):]
                ))

                i += len(delim)
            elif m:
                delim = next(filter(None, m.groups()))  # Получаем найденный разделитель.
                # +1 чтобы избежать совпадения сразу после (например, "****").
                end = message.find(delim, i + len(delim) + 1)  # Ищем ближайший закрывающий тег.
                # Если нашли закрывающий тег.
                if end != -1:
                    # Удаляем разделитель из строки.
                    message = ''.join((
                        message[:i],
                        message[i + len(delim):end],
                        message[end + len(delim):]
                    ))

                    # Проверяем другие затронутые сущности.
                    for ent in result:
                        # Если конец после нашего начала, это затронуто.
                        if ent.offset + ent.length > i:
                            # Если старое начало также перед нашим, оно полностью заключено.
                            if ent.offset <= i:
                                ent.length -= len(delim) * 2  # Уменьшаем длину сущности.
                            else:
                                ent.length -= len(delim)

                    # Добавляем найденную сущность.
                    ent = delimiters[delim]
                    if ent == MessageEntityPre:
                        result.append(ent(i, end - i - len(delim), ''))  # У сущности 'lang'.
                    else:
                        result.append(ent(i, end - i - len(delim)))  # Нет вложенных сущностей внутри блоков кода.
                    continue
            elif mg:
                # Заменяем всё совпадение только текстом URL.
                message = ''.join((
                    message[:mg.start()],
                    mg.group(1),
                    message[mg.end():]
                ))

                delim_size = mg.end() - mg.start() - len(mg.group())  # Вычисляем размер удаляемого текста.

                for ent in result:
                    # Если конец после нашего начала, это затронуто.
                    if ent.offset + ent.length > mg.start():
                        ent.length -= delim_size  # Уменьшаем длину сущности.

                if del_surrogate(mg.group(2)).startswith('emoji/'):
                    result.append(types.MessageEntityCustomEmoji(mg.start(), len(mg.group(1)),
                                                                 int(del_surrogate(mg.group(2)).split('/')[1])))
                elif del_surrogate(mg.group(2)).startswith('blockquote/'):
                    if str(del_surrogate(mg.group(2)).split('/')[1]) == 'True':
                        result.append(types.MessageEntityBlockquote(mg.start(), len(mg.group(1)), True))
                    else:
                        result.append(types.MessageEntityBlockquote(mg.start(), len(mg.group(1)), False))
                else:
                    result.append(MessageEntityTextUrl(
                        offset=mg.start(),
                        length=len(mg.group(1)),
                        url=del_surrogate(mg.group(2))
                    ))
                continue
            i += 1  # Переходим к следующему символу в сообщении.

        message = strip_text(message, result)  # Очищаем текст сообщения от лишнего.
        return del_surrogate(message), result  # Возвращаем обработанное сообщение и список сущностей.

    @staticmethod
    def unparse(text, entities, delimiters=None, url_fmt=None, count_replacements=0):
        # Проверяем, есть ли текст и сущности
        if not text or not entities:
            return text  # Если нет текста или сущностей, возвращаем текст как есть

        # Проверяем, заданы ли разделители
        if not delimiters:
            if delimiters is not None:
                return text  # Если разделители не заданы, но переданы явно, возвращаем текст
            delimiters = DEFAULT_DELIMITERS  # Устанавливаем разделители по умолчанию

        # Предупреждаем, что параметр url_fmt устарел
        if url_fmt is not None:
            warnings.warn('url_fmt is deprecated')  # так как это усложняет все *очень сильно*

        # Приводим сущности к кортежу, если это объект TLObject
        if isinstance(entities, TLObject):
            entities = (entities,)

        # Добавляем суррогаты в текст
        text = add_surrogate(text)

        # Переворачиваем словарь разделителей для удобства
        delimiters = {v: k for k, v in delimiters.items()}
        insert_at = []  # Список для хранения позиций вставки

        for i, entity in enumerate(entities):
            s = entity.offset + count_replacements  # Начальная позиция сущности
            e = entity.offset + entity.length + count_replacements  # Конечная позиция сущности

            text = del_surrogate(text)
            ll = 0
            for delimiter in DEFAULT_DELIMITERS.keys():
                count = text[s:e].count(delimiter)
                count_replacements += count  # Добавляем к общему счетчику
                ll += count
                text_sl = text[s:e].replace(delimiter, '\\' + delimiter)
                text = text[:s] + text_sl + text[e:]
            e += ll
            text = add_surrogate(text)

            delimiter = delimiters.get(type(entity), None)  # Получаем разделитель для данной сущности

            if delimiter:
                insert_at.append((s, i, delimiter))  # Добавляем позицию начала разделителя
                insert_at.append((e, -i, delimiter))  # Добавляем позицию конца разделителя
            else:
                url = None  # Инициализация переменной URL
                if isinstance(entity, MessageEntityTextUrl):
                    url = entity.url  # Если это URL-сущность, получаем URL
                elif isinstance(entity, MessageEntityMentionName):
                    url = 'tg://user?id={}'.format(entity.user_id)  # Если это упоминание пользователя, формируем URL
                elif isinstance(entity, MessageEntityCustomEmoji):
                    url = f'emoji/{entity.document_id}'  # Для пользовательского эмодзи формируем URL
                elif isinstance(entity, MessageEntityBlockquote):
                    url = f'blockquote/{entity.collapsed}'  # Для блока цитаты формируем URL

                if url:
                    insert_at.append((s, i, '['))  # Добавляем открывающую скобку для ссылки
                    insert_at.append((e, -i, ']({})'.format(url)))  # Добавляем закрывающую скобку с URL

        insert_at.sort(key=lambda t: (t[0], t[1]))  # Сортируем позиции вставки

        while insert_at:
            at, _, what = insert_at.pop()  # Извлекаем последнюю позицию вставки
            while within_surrogate(text, at):  # Проверяем на наличие суррогатов
                at += 1  # Если есть суррогаты, сдвигаем позицию

            text = text[:at] + what + text[at:]  # Вставляем нужный текст в позицию
        return del_surrogate(text)  # Убираем суррогаты из текста и возвращаем результат
