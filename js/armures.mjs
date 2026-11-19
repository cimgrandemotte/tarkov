/** Pages Armures et Boss : filtres du catalogue d’armure, comparateur à
 *  trois entrées, filtres de famille de boss et mémorisation des préférences.
 *  Aucune requête réseau : les données sont intégrées au HTML ou lues dans
 *  le script JSON embarqué par le rendu des pages. */
import { preferences } from './components/ui.mjs';

const normaliser = valeur => String(valeur ?? '')
  .toLowerCase()
  .normalize('NFD')
  .replace(/[\u0300-\u036f]/g, '');

const nombreFr = valeur => (typeof valeur === 'number' && Number.isFinite(valeur)
  ? valeur.toLocaleString('fr-FR')
  : '—');

const pourcentFr = valeur => (typeof valeur === 'number' && Number.isFinite(valeur)
  ? `${Math.round(valeur * 100)}\u202f%`
  : '—');

const poidsFr = valeur => (typeof valeur === 'number' && Number.isFinite(valeur)
  ? `${valeur.toLocaleString('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}\u202fkg`
  : '—');

function alimenter(selecteur, valeurs) {
  const champ = document.querySelector(selecteur);
  if (!champ) return;
  // La première option sert de valeur « toutes » : son libellé est conservé.
  const premier = champ.querySelector('option');
  const modele = premier ? premier.outerHTML : '<option value=""></option>';
  champ.innerHTML = modele;
  for (const [valeur, libelle] of valeurs) {
    const option = document.createElement('option');
    option.value = valeur;
    option.textContent = libelle;
    champ.append(option);
  }
}

/* ------------------------------------------------------------------ */
/* Catalogue d'armure : filtres et sélection pour le comparateur.      */
/* ------------------------------------------------------------------ */

function initCatalogueArmure() {
  const table = document.querySelector('#armures-catalogue, #armures-comparateur');
  if (!table) return;
  const corps = table.tBodies[0];
  const lignes = [...corps.rows];
  const recherche = document.querySelector('[data-armures-search]');
  const categorie = document.querySelector('[data-armures-categorie]');
  const classe = document.querySelector('[data-armures-classe]');
  const materiau = document.querySelector('[data-armures-materiau]');
  const poids = document.querySelector('[data-armures-poids]');
  const plaques = document.querySelector('[data-armures-plaques]');
  const compte = document.querySelector('[data-armures-compte]');

  const categories = [...new Set(lignes.map(l => l.dataset.categorie).filter(Boolean))].sort();
  const materiaux = [...new Set(lignes.map(l => l.dataset.materiau).filter(Boolean))].sort();
  alimenter('[data-armures-categorie]', categories.map(c => [c, c]));
  alimenter('[data-armures-materiau]', materiaux.map(m => [m, m]));

  function appliquer() {
    const terme = normaliser(recherche?.value ?? '');
    const categorieChoisie = categorie?.value ?? '';
    const classeChoisie = classe?.value ?? 'toutes';
    const materiauChoisi = materiau?.value ?? 'tous';
    const poidsMax = poids?.value ? Number(poids.value) : null;
    const plaquesChoisies = plaques?.value ?? 'toutes';
    let visibles = 0;
    for (const ligne of lignes) {
      const texte = normaliser(ligne.dataset.nom ?? '');
      const poidsLigne = ligne.dataset.poids === '' ? null : Number(ligne.dataset.poids);
      const correspond = (!terme || texte.includes(terme))
        && (!categorieChoisie || ligne.dataset.categorie === categorieChoisie)
        && (classeChoisie === 'toutes' || ligne.dataset.classe === classeChoisie)
        && (materiauChoisi === 'tous' || ligne.dataset.materiau === materiauChoisi)
        && (poidsMax === null || (poidsLigne !== null && poidsLigne <= poidsMax))
        && (plaquesChoisies === 'toutes' || ligne.dataset.plaques === plaquesChoisies);
      ligne.hidden = !correspond;
      if (correspond) visibles += 1;
    }
    if (compte) {
      compte.textContent = `${visibles} ${visibles > 1 ? 'pièces affichées' : 'pièce affichée'} sur ${lignes.length}`;
    }
  }

  for (const champ of [recherche, categorie, classe, materiau, poids, plaques]) {
    champ?.addEventListener('input', appliquer);
    champ?.addEventListener('change', appliquer);
  }
  appliquer();
  return lignes;
}

/* ------------------------------------------------------------------ */
/* Comparateur d'armures : deux à trois pièces sur les mêmes colonnes. */
/* ------------------------------------------------------------------ */

const COLONNES_COMPARE = [
  { cle: 'categorie', titre: 'Catégorie', valeur: piece => piece.categorie || '—' },
  { cle: 'classe', titre: 'Classe', valeur: piece => (piece.classe ? `Classe ${piece.classe}` : 'Sans classe') },
  { cle: 'materiau', titre: 'Matériau', valeur: piece => piece.materiau || 'Non relevé' },
  { cle: 'duree', titre: 'Durabilité', valeur: piece => nombreFr(piece.duree) },
  { cle: 'zones', titre: 'Zones couvertes', valeur: piece => nombreFr(piece.zones.length) },
  { cle: 'poids', titre: 'Poids', valeur: piece => poidsFr(piece.poids) },
  { cle: 'prix', titre: 'Prix de base', valeur: piece => (piece.prixBase ? `${nombreFr(piece.prixBase)}\u202f₽` : '—') },
  {
    cle: 'plaques',
    titre: 'Emplacements à plaques',
    valeur: piece => `${piece.emplacements.filter(e => e.plaquesAutorisees).length} / ${piece.emplacements.length}`,
  },
  {
    cle: 'classeMax',
    titre: 'Classe maximale acceptée',
    valeur: piece => {
      const classes = piece.emplacements.map(e => e.classeMax).filter(v => v !== null && v !== undefined);
      return classes.length ? `${Math.min(...classes)} – ${Math.max(...classes)}` : '—';
    },
  },
  { cle: 'vitesse', titre: 'Pénalité de vitesse', valeur: piece => (piece.penaliteVitesse === null ? '—' : `${Math.round(piece.penaliteVitesse * 100)}\u202f%`) },
  { cle: 'rotation', titre: 'Pénalité de rotation', valeur: piece => (piece.penaliteRotation === null ? '—' : `${Math.round(piece.penaliteRotation * 100)}\u202f%`) },
  { cle: 'ergonomie', titre: 'Pénalité d’ergonomie', valeur: piece => (piece.penaliteErgonomie === null ? '—' : `${Math.round(piece.penaliteErgonomie * 100)}\u202f%`) },
  { cle: 'capacite', titre: 'Capacité de rangement', valeur: piece => nombreFr(piece.capacite) },
  { cle: 'ricochet', titre: 'Ricochet (z)', valeur: piece => (piece.ricochet && piece.ricochet.z ? `${piece.ricochet.z}\u202f%` : '—') },
  { cle: 'audio', titre: 'Bloque le casque audio', valeur: piece => (piece.bloqueCasqueAudio ? 'Oui' : 'Non') },
  { cle: 'lunettes', titre: 'Bloque les lunettes', valeur: piece => (piece.bloqueLunettes ? 'Oui' : 'Non') },
];

function initComparateurArmure() {
  const bloc = document.querySelector('[data-armures-compare]');
  if (!bloc) return;
  const selects = [...bloc.querySelectorAll('[data-armures-compare-slot]')];
  const grille = bloc.querySelector('[data-armures-compare-grille]');
  const etat = bloc.querySelector('[data-armures-compare-compte]');
  if (!selects.length || !grille) return;

  let pieces = [];
  try {
    const source = document.querySelector('script[data-armures-json]');
    pieces = source ? JSON.parse(source.textContent) ?? [] : [];
  } catch { pieces = []; }
  if (!pieces.length) return;

  const parId = new Map(pieces.map(piece => [piece.id, piece]));
  const options = pieces
    .slice()
    .sort((a, b) => a.categorie.localeCompare(b.categorie, 'fr') || a.nom.localeCompare(b.nom, 'fr'))
    .map(piece => [piece.id, `${piece.categorie} — ${piece.nom}`]);

  selects.forEach((select, index) => {
    alimenter(`[data-armures-compare-slot="${index + 1}"]`, options);
    const memorise = preferences(`armure-compare-${index + 1}`);
    if (memorise && parId.has(memorise)) select.value = memorise;
    select.addEventListener('change', () => {
      preferences(`armure-compare-${index + 1}`, select.value);
      rendre();
    });
  });

  function rendre() {
    const choisies = selects.map(select => parId.get(select.value)).filter(Boolean);
    if (etat) {
      etat.textContent = `${choisies.length} ${choisies.length > 1 ? 'pièces sélectionnées' : 'pièce sélectionnée'} sur ${choisies.length || 0}.`;
    }
    if (choisies.length < 2) {
      grille.innerHTML = '<p class="armures-note">Choisissez au moins deux pièces pour lancer la comparaison.</p>';
      return;
    }
    const entetes = choisies
      .map(piece => `<div class="armures-compare__valeur armures-compare__entete">${piece.nom}</div>`)
      .join('');
    const lignes = COLONNES_COMPARE.map(colonne => {
      const valeurs = choisies
        .map(piece => {
          const brut = colonne.valeur(piece);
          const vide = brut === '—' || brut === null || brut === undefined;
          return `<div class="armures-compare__valeur" data-vide="${vide ? 'oui' : 'non'}">${brut ?? '—'}</div>`;
        })
        .join('');
      return `<div class="armures-compare__ligne"><div>${colonne.titre}</div>${valeurs}</div>`;
    }).join('');
    grille.innerHTML = `<div class="armures-compare__ligne"><div>Caractéristique</div>${entetes}</div>${lignes}`;
  }

  rendre();
}

/* ------------------------------------------------------------------ */
/* Grille de boss : filtre par famille.                                 */
/* ------------------------------------------------------------------ */

function initGrilleBoss() {
  const grille = document.querySelector('[data-boss-grid]');
  if (!grille) return;
  const cartes = [...grille.querySelectorAll('[data-boss-card]')];
  const boutons = [...document.querySelectorAll('[data-boss-famille]')];
  const compte = document.querySelector('[data-boss-compte]');

  function appliquer(famille) {
    let visibles = 0;
    for (const carte of cartes) {
      const correspond = famille === 'toutes' || carte.dataset.famille === famille;
      carte.hidden = !correspond;
      if (correspond) visibles += 1;
    }
    for (const bouton of boutons) {
      bouton.setAttribute('aria-pressed', String(bouton.dataset.bossFamille === famille));
    }
    if (compte) {
      compte.textContent = `${visibles} ${visibles > 1 ? 'fiches affichées' : 'fiche affichée'} sur ${cartes.length}`;
    }
  }

  for (const bouton of boutons) {
    bouton.addEventListener('click', () => appliquer(bouton.dataset.bossFamille));
  }
  appliquer('toutes');
}

/* ------------------------------------------------------------------ */

function init() {
  initCatalogueArmure();
  initComparateurArmure();
  initGrilleBoss();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
