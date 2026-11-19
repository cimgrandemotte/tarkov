/** Navigation, dialogue, onglets et infobulles sur des contrôles HTML natifs. */
export function preferences(key, value) {
  try {
    const name = `tug:${key}`;
    if (value !== undefined) {
      const stored = String(value);
      localStorage.setItem(name, stored);
      return stored;
    }
    return localStorage.getItem(name);
  } catch { /* Le site reste utilisable quand le stockage est bloqué. */ }
  return null;
}

export function focusToHash(hash) {
  if (!hash || !hash.startsWith('#')) return false;
  let id;
  try { id = decodeURIComponent(hash.slice(1)); } catch { return false; }
  const dest = document.getElementById(id);
  if (!dest) return false;
  dest.focus({ preventScroll: true });
  dest.scrollIntoView({ block: 'start' });
  return true;
}

export function initNavigation() {
  const mobile = document.querySelector('[data-mobile-menu]');
  const summary = mobile?.querySelector('summary');
  const update = () => {
    const hash = location.hash || '#vue-ensemble';
    document.querySelectorAll('[data-nav-link]').forEach(link => {
      if (link.getAttribute('href') === hash) link.setAttribute('aria-current', 'location');
      else if (link.getAttribute('aria-current') === 'location') link.removeAttribute('aria-current');
    });
  };
  addEventListener('hashchange', update);
  update();
  document.addEventListener('click', event => {
    if (mobile?.open && (!mobile.contains(event.target) || event.target.closest('a'))) mobile.open = false;
  });
  document.addEventListener('keydown', event => {
    if (mobile?.open && event.key === 'Escape' && !document.querySelector('dialog[open]')) {
      mobile.open = false;
      if (mobile.contains(document.activeElement) || document.activeElement === document.body) summary?.focus();
    }
  });
  document.querySelector('[data-skip]')?.addEventListener('click', event => {
    if (focusToHash(event.currentTarget.getAttribute('href'))) event.preventDefault();
  });
}

export function initDialogs() {
  const drivers = new Map();
  for (const dialog of document.querySelectorAll('dialog[data-dialog]')) {
    if (typeof dialog.showModal !== 'function') continue;
    let opener;
    const desk = {
      open(from = document.activeElement) {
        if (dialog.open || document.querySelector('dialog[open]')) return false;
        opener = from;
        dialog.returnValue = '';
        dialog.showModal();
        dialog.querySelector('[data-dialog-focus]')?.focus();
        return true;
      },
      dismiss(value = '') { if (dialog.open) dialog.close(value); },
    };
    for (const trigger of document.querySelectorAll('[data-dialog-open]')) {
      if (trigger.dataset.dialogOpen !== dialog.id) continue;
      trigger.hidden = false;
      trigger.addEventListener('click', () => desk.open(trigger));
    }
    dialog.addEventListener('keydown', event => {
      if (event.key === 'Escape' && !event.isComposing) {
        event.preventDefault();
        desk.dismiss();
      }
      if (event.key !== 'Tab' || event.ctrlKey || event.metaKey || event.altKey) return;
      const controls = [...dialog.querySelectorAll('a[href],button,input,select,textarea,[tabindex]')].filter(node =>
        node.tabIndex >= 0 && !node.matches(':disabled') && node.getClientRects().length && getComputedStyle(node).visibility === 'visible');
      const first = controls[0];
      const last = controls.at(-1);
      if ((event.shiftKey && document.activeElement === first) || (!event.shiftKey && document.activeElement === last)) {
        event.preventDefault();
        (event.shiftKey ? last : first)?.focus();
      }
    });
    dialog.addEventListener('close', () => {
      if (dialog.returnValue === 'navigate') return;
      if (opener instanceof HTMLElement && opener.isConnected && !opener.hidden) opener.focus({ preventScroll: true });
    });
    let fromBackdrop = false;
    dialog.addEventListener('pointerdown', event => { fromBackdrop = event.target === dialog; });
    dialog.addEventListener('click', event => {
      if (fromBackdrop && event.target === dialog) desk.dismiss();
      fromBackdrop = false;
    });
    drivers.set(dialog.id, desk);
  }
  return drivers;
}

export function initTabs(root) {
  const bar = root.querySelector('[data-tab-list]');
  const tabs = [...bar.querySelectorAll('[data-tab]')];
  const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));
  if (!tabs.length || panels.some(panel => !panel || !root.contains(panel))) return;
  bar.setAttribute('role', 'tablist');
  const select = index => {
    tabs.forEach((tab, i) => {
      tab.setAttribute('aria-selected', String(i === index));
      tab.tabIndex = i === index ? 0 : -1;
      panels[i].hidden = i !== index;
    });
  };
  tabs.forEach((tab, i) => {
    tab.setAttribute('role', 'tab');
    panels[i].setAttribute('role', 'tabpanel');
    panels[i].tabIndex = 0;
    panels[i].setAttribute('aria-labelledby', tab.id);
    tab.addEventListener('click', () => select(i));
    tab.addEventListener('keydown', event => {
      if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
      const n = ({ ArrowRight: (i + 1) % tabs.length, ArrowLeft: (i + tabs.length - 1) % tabs.length,
        Home: 0, End: tabs.length - 1 })[event.key];
      if (n === undefined) return;
      event.preventDefault();
      select(n);
      tabs[n].focus();
    });
  });
  select(0);
  bar.hidden = false;
}

export function initTooltip(root) {
  const trigger = root.querySelector('[aria-describedby]');
  const tip = trigger && document.getElementById(trigger.getAttribute('aria-describedby'));
  if (!tip || !root.contains(tip)) return;
  let pinned = false;
  function show() {
    tip.style.removeProperty('--tooltip-shift');
    tip.hidden = false;
    const { left, right } = tip.getBoundingClientRect();
    const padding = 10;
    const shift = left < padding ? padding - left : Math.min(0, document.documentElement.clientWidth - right - padding);
    if (shift) tip.style.setProperty('--tooltip-shift', `${shift}px`);
  }
  function dismiss() { pinned = false; tip.hidden = true; }
  root.addEventListener('pointerenter', event => { if (event.pointerType !== 'touch') show(); });
  root.addEventListener('pointerleave', () => { if (!pinned && document.activeElement !== trigger) dismiss(); });
  trigger.addEventListener('focus', show);
  trigger.addEventListener('blur', () => { if (!pinned && !root.matches(':hover')) dismiss(); });
  trigger.addEventListener('click', () => {
    if (pinned) dismiss();
    else { pinned = true; show(); }
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !tip.hidden && !document.querySelector('dialog[open]')) dismiss();
  });
  document.addEventListener('pointerdown', event => { if (!root.contains(event.target)) dismiss(); });
  addEventListener('resize', () => { if (!tip.hidden) show(); }, { passive: true });
  root.hidden = false;
}

export function initPreferences() {
  const root = document.documentElement;
  const motion = document.querySelector('[data-motion-toggle]');
  const theme = document.querySelector('[data-theme-toggle]');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  let off = preferences('motion') === 'off';
  let contrast = preferences('theme') === 'contrast';
  function setMotion() {
    root.dataset.motion = off ? 'off' : 'auto';
    if (motion) {
      motion.setAttribute('aria-pressed', String(off));
      motion.textContent = off || reduce.matches ? 'Animations réduites' : 'Réduire les animations';
    }
  }
  function setTheme() {
    root.dataset.theme = contrast ? 'contrast' : 'default';
    theme?.setAttribute('aria-pressed', String(contrast));
  }
  if (motion) {
    motion.addEventListener('click', () => {
      off = !off;
      preferences('motion', off ? 'off' : 'auto');
      setMotion();
    });
    motion.hidden = false;
  }
  if (theme) {
    theme.addEventListener('click', () => {
      contrast = !contrast;
      preferences('theme', contrast ? 'contrast' : 'default');
      setTheme();
    });
    theme.hidden = false;
  }
  reduce.addEventListener('change', setMotion);
  setMotion();
  setTheme();
}
