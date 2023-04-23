<h1 align="center">HordeTalk - KoboldAI Horde Chatbot</h1>
<h3 align="center">Terminal chatbot. Powered by KoboldAI Horde.</h3>

<p align="center">The main script to run is <code>main.py</code>.</p>

<p align="center"><strong>Commands:</strong></p>
<ul align="center">
  <li>restart - Restart the conversation completely</li>
  <li>retry   - Remove the last User and Assistant messages, allowing you to enter new text.</li>
  <li>prompt  - Print the current prompt being sent to the AI</li>
  <li>exit    - Exit the chat</li>
</ul>

<p align="center">Profanity filters are on by default for <code>text_generation.py</code>, but can be disabled by simply replacing <code>return "The AI's response contained inappropriate content. Please rephrase your input.", True</code> with <code>return text, False</code>.</p>

<p align="center">Have fun!</p>
