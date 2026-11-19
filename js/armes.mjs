/** Pages Armes et munitions : filtres du catalogue, comparateur à trois entrées,
 *  filtres du tableau balistique et nuage pénétration / dégâts.
 *  Aucune requête réseau : les données sont intégrées au HTML ou lues dans le
 *  script JSON embarqué par le rendu des pages. */
import { preferences } from './components/ui.mjs';

const normaliser = valeur => String(valeur ?? '')
  .toLowerCase()
  .normalize('NFD')
  .replace(/[\u0300-\u036f]/g, '');

const nombreFr = valeur => (typeof valeur === 'number' && Number.isFinite(valeur)
  ? valeur.toLocaleString('fr-FR')
  : '—');

function lireJson(selecteur) {
  const source = document.querySelector(selecteur);
  if (!source) return [];
  try { return JSON.parse(source.textContent) ?? []; } catch { return []; }
}

function alimenter(selecteur, valeurs, valeurParDefaut) {
  const champ = document.querySelector(selecteur);
  if (!champ) return;
  const premier = champ.querySelector('option');
  const modele = premier ? premier.outerHTML : '<option value=""></option>';
  champ.innerHTML = modele;
  for (const [valeur, libelle] of valeurs) {
    const option = document.createElement('option');
    option.value = valeur;
    option.textContent = libelle;
    champ.append(option);
  }
  if (valeurParDefaut && champ.querySelector(`option[value="${CSS.escape(valeurParDefaut)}"]`)) {
    champ.value = valeurParDefaut;
  }
}

/* ------------------------------------------------------------------ */
/* Hub arsenal : filtres du catalogue et comparateur à trois entrées.   */
/* ------------------------------------------------------------------ */

function initArsenal() {
  const table = document.querySelector('#armes-catalogue');
  if (!table) return;
  const lignes = [...table.querySelectorAll('tbody tr')];
  const total = lignes.length;

  const recherche = document.querySelector('[data-armes-search]');
  const famille = document.querySelector('[data-armes-famille]');
  const calibre = document.querySelector('[data-armes-calibre]');
  const marchand = document.querySelector('[data-armes-marchand]');
  const ergonomie = document.querySelector('[data-armes-ergonomie]');
  const recul = document.querySelector('[data-armes-recul]');
  const cadence = document.querySelector('[data-armes-cadence]');
  const compte = document.querySelector('[data-armes-compte]');

  const familles = new Map();
  const calibres = new Map();
  for (const ligne of lignes) {
    const nomFamille = ligne.dataset.famille || '';
    const nomCalibre = ligne.dataset.calibre || '';
    familles.set(nomFamille, (familles.get(nomFamille) ?? 0) + 1);
    calibres.set(nomCalibre, (calibres.get(nomCalibre) ?? 0) + 1);
  }
  const libelleFamille = {
    'fusils-assaut': 'Fusils d’assaut et carabines',
    'pistolets-mitrailleurs': 'Pistolets-mitrailleurs',
    'fusils-a-pompe': 'Fusils à pompe',
    'fusils-de-precision': 'Fusils de précision à verrou',
    dmr: 'Fusils de précision semi-auto',
    mitrailleuses: 'Mitrailleuses légères',
    pistolets: 'Pistolets et revolvers',
    'arme-de-melee': 'Armes de mêlée',
    'lance-grenades': 'Lance-grenades et lanceurs',
  };
  alimenter('[data-armes-famille]', [...familles.entries()]
    .sort((a, b) => b[1] - a[1])
    .map(([cle, compteFamille]) => [cle, `${libelleFamille[cle] ?? cle} (${compteFamille})`]));
  alimenter('[data-armes-calibre]', [...calibres.entries()]
    .sort((a, b) => a[0].localeCompare(b[0], 'fr'))
    .map(([cle, compteCalibre]) => [cle, `${cle} (${compteCalibre})`]));

  function appliquer() {
    const terme = normaliser(recherche?.value ?? '');
    const familleChoisie = famille?.value ?? 'toutes';
    const calibreChoisi = calibre?.value ?? 'tous';
    const marchandChoisi = marchand?.value ?? 'toutes';
    const ergonomieMin = Number.parseFloat(ergonomie?.value ?? '');
    const reculMax = Number.parseFloat(recul?.value ?? '');
    const cadenceMin = Number.parseFloat(cadence?.value ?? '');
    let visibles = 0;
    for (const ligne of lignes) {
      const nom = normaliser(ligne.dataset.nom ?? '');
      const ergo = Number.parseFloat(ligne.dataset.ergonomie ?? '');
      const rec = Number.parseFloat(ligne.dataset.recul ?? '');
      const cad = Number.parseFloat(ligne.dataset.cadence ?? '');
      const correspond = (!terme || nom.includes(terme))
        && (familleChoisie === 'toutes' || ligne.dataset.famille === familleChoisie)
        && (calibreChoisi === 'tous' || ligne.dataset.calibre === calibreChoisi)
        && (marchandChoisi === 'toutes' || ligne.dataset.marchand === marchandChoisi)
        && (!(ergonomieMin >= 0) || (Number.isFinite(ergo) && ergo >= ergonomieMin))
        && (!(reculMax >= 0) || (Number.isFinite(rec) && rec <= reculMax))
        && (!(cadenceMin >= 0) || (Number.isFinite(cad) && cad >= cadenceMin));
      ligne.hidden = !correspond;
      if (correspond) visibles += 1;
    }
    if (compte) {
      compte.textContent = `${visibles} ${visibles > 1 ? 'armes affichées' : 'arme affichée'} sur ${total}`;
    }
  }

  for (const champ of [recherche, famille, calibre, marchand, ergonomie, recul, cadence]) {
    champ?.addEventListener('input', appliquer);
    champ?.addEventListener('change', appliquer);
  }
  appliquer();

  // Comparateur à trois entrées.
  const armes = lireJson('#armes-donnees');
  const corpsComparatif = document.querySelector('[data-armes-compare-corps]');
  const enteteComparatif = document.querySelector('[data-armes-compare-table] thead tr');
  const champs = ['a', 'b', 'c'].map(cle => document.querySelector(`[data-armes-compare-${cle}]`));
  const statut = document.querySelector('[data-armes-compare-status]');
  if (!armes.length || !corpsComparatif || !enteteComparatif || !champs.some(Boolean)) return;

  const options = armes.map(arme => `<option value="${arme.id}">${arme.nom}</option>`).join('');
  for (const champ of champs) {
    if (!champ) continue;
    champ.innerHTML = '<option value="">—</option>' + options;
  }
  const indicateurs = [
    ['Famille', arme => libelleFamille[arme.famille] ?? arme.famille],
    ['Calibre', arme => arme.calibre],
    ['Ergonomie', arme => nombreFr(arme.ergonomie)],
    ['Recul vertical', arme => nombreFr(arme.reculVertical)],
    ['Recul horizontal', arme => nombreFr(arme.reculHorizontal)],
    ['Cadence (c/min)', arme => nombreFr(arme.cadence)],
    ['Distance efficace (m)', arme => nombreFr(arme.distanceEfficace)],
    ['Modes de tir', arme => (arme.modeTirFr || []).join(', ') || '—'],
    ['Munitions compatibles', arme => nombreFr(arme.nbMunitions)],
    ['Presets publiés', arme => nombreFr(arme.nbPresets)],
    ['Poids (kg)', arme => nombreFr(arme.poids)],
    ['Prix marchand', arme => (typeof arme.prixMarchand === 'number' ? `${nombreFr(arme.prixMarchand)} ₽` : '—')],
    ['Disponibilité', arme => (arme.disponibleChezMarchand ? `En magasin (${arme.marchands.join(', ')})` : 'Sans offre en magasin')],
  ];

  function rendre() {
    const choisies = champs
      .filter(Boolean)
      .map(champ => armes.find(arme => arme.id === champ.value))
      .filter(Boolean);
    enteteComparatif.querySelectorAll('th:nth-child(n+2)').forEach(th => th.remove());
    corpsComparatif.innerHTML = '';
    if (!choisies.length) {
      if (statut) statut.textContent = 'Sélectionnez jusqu’à trois armes.';
      return;
    }
    for (const arme of choisies) {
      const th = document.createElement('th');
      th.scope = 'col';
      th.textContent = arme.nom;
      enteteComparatif.append(th);
    }
    for (const [libelle, lire] of indicateurs) {
      const tr = document.createElement('tr');
      const th = document.createElement('th');
      th.scope = 'row';
      th.textContent = libelle;
      tr.append(th);
      for (const arme of choisies) {
        const td = document.createElement('td');
        td.textContent = lire(arme);
        tr.append(td);
      }
      corpsComparatif.append(tr);
    }
    if (statut) {
      statut.textContent = `${choisies.length} ${choisies.length > 1 ? 'armes comparées' : 'arme comparée'} · mesures à configuration de base.`;
    }
  }

  for (const champ of champs) champ?.addEventListener('change', rendre);
  const memoriser = preferences('armes:comparateur');
  if (memoriser) {
    try {
      const choix = JSON.parse(memoriser);
      champs.forEach((champ, index) => {
        if (champ && choix?.[index]) champ.value = choix[index];
      });
    } catch { /* Valeur illisible : on garde les choix par défaut. */ }
  }
  const sauvegarder = () => preferences('armes:comparateur',
    JSON.stringify(champs.map(champ => champ?.value ?? '')));
  for (const champ of champs) champ?.addEventListener('change', sauvegarder);
  rendre();
}

/* ------------------------------------------------------------------ */
/* Tableau balistique : filtres du tableau et nuage de points.         */
/* ------------------------------------------------------------------ */

function initAmmo() {
  const table = document.querySelector('#ammo-tableau');
  if (!table) return;
  const lignes = [...table.querySelectorAll('tbody tr')];
  const total = lignes.length;

  const recherche = document.querySelector('[data-ammo-search]');
  const calibre = document.querySelector('[data-ammo-calibre]');
  const marchand = document.querySelector('[data-ammo-marchand]');
  const type = document.querySelector('[data-ammo-type]');
  const penetration = document.querySelector('[data-ammo-penetration]');
  const degats = document.querySelector('[data-ammo-degats]');
  const classe = document.querySelector('[data-ammo-classe]');
  const compte = document.querySelector('[data-ammo-compte]');

  const calibres = new Map();
  const types = new Map();
  for (const ligne of lignes) {
    const nomCalibre = ligne.dataset.calibre || '';
    const nomType = ligne.dataset.type || '';
    calibres.set(nomCalibre, (calibres.get(nomCalibre) ?? 0) + 1);
    types.set(nomType, (types.get(nomType) ?? 0) + 1);
  }
  const libelleType = {
    bullet: 'Projectile simple',
    buckshot: 'Projectiles multiples',
    grenade: 'Projectile explosif',
    flashbang: 'Projectile incapacitant',
  };
  alimenter('[data-ammo-calibre]', [...calibres.entries()]
    .sort((a, b) => a[0].localeCompare(b[0], 'fr'))
    .map(([cle, valeur]) => [cle, `${cle} (${valeur})`]));
  alimenter('[data-ammo-type]', [...types.entries()]
    .sort((a, b) => b[1] - a[1])
    .map(([cle, valeur]) => [cle, `${libelleType[cle] ?? cle} (${valeur})`]));

  function appliquer() {
    const terme = normaliser(recherche?.value ?? '');
    const calibreChoisi = calibre?.value ?? 'tous';
    const marchandChoisi = marchand?.value ?? 'toutes';
    const typeChoisi = type?.value ?? 'tous';
    const penetrationMin = Number.parseFloat(penetration?.value ?? '');
    const degatsMin = Number.parseFloat(degats?.value ?? '');
    const classeChoisie = classe?.value ?? 'toutes';
    let visibles = 0;
    for (const ligne of lignes) {
      const nom = normaliser(ligne.dataset.nom ?? '');
      const pen = Number.parseFloat(ligne.dataset.penetration ?? '');
      const deg = Number.parseFloat(ligne.dataset.degats ?? '');
      const correspond = (!terme || nom.includes(terme))
        && (calibreChoisi === 'tous' || ligne.dataset.calibre === calibreChoisi)
        && (marchandChoisi === 'toutes' || ligne.dataset.marchand === marchandChoisi)
        && (typeChoisi === 'tous' || ligne.dataset.type === typeChoisi)
        && (!(penetrationMin >= 0) || (Number.isFinite(pen) && pen >= penetrationMin))
        && (!(degatsMin >= 0) || (Number.isFinite(deg) && deg >= degatsMin))
        && (classeChoisie === 'toutes' || ligne.dataset.classe === classeChoisie);
      ligne.hidden = !correspond;
      if (correspond) visibles += 1;
    }
    if (compte) {
      compte.textContent = `${visibles} ${visibles > 1 ? 'cartouches affichées' : 'cartouche affichée'} sur ${total}`;
    }
  }

  for (const champ of [recherche, calibre, marchand, type, penetration, degats, classe]) {
    champ?.addEventListener('input', appliquer);
    champ?.addEventListener('change', appliquer);
  }
  appliquer();
}

function chargerChartJs() {
  if (window.Chart) return Promise.resolve(window.Chart);
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = new URL('vendor/chart.umd.js', import.meta.url).href;
    script.async = true;
    script.addEventListener('load', () => (window.Chart ? resolve(window.Chart) : reject(new Error('Chart.js indisponible'))));
    script.addEventListener('error', () => reject(new Error('Chart.js indisponible')));
    document.head.append(script);
  });
}

async function initNuage() {
  const toile = document.querySelector('#armes-nuage');
  if (!toile) return;
  const munitions = lireJson('#munitions-donnees');
  const note = document.querySelector('[data-armes-chart-note]');
  if (!munitions.length) return;
  let Chart;
  try {
    Chart = await chargerChartJs();
  } catch {
    if (note) {
      note.textContent = 'La visualisation n’a pas pu être chargée : le tableau complet ci-dessous reste disponible et filtrable.';
    }
    return;
  }

  const couleurs = {
    bullet: 'rgba(212, 176, 106, 0.75)',
    buckshot: 'rgba(126, 178, 147, 0.75)',
    grenade: 'rgba(201, 106, 106, 0.8)',
    flashbang: 'rgba(140, 160, 196, 0.8)',
  };
  const parType = new Map();
  for (const munition of munitions) {
    const type = munition.typeProjectile || 'bullet';
    if (!parType.has(type)) parType.set(type, []);
    parType.get(type).push({
      x: munition.penetration ?? 0,
      y: munition.degats ?? 0,
      nom: munition.nom,
      calibre: munition.calibre,
      classe: munition.classeAtteinte || '—',
      marchande: munition.disponibleChezMarchand ? 'En magasin' : 'Sans offre en magasin',
    });
  }
  const libelleType = {
    bullet: 'Projectile simple',
    buckshot: 'Projectiles multiples',
    grenade: 'Projectile explosif',
    flashbang: 'Projectile incapacitant',
  };

  const graphe = new Chart(toile.getContext('2d'), {
    type: 'scatter',
    data: {
      datasets: [...parType.entries()].map(([type, points]) => ({
        label: `${libelleType[type] ?? type} (${points.length})`,
        data: points,
        backgroundColor: couleurs[type] ?? 'rgba(200, 200, 200, 0.7)',
        borderColor: 'rgba(12, 15, 12, 0.8)',
        borderWidth: 0.6,
        pointRadius: 3.6,
        pointHoverRadius: 6,
      })),
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      scales: {
        x: {
          title: { display: true, text: 'Pénétration' },
          beginAtZero: true,
          grid: { color: 'rgba(255, 255, 255, 0.08)' },
          ticks: { color: '#c9c6bb' },
        },
        y: {
          title: { display: true, text: 'Dégâts' },
          beginAtZero: true,
          grid: { color: 'rgba(255, 255, 255, 0.08)' },
          ticks: { color: '#c9c6bb' },
        },
      },
      plugins: {
        legend: { labels: { color: '#c9c6bb' } },
        tooltip: {
          callbacks: {
            label: (contexte) => {
              const point = contexte.raw;
              return [`${point.nom}`, `${point.calibre} · classe atteinte ${point.classe}`, point.marchande];
            },
          },
        },
      },
    },
  });

  if (note) {
    const classeMax = munitions.reduce((max, munition) => Math.max(max, munition.classeAtteinte ?? 0), 0);
    note.textContent = `Nuage des ${munitions.length} cartouches de l’export, relevé du 18 novembre 2026 : pénétration en abscisse, dégâts en ordonnée. La classe d’armure atteinte va jusqu’à la classe ${classeMax} selon la règle de pénétration du correctif 0.14.6.0.`;
  }
  window.addEventListener('resize', () => graphe.resize(), { passive: true });
}

initArsenal();
initAmmo();
initNuage();
