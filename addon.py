# -*- coding: utf-8 -*-

import re
from telethon import types

from telethon.helpers import add_surrogate, del_surrogate, within_surrogate, strip_text
from telethon.tl import TLObject
from telethon.tl.types import (
    MessageEntityBold, MessageEntityItalic, MessageEntityCode,
    MessageEntityPre, MessageEntityTextUrl, MessageEntityMentionName,
    MessageEntityStrike, MessageEntityCustomEmoji, MessageEntitySpoiler,
    MessageEntityBlockquote, MessageEntityUnderline, MessageEntityHashtag,
    MessageEntityPre
)

DEFAULT_DELIMITERS = {
    '**': MessageEntityBold,
    '__': MessageEntityItalic,
    '~~': MessageEntityStrike,
    '`': MessageEntityCode,
    '```': MessageEntityPre,
    '_u_': MessageEntityUnderline,
    '||': MessageEntitySpoiler
}


DEFAULT_URL_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
DEFAULT_URL_FORMAT = '[{0}]({1})'


def overlap(a, b, x, y):
    return max(a, x) < min(b, y)


class CustomMarkdown:
    @staticmethod
    def parse(message, delimiters=None, url_re=None):
        if not message:
            return message, []

        if url_re is None:
            url_re = DEFAULT_URL_RE
        elif isinstance(url_re, str):
            url_re = re.compile(url_re)

        if not delimiters:
            if delimiters is not None:
                return message, []
            delimiters = DEFAULT_DELIMITERS

        # Build a regex to efficiently test all delimiters at once.
        # Note that the largest delimiter should go first, we don't
        # want ``` to be interpreted as a single back-tick in a code block.
        delim_re = re.compile('|'.join('({})'.format(re.escape(k))
                                       for k in sorted(delimiters, key=len, reverse=True)))

        # Cannot use a for loop because we need to skip some indices
        i = 0
        result = []

        # Work on byte level with the utf-16le encoding to get the offsets right.
        # The offset will just be half the index we're at.
        message = add_surrogate(message)
        while i < len(message):
            m = delim_re.match(message, pos=i)

            # Did we find some delimiter here at `i`?
            if m:
                delim = next(filter(None, m.groups()))

                # +1 to avoid matching right after (e.g. "****")
                end = message.find(delim, i + len(delim) + 1)

                # Did we find the earliest closing tag?
                if end != -1:

                    # Remove the delimiter from the string
                    message = ''.join((
                        message[:i],
                        message[i + len(delim):end],
                        message[end + len(delim):]
                    ))

                    # Check other affected entities
                    for ent in result:
                        # If the end is after our start, it is affected
                        if ent.offset + ent.length > i:
                            # If the old start is also before ours, it is fully enclosed
                            if ent.offset <= i:
                                ent.length -= len(delim) * 2
                            else:
                                ent.length -= len(delim)

                    # Append the found entity
                    ent = delimiters[delim]
                    if ent == MessageEntityPre:
                        result.append(ent(i, end - i - len(delim), ''))  # has 'lang'
                    else:
                        result.append(ent(i, end - i - len(delim)))

                    # No nested entities inside code blocks
                    if ent in (MessageEntityCode, MessageEntityPre):
                        i = end - len(delim)

                    continue

            elif url_re:
                m = url_re.match(message, pos=i)
                if m:
                    # Replace the whole match with only the inline URL text.
                    message = ''.join((
                        message[:m.start()],
                        m.group(1),
                        message[m.end():]
                    ))

                    delim_size = m.end() - m.start() - len(m.group())
                    for ent in result:
                        # If the end is after our start, it is affected
                        if ent.offset + ent.length > m.start():
                            ent.length -= delim_size
                    if del_surrogate(m.group(2)).startswith('emoji/'):
                        result.append(types.MessageEntityCustomEmoji(m.start(), len(m.group(1)), int(del_surrogate(m.group(2)).split('/')[1])))
                    elif del_surrogate(m.group(2)).startswith('blockquote/'):
                        result.append(types.MessageEntityBlockquote(m.start(), len(m.group(1)), bool(del_surrogate(m.group(2)).split('/')[1])))
                    else:
                        result.append(MessageEntityTextUrl(
                            offset=m.start(), length=len(m.group(1)),
                            url=del_surrogate(m.group(2))
                        ))
                    i += len(m.group(1))
                    continue

            i += 1

        message = strip_text(message, result)
        return del_surrogate(message), result

    @staticmethod
    def unparse(text, entities, delimiters=None, url_fmt=None):
        if not text or not entities:
            return text

        if not delimiters:
            if delimiters is not None:
                return text
            delimiters = DEFAULT_DELIMITERS

        if url_fmt is not None:
            warnings.warn('url_fmt is deprecated')  # since it complicates everything *a lot*

        if isinstance(entities, TLObject):
            entities = (entities,)

        text = add_surrogate(text)
        delimiters = {v: k for k, v in delimiters.items()}
        insert_at = []
        for i, entity in enumerate(entities):
            s = entity.offset
            e = entity.offset + entity.length
            delimiter = delimiters.get(type(entity), None)
            if delimiter:
                insert_at.append((s, i, delimiter))
                insert_at.append((e, -i, delimiter))
            else:
                url = None
                if isinstance(entity, MessageEntityTextUrl):
                    url = entity.url
                elif isinstance(entity, MessageEntityMentionName):
                    url = 'tg://user?id={}'.format(entity.user_id)
                elif isinstance(entity, MessageEntityCustomEmoji):
                    url = f'emoji/{entity.document_id}'
                elif isinstance(entity, MessageEntityBlockquote):
                    url = f'blockquote/{entity.collapsed}'
                if url:
                    insert_at.append((s, i, '['))
                    insert_at.append((e, -i, ']({})'.format(url)))

        insert_at.sort(key=lambda t: (t[0], t[1]))
        while insert_at:
            at, _, what = insert_at.pop()

            while within_surrogate(text, at):
                at += 1

            text = text[:at] + what + text[at:]

        return del_surrogate(text)