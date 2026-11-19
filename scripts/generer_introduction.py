#!/usr/bin/env python3
"""Crée un thème original de 30 secondes, sans voix, jeu ni banque de sons."""
import json
import numpy as np
from generer_audio import ROOT, RATE, noise, place, swell, tvec, write_mp3


def composition():
    n = RATE * 30
    t = tvec(n)
    rng = np.random.default_rng(321786)
    tau = 2 * np.pi
    breathing = (0.44 + .28 * np.sin(t * .43) ** 2) * np.clip(t / 2.2, 0, 1)
    out = noise(rng, n, 45, 288, .43) * (.024 * breathing)[:, None]
    out += noise(rng, n, 420, 2560, .66) * (.006 * breathing)[:, None]
    surges = (.39 * swell(t, 4.1, 2.1) + .62 * swell(t, 11.5, 3.0) + .78 * swell(t, 19.2, 3.3) + .28 * swell(t, 24.1, 4))
    drones = ((46.25, 0.026, -.18), (92.5, .018, .22), (138.59, .010, -.55), (164.81, .008, .59))
    for idx, (f, level, pan) in enumerate(drones):
        drift = .048 * np.sin(tau * (.12 + idx * .035) * t) + .035 * np.sin(tau * .45 * t + idx)
        phase = tau * (f * t + drift)
        tone = (np.sin(phase) + .18 * np.sin(phase * 2.002 + .4)) * surges * level
        out[:, 0] += tone * (1 - pan * .55)
        out[:, 1] += np.roll(tone, 273 + idx * 97) * (1 + pan * .55)
    for seq, (pos, freq) in enumerate([(2.75,185),(5.72,246.94),(8.2,207.65),(12.38,185),(14.77,277.18),(17.92,246.94),(21.3,207.65),(24.57,185)]):
        x = tvec(int(2.15 * RATE))
        env = (1 - np.exp(-x * 160)) * (np.exp(-x * 4.3) + .085 * np.exp(-x * 1.5))
        bell = np.sin(tau * freq * x) + .18 * np.sin(tau * (freq * 2.03) * x) + .055 * np.sin(tau * freq * 4.04 * x)
        sample = bell * env * (.059 + .048 * (3 <= seq <= 5))
        side = -.54 if seq % 2 else .46
        place(out, pos, sample, side)
        place(out, pos + .186, sample * .20, -side)
        place(out, pos + .408, sample * .09, side * .5)
    for pos, side, level in ((1.54,-.6,.055),(10.18,.7,.072),(21.67,-.25,.052)):
        x = tvec(int(.8 * RATE)); static = noise(rng, len(x), 970, 3300, .10)[:,0]
        place(out, pos, static * np.exp(-x * 9) * np.sin(np.pi * np.minimum(1, x * 1.25)) * level, side)
    envelope = np.minimum(1, t / 1.4) ** 2 * np.minimum(1, (30 - t) / 4.2) ** 2
    return out * envelope[:, None]


def main():
    catalogue = ROOT / 'audio/catalogue.json'
    data = json.loads(catalogue.read_text())
    rel = 'audio/themes/intro_norvinsk.mp3'
    file = ROOT / rel
    output = {'fichier': rel, 'nom': 'Signal de Norvinsk', 'type': 'theme', 'boucle': False,
              **write_mp3(file, composition(), -22.5)}
    data['clips'] = [clip for clip in data['clips'] if clip['fichier'] != rel] + [output]
    catalogue.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(rel, output['secondesPcm'], 's (PCM)', output['octets'], 'octets')


if __name__ == '__main__':
    main()
