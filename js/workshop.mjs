// Les données et les composants de démonstration n’entrent pas dans le chargement de l’accueil.
import { initCatalogue, initComparator, initTierList } from './components/tables.mjs';

for (const [selector, handler] of [['[data-catalogue]', initCatalogue], ['[data-comparator]', initComparator], ['[data-tier-list]', initTierList]]) {
  document.querySelectorAll(selector).forEach(handler);
}
