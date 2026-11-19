import { initDialogs, initNavigation, initPreferences, initTabs, initTooltip } from './components/ui.mjs';
import { initSearch } from './components/search.mjs';
import { initAudio } from './components/audio.mjs';
import { initMotion, initReveal } from './components/motion.mjs';
import { initSitePanels, initChecklist } from './components/site-panels.mjs';

initNavigation();
initPreferences();
const dialogs = initDialogs();
initSearch(document.querySelector('#search-dialog'), dialogs.get('search-dialog'));
const activate = (selector, handler) => document.querySelectorAll(selector).forEach(handler);
activate('[data-tabs]', initTabs);
activate('[data-tooltip]', initTooltip);
initSitePanels();
activate('[data-checklist]', initChecklist);
activate('[data-audio-player]', initAudio);
activate('[data-hero-motion]', initMotion);
initReveal();

