(() => {
  'use strict';

  /* Navigation: Hamburger-Menü (nur wenn JavaScript aktiv ist) */
  const toggle = document.querySelector('.nav-toggle');
  const menu = document.getElementById('hauptmenue');
  if (toggle && menu) {
    const setOpen = (open) => {
      toggle.setAttribute('aria-expanded', String(open));
      menu.classList.toggle('is-open', open);
    };
    toggle.addEventListener('click', () => {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        toggle.focus();
      }
    });
  }

  /* Arbeitszeit Rechner */
  const form = document.getElementById('calc-form');
  if (!form) return;

  const el = {
    start: document.getElementById('calc-start'),
    end: document.getElementById('calc-end'),
    pause: document.getElementById('calc-pause'),
    soll: document.getElementById('calc-soll'),
    net: document.getElementById('res-net'),
    dec: document.getElementById('res-dec'),
    gross: document.getElementById('res-gross'),
    diff: document.getElementById('res-diff'),
    msg: document.getElementById('res-msg'),
    live: document.getElementById('res-live'),
  };

  const MINUS = '−';
  const decimalFormat = new Intl.NumberFormat('de-DE', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

  const toMinutes = (value) => {
    const [h, m] = value.split(':').map(Number);
    return h * 60 + m;
  };

  const formatHM = (minutes) => {
    const sign = minutes < 0 ? MINUS : '';
    const abs = Math.abs(Math.round(minutes));
    return `${sign}${Math.floor(abs / 60)}:${String(abs % 60).padStart(2, '0')} Std.`;
  };

  const formatDecimal = (minutes) => `${decimalFormat.format(minutes / 60)} Std.`;

  const setMessage = (text, state) => {
    el.msg.textContent = text;
    el.msg.className = 'calc__msg' + (state ? ` is-${state}` : '');
  };

  const clearResults = () => {
    el.net.textContent = el.dec.textContent = el.gross.textContent = el.diff.textContent = '–';
    el.live.textContent = '';
  };

  let liveTimer;
  const announce = (text) => {
    clearTimeout(liveTimer);
    liveTimer = setTimeout(() => { el.live.textContent = text; }, 600);
  };

  /* § 4 ArbZG: mehr als 6 bis 9 Stunden Arbeitszeit -> mindestens 30 Minuten,
     mehr als 9 Stunden -> mindestens 45 Minuten Ruhepause. */
  const requiredBreak = (netMinutes) => {
    if (netMinutes > 9 * 60) return { minutes: 45, text: 'Bei mehr als neun Stunden Arbeitszeit sieht § 4 ArbZG mindestens 45 Minuten Ruhepause vor.' };
    if (netMinutes > 6 * 60) return { minutes: 30, text: 'Bei mehr als sechs Stunden Arbeitszeit sieht § 4 ArbZG mindestens 30 Minuten Ruhepause vor.' };
    return { minutes: 0, text: '' };
  };

  const compute = () => {
    if (!el.start.value || !el.end.value) {
      clearResults();
      setMessage('Bitte Arbeitsbeginn und Arbeitsende angeben.', 'error');
      return;
    }

    const pause = el.pause.value === '' ? 0 : el.pause.valueAsNumber;
    if (!Number.isFinite(pause) || pause < 0) {
      clearResults();
      setMessage('Bitte eine gültige Pause in Minuten angeben.', 'error');
      return;
    }

    const start = toMinutes(el.start.value);
    const end = toMinutes(el.end.value);
    if (start === end) {
      clearResults();
      setMessage('Arbeitsbeginn und Arbeitsende sind identisch.', 'error');
      return;
    }

    const overnight = end < start;
    const gross = overnight ? end + 1440 - start : end - start;
    if (pause > gross) {
      clearResults();
      setMessage('Die Pause ist länger als die Anwesenheitszeit.', 'error');
      return;
    }

    const net = gross - pause;
    el.net.textContent = formatHM(net);
    el.dec.textContent = formatDecimal(net);
    el.gross.textContent = formatHM(gross);

    const sollHours = el.soll.value === '' ? NaN : el.soll.valueAsNumber;
    let summary = `Nettoarbeitszeit ${formatHM(net)}, ${formatDecimal(net)}.`;
    if (Number.isFinite(sollHours) && sollHours >= 0) {
      const diff = net - Math.round(sollHours * 60);
      const label = diff > 0 ? 'Überstunden' : diff < 0 ? 'Minusstunden' : 'keine Abweichung';
      el.diff.textContent = `${diff > 0 ? '+' : ''}${formatHM(diff)}`;
      summary += ` Abweichung zur Soll-Arbeitszeit: ${formatHM(diff)} (${label}).`;
    } else {
      el.diff.textContent = '–';
    }

    const notes = [];
    if (overnight) notes.push('Arbeitsende am Folgetag angenommen.');
    const rule = requiredBreak(net);
    if (pause < rule.minutes) notes.push(`Hinweis: ${rule.text}`);
    setMessage(notes.join(' '), pause < rule.minutes ? 'warn' : '');
    announce(summary);
  };

  form.addEventListener('input', compute);
  form.addEventListener('change', compute);
  form.addEventListener('submit', (event) => event.preventDefault());
  form.addEventListener('reset', () => setTimeout(compute, 0));
  compute();
})();
