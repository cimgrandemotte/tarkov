/** Pages Cartes : filtres de l'atlas, comparatif de deux lieux, couches d'une fiche de carte.
 *  Aucune requête réseau : les données sont intégrées au HTML. */
import { preferences } from './components/ui.mjs';

const normaliser = valeur => String(valeur ?? '')
  .toLowerCase()
  .normalize('NFD')
  .replace(/[\u0300-\u036f]/g, '');

function initAtlas() {
  const racine = document.querySelector('[data-atlas]');
  if (!racine) return;
  const cartes = [...racine.querySelectorAll('[data-atlas-card]')];
  const recherche = racine.querySelector('[data-atlas-search]');
  const compte = racine.querySelector('[data-atlas-count]');
  const vide = racine.querySelector('[data-atlas-empty]');
  const mode = racine.querySelector('[data-atlas-mode]');
  const menace = racine.querySelector('[data-atlas-threat]');

  function appliquer() {
    const terme = normaliser(recherche?.value ?? '');
    const modeChoisi = mode?.value ?? 'tous';
    const menaceChoisie = menace?.value ?? 'toutes';
    let visibles = 0;
    for (const carte of cartes) {
      const texte = normaliser(carte.dataset.recherche ?? carte.textContent);
      const correspond = (!terme || texte.includes(terme))
        && (modeChoisi === 'tous' || (carte.dataset.modes ?? '').split(' ').includes(modeChoisi))
        && (menaceChoisie === 'toutes' || (carte.dataset.threat ?? '').split(' ').includes(menaceChoisie));
      carte.hidden = !correspond;
      if (correspond) visibles += 1;
    }
    if (compte) compte.textContent = `${visibles} ${visibles > 1 ? 'lieux affichés' : 'lieu affiché'} sur ${cartes.length}`;
    if (vide) vide.hidden = visibles !== 0;
  }

  recherche?.addEventListener('input', appliquer);
  mode?.addEventListener('change', appliquer);
  menace?.addEventListener('change', appliquer);
  appliquer();

  // Comparatif de deux lieux, données intégrées à la page.
  const source = document.querySelector('[data-compare-data]');
  const grille = document.querySelector('[data-compare-grid]');
  const champA = document.querySelector('[data-compare-a]');
  const champB = document.querySelector('[data-compare-b]');
  if (!source || !grille || !champA || !champB) return;
  let donnees = [];
  try { donnees = JSON.parse(source.textContent) ?? []; } catch { donnees = []; }
  if (!donnees.length) return;
  const parSlug = new Map(donnees.map(lieu => [lieu.slug, lieu]));
  const options = donnees.map(lieu => `<option value="${lieu.slug}">${lieu.nom}</option>`).join('');
  champA.innerHTML = options;
  champB.innerHTML = options;
  if (donnees[1]) champB.value = donnees[1].slug;

  function ligne(label, valeur) {
    return `<dt>${label}</dt><dd>${valeur ?? '—'}</dd>`;
  }

  function rendre() {
    const a = parSlug.get(champA.value);
    const b = parSlug.get(champB.value);
    if (!a || !b) { grille.innerHTML = ''; return; }
    const lignes = [
      ['Durée de raid', lieu => `${lieu.duree} min`],
      ['Effectif PMC', lieu => lieu.joueurs],
      ['Niveaux', lieu => lieu.niveaux],
      ['Sorties PMC', lieu => lieu.sortiesPmc],
      ['Sorties Scav', lieu => lieu.sortiesScav],
      ['Transits', lieu => lieu.transits],
      ['Rencontres', lieu => lieu.boss],
      ['Dangers relevés', lieu => lieu.dangers],
      ['Variantes', lieu => lieu.variantes],
    ];
    grille.innerHTML = [a, b].map(lieu => {
      const dl = lignes.map(([label, lire]) => ligne(label, lire(lieu))).join('');
      return `<div class="map-compare__col"><h3>${lieu.nom}</h3><dl>${dl}</dl></div>`;
    }).join('');
  }

  champA.addEventListener('change', rendre);
  champB.addEventListener('change', rendre);
  rendre();

  const memoriser = preferences('cartes:comparatif');
  if (memoriser) {
    try {
      const choix = JSON.parse(memoriser);
      if (parSlug.has(choix?.a)) champA.value = choix.a;
      if (parSlug.has(choix?.b)) champB.value = choix.b;
      rendre();
    } catch { /* Valeur illisible : on garde les choix par défaut. */ }
  }
  const sauvegarder = () => preferences('cartes:comparatif', JSON.stringify({ a: champA.value, b: champB.value }));
  champA.addEventListener('change', sauvegarder);
  champB.addEventListener('change', sauvegarder);
}

function initFiche() {
  const racine = document.querySelector('[data-map]');
  if (!racine) return;
  // Couches : chaque pastille affiche ou masque un panneau de données.
  const bascules = [...racine.querySelectorAll('[data-layer-toggle]')];
  const panneaux = [...racine.querySelectorAll('[data-layer]')];
  const etat = preferences('cartes:couches');
  let visibles = null;
  if (etat) {
    try { visibles = JSON.parse(etat); } catch { visibles = null; }
  }
  function poser(actifs) {
    for (const panneau of panneaux) {
      const actif = actifs.includes(panneau.dataset.layer);
      panneau.hidden = !actif;
      const bascule = bascules.find(bouton => bouton.dataset.layerToggle === panneau.dataset.layer);
      if (bascule) {
        bascule.setAttribute('aria-pressed', String(actif));
        bascule.classList.toggle('badge--gold', actif);
      }
    }
  }
  const tous = panneaux.map(panneau => panneau.dataset.layer);
  // Sans préférence enregistrée, l'état par défaut est celui écrit dans le gabarit.
  const parDefaut = panneaux.filter(panneau => !panneau.hasAttribute('hidden')).map(panneau => panneau.dataset.layer);
  poser(Array.isArray(visibles) ? visibles.filter(couche => tous.includes(couche)) : parDefaut);
  for (const bascule of bascules) {
    bascule.addEventListener('click', () => {
      const couche = bascule.dataset.layerToggle;
      const actifs = panneaux.filter(panneau => !panneau.hidden).map(panneau => panneau.dataset.layer);
      const suivants = actifs.includes(couche) ? actifs.filter(item => item !== couche) : [...actifs, couche];
      poser(suivants);
      preferences('cartes:couches', JSON.stringify(suivants));
    });
  }

  // Filtre par camp sur les tableaux de sorties.
  const selecteur = racine.querySelector('[data-camp-filter]');
  if (selecteur) {
    const lignes = [...racine.querySelectorAll('[data-camp-row]')];
    selecteur.addEventListener('change', () => {
      const camp = selecteur.value;
      for (const ligne of lignes) {
        ligne.classList.toggle('map-table__row--on', camp === 'tous' || ligne.dataset.campRow === camp);
      }
    });
  }
}

initAtlas();
initFiche();
