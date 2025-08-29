(function () {
  const ui = {
    prompt: document.getElementById('prompt'),
    send: document.getElementById('send'),
    status: document.getElementById('status'),
    historyBtn: document.getElementById('history'),
    pane: document.getElementById('historyPane'),
  };

  function addMsg(role, text) {
    const el = document.createElement('div');
    el.className = 'msg ' + (role === 'assistant' ? 'assistant' : 'user');
    el.textContent = text || '';
    ui.pane.appendChild(el);
    ui.pane.scrollTop = ui.pane.scrollHeight;
  }

  async function sendMsg() {
    const prompt = (ui.prompt.value || '').trim();
    if (!prompt) return;

    ui.status.textContent = 'Думаю…';
    ui.send.disabled = true;

    addMsg('user', prompt);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || ('HTTP ' + res.status));

      addMsg('assistant', data.reply || '');
      ui.status.textContent = '';
    } catch (e) {
      ui.status.textContent = 'Ошибка: ' + e.message;
    } finally {
      ui.send.disabled = false;
      ui.prompt.value = '';
      ui.prompt.focus();
    }
  }

  async function loadHistory() {
    ui.status.textContent = 'Загружаю историю…';
    try {
      const res = await fetch('/api/history/current');
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || ('HTTP ' + res.status));

      ui.pane.textContent = '';
      for (const m of data) {
        if (m.role === 'system') continue;
        addMsg(m.role, m.content);
      }
      ui.status.textContent = '';
    } catch (e) {
      ui.status.textContent = 'Ошибка: ' + e.message;
    }
  }

  ui.send.addEventListener('click', sendMsg);
  ui.prompt.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMsg();
    }
  });

  ui.historyBtn.addEventListener('click', loadHistory);
})();