(function () {
  const ui = {
    prompt: document.getElementById('prompt'),
    send: document.getElementById('send'),
    status: document.getElementById('status'),
    out: document.getElementById('out'),
  };
  const DEFAULT_PROVIDER = 'openai';

  async function sendMsg() {
    const prompt = (ui.prompt.value || '').trim();
    if (!prompt) return;

    ui.out.textContent = '';
    ui.status.textContent = 'Думаю…';
    ui.send.disabled = true;

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, provider: DEFAULT_PROVIDER })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || ('HTTP ' + res.status));
      ui.out.textContent = data.reply || '';
      ui.status.textContent = '';
    } catch (e) {
      ui.status.textContent = 'Ошибка: ' + e.message;
    } finally {
      ui.send.disabled = false;
      ui.prompt.value = '';
    }
  }

  ui.send.addEventListener('click', sendMsg);
  ui.prompt.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMsg();
    }
  });
})();