#!/usr/bin/env python3
"""Synthèse originale des ambiances Tarkov Ultimate Guide. Sortie MP3 uniquement.
Dépendances de production audio : numpy, scipy, lameenc. Aucun échantillon externe.
"""
import hashlib
import json
from pathlib import Path

import lameenc
import numpy as np
from scipy.signal import butter, sosfilt

ROOT = Path(__file__).resolve().parent.parent
RATE = 44100
BITRATE = 160
LOOP = 60
CROSSFADE = int(0.9 * RATE)
PI2 = np.pi * 2
LENGTH = RATE * LOOP + CROSSFADE


def noise(rng, n, low, high, stereo=0.4):
    """Mix de bruit commun et latéral, filtré et normalisé à un RMS de 1."""
    common = rng.normal(size=(n, 1)).astype('float32')
    sides = rng.normal(size=(n, 2)).astype('float32')
    signal = common * (1 - stereo) + sides * stereo
    filtered = sosfilt(butter(2, (low, high), btype='bandpass', fs=RATE, output='sos'), signal, axis=0)
    return (filtered / max(np.sqrt(np.mean(filtered ** 2)), 1e-8)).astype('float32')


def tvec(n):
    return np.arange(n, dtype=np.float64) / RATE


def swell(t, center, width):
    return np.exp(-0.5 * ((t - center) / width) ** 2)


def place(dest, t, mono, pan=0.0):
    n = int(t * RATE)
    remaining = min(len(mono), len(dest) - n)
    if n >= 0 and remaining > 0:
        angles = (np.clip(pan, -1, 1) + 1) * np.pi / 4
        dest[n:n + remaining] += np.column_stack((mono[:remaining] * np.cos(angles), mono[:remaining] * np.sin(angles)))


def impacts(out, rng, n, frequencies, volume, decay, resonance=0.15):
    """Petites résonances d'impacts et texture de surface, réparties en stéréo."""
    max_time = len(out) / RATE
    for _ in range(n):
        at = rng.uniform(0, max_time)
        d = rng.uniform(decay * 0.45, decay * 1.75)
        t = tvec(int(RATE * d * 4.5))
        f = rng.uniform(*frequencies)
        envelope = (1 - np.exp(-t * 3800)) * np.exp(-t / d)
        textured = (rng.normal(size=len(t)) * 0.32 + resonance * np.sin(PI2 * f * t))
        place(out, at, textured * envelope * rng.uniform(0.25, 1.0) * volume, rng.uniform(-0.85, 0.85))


def distant_siren(out, t, center, amplitude, pan):
    # Sinusoïde lointaine et deux reflets plutôt qu'un signal d'alerte réaliste au premier plan.
    phase = PI2 * (405 * t - 32 / (PI2 * .18) * np.cos(PI2 * .18 * t))
    signal = (np.sin(phase) + .21 * np.sin(2 * phase + .4)) * swell(t, center, 2.1) * amplitude
    out[:, 0] += signal * (1 - pan * .32)
    out[:, 1] += np.roll(signal, 382) * (1 + pan * .32)


def rain(rng):
    t = tvec(LENGTH)
    change = (0.81 + .13 * np.sin(PI2 * .08 * t) + .08 * np.sin(PI2 * .21 * t + 2.1))[:, None]
    out = (noise(rng, LENGTH, 150, 1200, .63) * .033 + noise(rng, LENGTH, 1300, 6500, .71) * .034) * change
    out += noise(rng, LENGTH, 65, 320, .45) * .013
    impacts(out, rng, 2870, (540, 3300), .17, .012, .40)
    thunder = .036 * swell(t, 15.5, 2.5) + .025 * swell(t, 43.7, 3.5)
    out += noise(rng, LENGTH, 26, 87, .25) * thunder[:, None]
    distant_siren(out, t, 34, .0095, .90)
    return out


def industrial(rng):
    t = tvec(LENGTH)
    air = noise(rng, LENGTH, 40, 470, .44) * (.022 * (1 + .27 * np.sin(PI2 * .16 * t)))[:, None]
    out = air + noise(rng, LENGTH, 430, 2200, .62) * .012
    phase = PI2 * (51.3 * t + .22 * np.sin(PI2 * .48 * t))
    hum = .017 * np.sin(phase) + .012 * np.sin(2 * phase + .18) + .004 * np.sin(3 * phase)
    hum *= (.85 + .13 * np.cos(PI2 * .24 * t))
    out[:, 0] += hum
    out[:, 1] += np.roll(hum, 98) * .91
    impacts(out, rng, 460, (82, 530), .080, .035, .56)
    impacts(out, rng, 21, (330, 690), .102, .16, .46)
    return out


def forest(rng):
    t = tvec(LENGTH)
    gust = (.50 + .25 * (1 + np.sin(PI2 * .09 * t)) + .17 * (1 + np.sin(PI2 * .041 * t + 1)))[:, None]
    out = noise(rng, LENGTH, 72, 525, .54) * .032 * gust
    out += noise(rng, LENGTH, 850, 4800, .75) * .014 * gust**2
    impacts(out, rng, 780, (380, 1550), .088, .018, .19)
    impacts(out, rng, 7, (195, 440), .21, .059, .29)
    for at, pan in ((9.6, -.64), (25.1, -.78), (37.4, .55), (52.3, .76)):
        for delay in (0, .24, .60):
            chirp = tvec(int(.17 * RATE)); tone = rng.uniform(605, 825)
            signal = np.sin(PI2 * (tone * chirp - 480 * chirp**2)) * np.sin(np.pi * chirp / .17)**2
            place(out, at + delay, signal * rng.uniform(.023, .036), pan)
    return out


def urban(rng):
    t = tvec(LENGTH)
    traces = .74 + .25 * np.sin(PI2 * .065 * t) + .14 * np.cos(PI2 * .19 * t + .6)
    out = noise(rng, LENGTH, 43, 240, .42) * (.027 * traces)[:, None]
    out += noise(rng, LENGTH, 285, 1520, .67) * (.017 * traces)[:, None]
    out += noise(rng, LENGTH, 2100, 6200, .67) * .006
    distant_siren(out, t, 21.0, .023, -.75)
    distant_siren(out, t, 47.9, .010, .60)
    impacts(out, rng, 200, (265, 620), .065, .028, .54)
    impacts(out, rng, 11, (990, 2540), .11, .061, .69)
    return out


def effect(rng, mode):
    secs = {'hover': .165, 'click': .32, 'notification': .81}[mode]
    n = int(RATE * secs)
    t = tvec(n)
    signal = np.zeros((n, 2))
    if mode in ('hover', 'click'):
        for pos, f, vol, decay in [(0.011, 1389, .27, .019), (.057, 704, .13, .016)] if mode == 'hover' else [(0.018, 894, .24, .022), (.066, 471, .42, .029), (.13, 226, .27, .054)]:
            tt = tvec(int(decay * 4 * RATE))
            metal = np.sin(PI2 * f * tt) + .34 * np.sin(PI2 * (f * 2.59) * tt)
            env = (1 - np.exp(-tt * 2500)) * np.exp(-tt / decay)
            place(signal, pos, vol * env * (metal + rng.normal(size=len(tt)) * .26), .11)
    else:
        signal += noise(rng, n, 600, 3280, .30) * (.010 * swell(t, .27, .18))[:, None]
        for pos, f in ((.075, 634), (.24, 813), (.405, 970)):
            tt = tvec(int(RATE * .136))
            shape = np.sin(np.pi * np.minimum(tt / .136, 1.0)) ** 1.4
            place(signal, pos, .19 * shape * (np.sin(PI2 * f * tt) + .1 * np.sin(PI2 * 2 * f * tt)), 0.0)
    nfade = int(.013 * RATE)
    signal[-nfade:] *= np.linspace(1, 0, nfade)[:, None]
    return signal


def seamless(audio):
    """Conserver 60 s, joindre la fin à sa continuation puis fondre vers le début."""
    s = RATE * LOOP
    head = np.linspace(0, np.pi / 2, CROSSFADE)[:, None]
    audio[:CROSSFADE] = audio[s:s + CROSSFADE] * np.cos(head)**2 + audio[:CROSSFADE] * np.sin(head)**2
    return audio[:s]


def write_mp3(path, audio, target_dbfs):
    audio = audio - audio.mean(axis=0)
    audio *= 10 ** (target_dbfs / 20) / max(1e-8, np.sqrt(np.mean(audio**2)))
    audio = np.tanh(audio / .76) * .76
    pcm = np.round(np.clip(audio, -1, 1) * 32767).astype('<i2').tobytes()
    encoder = lameenc.Encoder()
    encoder.set_bit_rate(BITRATE)
    encoder.set_in_sample_rate(RATE)
    encoder.set_channels(2)
    encoder.set_quality(2)
    encoder.silence()
    data = bytes(encoder.encode(pcm) + encoder.flush())
    path.write_bytes(data)
    return {'octets': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'secondesPcm': len(audio) / RATE,
            'rmsDbfsPcm': round(20 * np.log10(np.sqrt(np.mean(audio**2))), 1),
            'cretesDbfsPcm': round(20 * np.log10(np.max(np.abs(audio))), 1)}


def main():
    clips = []
    for i, (name, label, generator) in enumerate((('rain', 'Pluie sur tôle', rain), ('industrial', 'Bunker industriel', industrial),
                                                   ('forest', 'Forêt nocturne', forest), ('urban', 'Ruines urbaines', urban))):
        path = Path(f'audio/ambient/ambient_{name}.mp3')
        audio = seamless(generator(np.random.default_rng(96671 + i)))
        clips.append({'fichier': str(path), 'nom': label, 'type': 'ambiance', 'boucle': True,
                      **write_mp3(ROOT / path, audio, -24.0)})
        print(path, 'OK', flush=True)
    for i, (name, label) in enumerate((('hover', 'Effleurement métallique'), ('click', 'Clic métallique'), ('notification', 'Signal radio'))):
        path = Path(f'audio/ui/ui_{name}.mp3')
        clips.append({'fichier': str(path), 'nom': label, 'type': 'interface', 'boucle': False,
                      **write_mp3(ROOT / path, effect(np.random.default_rng(1066 + i), name), -24.0)})
        print(path, 'OK', flush=True)
    catalogue = ROOT / 'audio/catalogue.json'
    previous = json.loads(catalogue.read_text(encoding='utf-8')) if catalogue.is_file() else {}
    generated = {clip['fichier'] for clip in clips}
    # Préserver les thèmes et autres lots ajoutés après les fondations.
    clips.extend(clip for clip in previous.get('clips', []) if clip['fichier'] not in generated)
    doc = {**previous, 'schemaVersion': 1, 'origine': 'Synthèse sonore originale, sans échantillon externe',
           'format': 'MP3', 'canaux': 2, 'echantillonnageHz': RATE, 'debitKbS': BITRATE, 'clips': clips}
    stage = catalogue.with_suffix('.tmp')
    stage.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    stage.replace(catalogue)



if __name__ == '__main__':
    main()
