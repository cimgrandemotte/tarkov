import { preferences } from './ui.mjs';

const base = new URL('../../audio/', import.meta.url);
const ambiences = Object.freeze({
  rain: 'Pluie sur tôle', industrial: 'Bunker industriel', forest: 'Forêt nocturne', urban: 'Ruines urbaines',
  intro: 'Signal de Norvinsk',
});
const effects = Object.freeze({ hover: 'Effleurement métallique', click: 'Clic métallique', notification: 'Signal radio' });
const clamp = (number, lo, hi) => Math.min(hi, Math.max(lo, number));

export function initAudio(root) {
  const stream = root.querySelector('audio[data-audio-element]');
  const play = root.querySelector('[data-audio-toggle]');
  const label = play?.querySelector('[data-audio-label]');
  const track = root.querySelector('[data-audio-track]');
  const live = root.querySelector('[data-audio-status]');
  const volume = root.querySelector('[data-audio-volume]');
  const value = root.querySelector('[data-audio-volume-value]');
  const effectLive = root.querySelector('[data-audio-sample-status]');
  const options = [...root.querySelectorAll('[data-ambience]')];
  if (!stream || !label || !track || !live || !volume || !value) return;
  const prefKey = root.dataset.audioPreference || 'ambience';
  const storedTrack = preferences(prefKey);
  const available = options.map(button => button.dataset.ambience).filter(key => Object.hasOwn(ambiences, key));
  let selected = available.includes(storedTrack) ? storedTrack : available[0] ?? 'rain';
  const storedVolume = preferences('gain');
  let gain = storedVolume !== null && Number.isFinite(Number(storedVolume)) ? clamp(Number(storedVolume), 0, 100) : 32;
  let serial = 0;
  let requested = false;
  let loaded;
  let effect;
  let effectSeq = 0;

  function state(name, message) {
    root.dataset.audioState = name;
    label.textContent = ({ ready: 'Écouter', paused: 'Reprendre', loading: 'Annuler', playing: 'Pause', error: 'Réessayer' })[name];
    const isError = name === 'error';
    live.toggleAttribute('data-error', isError);
    if (live.textContent !== message) live.textContent = message;
  }
  function paintTrack() {
    track.textContent = ambiences[selected];
    options.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.ambience === selected)));
  }
  function setGain() {
    stream.volume = gain / 100;
    volume.value = String(gain);
    volume.setAttribute('aria-valuetext', `${gain} pour cent`);
    value.textContent = `${gain} %`;
  }
  function fail(id, err) {
    if (id !== serial || !requested || err?.name === 'AbortError') return;
    requested = false;
    stream.pause();
    loaded = null;
    state('error', err?.name === 'NotAllowedError' ? 'Lecture refusée par le navigateur. Relancez avec le bouton.' : 'Cette piste n’a pas pu être lue. Réessayez ou sélectionnez une autre ambiance.');
  }
  async function start() {
    const id = ++serial;
    requested = true;
    state('loading', `Chargement · ${ambiences[selected]}`);
    if (loaded !== selected) {
      loaded = selected;
      const isTheme = selected === 'intro';
      stream.loop = !isTheme;
      stream.src = new URL(isTheme ? 'themes/intro_norvinsk.mp3' : `ambient/ambient_${selected}.mp3`, base).href;
    }
    try {
      await stream.play();
      if (id === serial && requested) state('playing', `En lecture · ${ambiences[selected]}`);
    } catch (err) { fail(id, err); }
  }
  function pause() {
    serial++;
    requested = false;
    stream.pause();
    state('paused', `En pause · ${ambiences[selected]}`);
  }
  play.addEventListener('click', () => { if (requested) pause(); else void start(); });
  stream.addEventListener('error', () => fail(serial));
  stream.addEventListener('pause', () => {
    if (requested && stream.paused && !stream.ended && root.dataset.audioState === 'playing') pause();
  });
  stream.addEventListener('ended', () => {
    serial++;
    requested = false;
    state('ready', `Écoute terminée · ${ambiences[selected]}`);
  });
  for (const button of options) button.addEventListener('click', () => {
    const next = button.dataset.ambience;
    if (!Object.hasOwn(ambiences, next) || next === selected) return;
    selected = next;
    preferences(prefKey, selected);
    paintTrack();
    if (requested) void start();
    else state('ready', 'Prêt · aucune lecture automatique');
  });
  volume.addEventListener('input', () => {
    gain = clamp(Number(volume.value), 0, 100);
    setGain();
    preferences('gain', gain);
  });

  function playEffect(name) {
    if (!Object.hasOwn(effects, name)) return;
    const seq = ++effectSeq;
    effect?.unload();
    const url = new URL(`ui/ui_${name}.mp3`, base).href;
    effectLive.textContent = `Échantillon : ${effects[name]}.`;
    if (typeof globalThis.Howl === 'function') {
      const error = () => { if (seq === effectSeq) effectLive.textContent = 'Lecture de l’échantillon impossible.'; };
      effect = new globalThis.Howl({ src: [url], html5: true, preload: false, volume: .23, onloaderror: error, onplayerror: error });
      effect.play();
    } else {
      const audio = new Audio(url);
      audio.volume = .23;
      effect = { unload() { audio.pause(); audio.removeAttribute('src'); audio.load(); } };
      audio.play().catch(() => { if (seq === effectSeq) effectLive.textContent = 'Lecture de l’échantillon impossible.'; });
    }
  }
  root.querySelectorAll('[data-effect]').forEach(button => button.addEventListener('click', () => playEffect(button.dataset.effect)));
  paintTrack();
  setGain();
  root.querySelectorAll('[data-audio-control]').forEach(element => { element.hidden = false; });
}
