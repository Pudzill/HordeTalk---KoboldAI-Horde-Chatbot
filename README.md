<h1 align="center">HordeTalk---KoboldAI-Horde-Chatbot</h1>
<h3 align="center">Terminal chatbot. Powered by KoboldAI Horde.</h3>

<p align="center">Parameters changeable in <code>main.py</code>:</p>
<ul align="center">
  <li>chat - True or False. if True, only use Pygmalion models. If False, never use Pygmalion models.</li>
  <li>prompt - The prompt. A string.</li>
  <li>printing - True or False. Debugging purposes. If True, prints everything, if False, prints nothing.</li>
  <li>timeout - How long until it timeouts. A number. Sometimes requests get stuck, so this is important.</li>
</ul>

<p align="center">Profanity filters are on by default for <code>text_generation.py</code>, but can be disabled by simply replacing <code>return "The AI's response contained inappropriate content. Please rephrase your input.", True</code> with <code>return text, False</code>.</p>

<p align="center">Have fun!</p>
