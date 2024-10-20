<h1>Telethon Markdown Processing Addon</h1>

<p>This addon enhances the markdown processing capabilities of the Telethon library.</p>

<h2>Features</h2>
<ul>
    <li>Hidden text processing</li>
    <li>Text underlining</li>
    <li>Custom emojis</li>
    <li>Quotes (both collapsible and full)</li>
</ul>

<h2>Usage</h2>
<pre><code>from addon import CustomMarkdown
client.parse_mode = CustomMarkdown()</code></pre>

<p>To utilize the features, simply import <code>CustomMarkdown</code> from the <code>addon.py</code> file and set the client's parse mode as shown above.</p>
<p>An example of how to use this addon can be found in the <code>test.py</code> file.</p>

<h2>Installation</h2>
<p>You can include this addon in your project by cloning the repository or downloading the <code>addon.py</code> file directly. All additional libraries are installed together with Telethon.</p>

<h2>Python and Telethon library Version</h2>
<p>This addon has been developed using Python version <strong>3.9</strong>, haven't tried it with other versions.</p>
<p>This addon is compatible with Telethon version <strong>1.37.0</strong>, haven't tried it with other versions.</p>

<h2>Update Versions</h2>
<p>1.0.0:</p>
<ul>
    <li>The main functionality</li>
</ul>
<p>1.1.0:</p>
<ul>
    <li>Added processing of special characters in blocks (Link, Quote, Copyable text "Mono", Code).</li>
    <li>Added escaping of special characters "\".</li>
    <li>Minor bugs have been fixed.</li>
</ul>
