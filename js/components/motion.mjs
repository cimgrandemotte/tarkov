/** Particules décoratives et parallaxe légère, suspendues hors écran. */
export function initMotion(hero) {
  const canvas = hero.querySelector('canvas');
  const image = hero.querySelector('[data-parallax]');
  const ctx = canvas?.getContext('2d');
  if (!ctx || !image || !('IntersectionObserver' in globalThis) || !('ResizeObserver' in globalThis)) return;
  const mq = matchMedia('(prefers-reduced-motion: reduce)');
  let nowVisible = false;
  let width = 1, height = 1, dpr = 1;
  let frame = 0, lastTime = 0;
  const motes = Array.from({ length: 26 }, (_, i) => ({
    x: Math.random(), y: Math.random(), r: i % 5 === 0 ? 1.45 : .68,
    drift: .0008 + Math.random() * .0029, alpha: .13 + Math.random() * .28,
  }));
  const allowed = () => nowVisible && !document.hidden && !mq.matches && document.documentElement.dataset.motion !== 'off';

  function clear() {
    ctx.clearRect(0, 0, width, height);
    image.style.removeProperty('--parallax');
  }
  function resize() {
    width = hero.clientWidth;
    height = hero.clientHeight;
    dpr = Math.min(1.5, devicePixelRatio || 1);
    canvas.width = Math.max(1, Math.round(width * dpr));
    canvas.height = Math.max(1, Math.round(height * dpr));
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function loop(time) {
    if (!allowed()) { frame = 0; clear(); return; }
    if (time - lastTime >= 32) {
      const step = Math.min(.065, (time - lastTime) / 1000);
      lastTime = time;
      ctx.clearRect(0, 0, width, height);
      for (const p of motes) {
        p.x = (p.x + p.drift * step + 1) % 1;
        p.y = (p.y - p.drift * step * .65 + 1) % 1;
        ctx.beginPath();
        ctx.fillStyle = `rgba(235,216,177,${p.alpha})`;
        ctx.arc(p.x * width, p.y * height, p.r, 0, Math.PI * 2);
        ctx.fill();
      }
      const y = Math.max(-7, Math.min(7, -hero.getBoundingClientRect().top * .045));
      image.style.setProperty('--parallax', `${y.toFixed(2)}px`);
    }
    frame = requestAnimationFrame(loop);
  }
  function sync() {
    if (allowed() && !frame) {
      lastTime = performance.now();
      frame = requestAnimationFrame(loop);
    } else if (!allowed() && frame) {
      cancelAnimationFrame(frame);
      frame = 0;
      clear();
    }
    hero.dataset.motionActive = String(Boolean(frame));
  }
  new ResizeObserver(resize).observe(hero);
  new IntersectionObserver(([entry]) => { nowVisible = entry.isIntersecting; sync(); }).observe(hero);
  new MutationObserver(sync).observe(document.documentElement, { attributes: true, attributeFilter: ['data-motion'] });
  document.addEventListener('visibilitychange', sync);
  mq.addEventListener('change', sync);
}

export function initReveal() {
  if (!('IntersectionObserver' in globalThis)) return;
  const io = new IntersectionObserver(entries => entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    entry.target.classList.add('reveal--in');
    io.unobserve(entry.target);
  }), { threshold: .16 });
  document.querySelectorAll('[data-reveal]').forEach(node => io.observe(node));
}
