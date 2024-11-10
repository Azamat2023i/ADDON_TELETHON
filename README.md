<h1>Telethon HTML Processing Addon (English)</h1>

<p>This addon enhances the HTML processing capabilities of the Telethon library.</p>

<h2>Features</h2>
<ul>
    <li>Hidden text processing</li>
    <li>Text underlining</li>
    <li>Custom emojis</li>
    <li>Quotes (both collapsible and full)</li>
</ul>

<h2>Usage</h2>
<pre><code>from addon import CustomHTML
client.parse_mode = CustomHTML()</code></pre>

<p>To utilize the features, simply import <code>CustomHTML</code> from the <code>addon.py</code> file and set the client's parse mode as shown above.</p>
<p>An example of how to use this addon can be found in the <code>test.py</code> file.</p>

<h2>Installation</h2>
<p>You can include this addon in your project by cloning the repository or downloading the <code>addon.py</code> file directly. All additional libraries are installed together with Telethon.</p>

<h2>Python and Telethon library Version</h2>
<p>This addon has been developed using Python version <strong>3.9</strong>, haven't tried it with other versions.</p>
<p>This addon is compatible with Telethon version <strong>1.37.0</strong>, haven't tried it with other versions.</p>

<h2>Update Versions</h2>
<s><p>1.0.0:</p>
<ul>
    <li>The main functionality</li>
</ul>
<p>1.1.0:</p>
<ul>
    <li>Added processing of special characters in blocks (Link, Quote, Copyable text "Mono", Code).</li>
    <li>Added escaping of special characters "\".</li>
    <li>Minor bugs have been fixed.</li>
</ul></s>
<p>2.0.0:</p>
<ul>
    <li>Total change, changed Markdown to HTML</li>
</ul>
<br><br>
<h1>Дополнение для обработки HTML в Telethon (Русский)</h1>

<p>Это дополнение улучшает возможности обработки HTML в библиотеке Telethon.</p>

<h2>Особенности</h2>
<ul>
    <li>Обработка скрытого текста</li>
    <li>Подчеркивание текста</li>
    <li>Пользовательские эмодзи</li>
    <li>Цитаты (как сворачиваемые, так и полные)</li>
</ul>

<h2>Использование</h2>
<pre><code>from addon import CustomHTML
client.parse_mode = CustomHTML()</code></pre>

<p>Чтобы использовать функции, просто импортируйте <code>CustomHTML</code> из файла <code>addon.py</code> и установите режим разбора клиента, как показано выше.</p>
<p>Пример использования этого дополнения можно найти в файле <code>test.py</code>.</p>

<h2>Установка</h2>
<p>Вы можете включить это дополнение в свой проект, клонировав репозиторий или скачав файл <code>addon.py</code> напрямую. Все дополнительные библиотеки устанавливаются вместе с Telethon.</p>

<h2>Версия Python и библиотеки Telethon</h2>
<p>Это дополнение было разработано с использованием версии Python <strong>3.9</strong>, с другими версиями не проверялось.</p>
<p>Это дополнение совместимо с версией Telethon <strong>1.37.0</strong>, с другими версиями не проверялось.</p>

<h2>Обновления версий</h2>
<s><p>1.0.0:</p>
<ul>
    <li>Основная функциональность</li>
</ul>
<p>1.1.0:</p>
<ul>
    <li>Добавлена обработка специальных символов в блоках (Ссылка, Цитата, Копируемый текст "Моно", Код).</li>
    <li>Добавлено экранирование специальных символов "\".</li>
    <li>Исправлены мелкие ошибки.</li>
</ul></s>
<p>2.0.0:</p>
<ul>
    <li>Татальное изменение, изменен Markdown в HTML</li>
</ul>
