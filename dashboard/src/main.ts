import type { Board, Phase, Problem, Source, Status, Step, Work } from './types';

function get<T extends HTMLElement = HTMLElement>(id: string): T {
  const element = document.getElementById(id);
  if (!element) throw new Error(`Missing dashboard element: ${id}`);
  return element as T;
}
function el<K extends keyof HTMLElementTagNameMap>(tag: K, className = '', text?: string): HTMLElementTagNameMap[K] {
  const element = document.createElement(tag);
  element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}
function button(text: string, className: string, action: () => void): HTMLButtonElement {
  const result = el('button', className, text); result.type = 'button'; result.addEventListener('click', action); return result;
}
function link(label: string, url: string, className = ''): HTMLAnchorElement {
  const result = el('a', className, label); result.href = url; result.target = '_blank'; result.rel = 'noopener noreferrer'; return result;
}
const board = JSON.parse(get('dashboard-data').textContent ?? '{}') as Board;
const featureMap = new Map(board.features.map(feature => [feature.id, feature]));
const names: Record<Status, string> = { planned: 'Planned', in_progress: 'In progress', blocked: 'Blocked', accepted: 'Accepted' };
function badge(status: Status | 'implemented' | 'open' | 'resolved', label?: string): HTMLElement {
  return el('span', `badge ${status}`, label ?? (Object.hasOwn(names, status) ? names[status as Status] : status === 'implemented' ? 'Implemented increment' : status === 'resolved' ? 'Resolved' : 'Open'));
}
interface State { view: 'overview' | 'phase' | 'log'; phase: number | null; q: string; status: Status | 'all'; step: string | null }
function readState(): State {
  const params = new URLSearchParams(location.hash.slice(1));
  const phase = params.has('phase') ? Number(params.get('phase')) : null;
  const valid = phase !== null && Number.isInteger(phase) && phase >= 0 && phase < board.phases.length;
  const selected = params.get('status') ?? 'all';
  return { view: valid ? 'phase' : params.get('view') === 'log' ? 'log' : 'overview', phase: valid ? phase : null,
    q: params.get('q') ?? '', status: Object.hasOwn(names, selected) ? selected as Status : 'all', step: params.get('step') };
}
let state = readState();
let issueStatus: 'all' | 'open' | 'resolved' = 'all';
function navigate(change: Partial<State>, push = true): void {
  const pageChanged = (change.view !== undefined && change.view !== state.view) || (change.phase !== undefined && change.phase !== state.phase);
  state = { ...state, step: null, ...change };
  const params = new URLSearchParams();
  if (state.view === 'phase' && state.phase !== null) params.set('phase', String(state.phase));
  if (state.view === 'log') params.set('view', 'log');
  if (state.q) params.set('q', state.q);
  if (state.status !== 'all') params.set('status', state.status);
  if (state.step) params.set('step', state.step);
  history[push ? 'pushState' : 'replaceState'](null, '', `#${params.toString()}`);
  render();
  if (pageChanged) {
    if (!state.step) window.scrollTo({ top: 0, behavior: 'auto' });
    get('content').focus({ preventScroll: true });
  }
}
function openStep(id: string): void {
  const phase = board.phases.find(item => item.steps.some(step => step.id === id));
  if (phase) navigate({ view: 'phase', phase: phase.id, step: id, q: '', status: 'all' });
}
function matches(text: string): boolean { return text.toLowerCase().includes(state.q.trim().toLowerCase()); }
function workFor(step: Step): Work[] { return board.workItems.filter(item => item.requirements.includes(step.id)); }
function problemFor(step: Step): Problem[] {
  const indirect = new Set(workFor(step).flatMap(item => item.problems));
  return board.problems.filter(item => item.requirements.includes(step.id) || indirect.has(item.id));
}
function filtered(phase: Phase): Step[] {
  return phase.steps.filter(step => (state.status === 'all' || state.status === step.status) && matches([
    phase.title, step.id, step.title, step.note, ...step.features.flatMap(id => [id, featureMap.get(id)?.title ?? '']),
    ...workFor(step).flatMap(item => [item.title, item.how]), ...problemFor(step).map(item => item.title),
  ].join(' ')));
}
function chips(ids: string[]): HTMLElement {
  const container = el('div', 'chips');
  for (const id of ids) container.append(button(id, 'chip', () => showFeature(id)));
  return container;
}
function showFeature(id: string): void {
  const feature = featureMap.get(id); if (!feature) return;
  const body = get('feature-content'); body.replaceChildren();
  body.append(el('div', 'eyebrow', 'ASSOCIATED CAPABILITY'), el('code', 'feature-code', id), el('h2', '', feature.title));
  body.querySelector('h2')?.setAttribute('id', 'feature-title');
  body.append(el('p', '', 'This is a requirement association, not an implementation claim.'), el('h3', '', 'Acceptance evidence required'), el('p', '', feature.verification), link('Open canonical feature contract →', feature.url, 'text-link'));
  get<HTMLDialogElement>('feature-dialog').showModal();
}
function sources(items: Source[]): HTMLElement {
  const row = el('div', 'source-links');
  for (const source of items) row.append(link(source.path, source.url));
  return row;
}
function workCard(item: Work): HTMLElement {
  const card = el('details', 'work-card');
  const head = el('summary', 'card-heading'); head.append(el('h4', '', `${item.id} · ${item.title}`), badge('implemented', item.kind === 'design' ? 'Design recorded' : undefined));
  card.append(head, el('div', 'section-label', 'HOW IT WAS DONE'), el('p', '', item.how), el('div', 'section-label', 'RECORDED VALIDATION'), el('p', '', item.verification), el('div', 'limitation', item.limitations), sources(item.sources));
  return card;
}
function issueCard(item: Problem): HTMLElement {
  const card = el('details', `issue-card ${item.status}`);
  const head = el('summary', 'card-heading'); head.append(el('h4', '', `${item.id} · ${item.title}`), badge(item.status));
  card.append(head, el('p', '', item.detail));
  if (item.resolution) card.append(el('div', 'section-label', 'RESOLUTION'), el('p', '', item.resolution));
  card.append(el('div', 'section-label', item.status === 'open' ? 'NEXT ACTION' : 'FOLLOW-UP'), el('p', '', item.next_action), el('p', 'provenance', item.provenance), sources(item.sources));
  return card;
}
function header(eyebrow: string, title: string, description: string): HTMLElement {
  const result = el('section', 'page-heading'); result.append(el('div', 'eyebrow', eyebrow), el('h1', '', title), el('p', 'intro', description)); return result;
}
function notice(): HTMLElement {
  return el('div', 'notice', 'Implemented increments are narrower than accepted requirements. Acceptance follows an explicit owner review of the scope, evidence and limits. Phase sizes vary; counts are not effort percentages.');
}
function stats(): HTMLElement {
  const result = el('section', 'stats'); result.setAttribute('aria-label', 'Snapshot summary');
  const values: [string, number, string][] = [
    ['Delivery phases', board.phases.length, `${board.phases.filter(p => p.status === 'accepted').length} accepted`],
    ['In progress', board.phases.filter(p => p.status === 'in_progress').length, 'Phases with active or accepted requirements'],
    ['Recorded increments', board.workItems.length, 'Code and design artifacts'],
    ['Open issues', board.problems.filter(p => p.status === 'open').length, 'Decisions and external blockers'],
  ];
  for (const [label, value, description] of values) {
    const card = el('div', 'stat'); card.append(el('span', 'stat-label', label), el('strong', '', String(value)), el('span', 'stat-description', description)); result.append(card);
  }
  return result;
}
function reset(): HTMLElement { return button('Clear filters', 'button secondary', () => navigate({ q: '', status: 'all' }, false)); }
function empty(text: string): HTMLElement {
  const result = el('div', 'empty'); result.append(el('h3', '', 'No matches'), el('p', '', text), reset()); return result;
}
function overview(): HTMLElement {
  const result = el('div', 'overview-page'); result.append(header('PROJECT OVERVIEW', 'Roadmap & implementation', 'Choose a phase. Open only the steps and evidence you need.'), stats());
  const focus = el('section', 'focus'); const focusText = el('div');
  const focusPhase = board.phases.find(phase => phase.id === board.focusPhase);
  focusText.append(el('div', 'eyebrow', 'CURRENT FOCUS'), el('h2', '', `${String(board.focusPhase).padStart(2, '0')} / ${focusPhase?.title ?? 'Development'}`), el('p', '', board.focusSummary));
  focus.append(focusText, button(`Review Phase ${String(board.focusPhase).padStart(2, '0')} →`, 'button primary', () => navigate({ view: 'phase', phase: board.focusPhase, q: '', status: 'all' }))); result.append(focus);
  const visible = board.phases.filter(phase => filtered(phase).length > 0);
  const heading = el('div', 'list-heading'); heading.append(el('h2', '', 'The delivery plan'), el('span', 'muted', `${visible.length} of ${board.phases.length} phases · ${board.phases.reduce((sum, phase) => sum + phase.steps.length, 0)} requirements`)); result.append(heading);
  if (!visible.length) result.append(empty('No phase contains a requirement matching your search and status.'));
  const grid = el('div', 'phase-grid');
  for (const phase of visible) {
    const card = el('article', `phase-card ${phase.status}`); card.dataset.testid = `phase-card-${phase.id}`;
    const top = el('div', 'card-heading'); top.append(el('span', 'phase-number', String(phase.id).padStart(2, '0')), badge(phase.status));
    const accepted = phase.steps.filter(step => step.status === 'accepted').length;
    const increments = board.workItems.filter(item => item.requirements.some(id => phase.steps.some(step => step.id === id))).length;
    card.append(top, el('h3', '', phase.title), el('p', 'phase-caption', `${accepted}/${phase.steps.length} accepted · ${increments} related records`));
    const progress = el('progress'); progress.max = phase.steps.length; progress.value = accepted; progress.setAttribute('aria-label', `Phase ${phase.id}: ${accepted} of ${phase.steps.length} requirements accepted`); card.append(progress);
    if (state.q || state.status !== 'all') card.append(el('span', 'match-count', `${filtered(phase).length} matching requirements`));
    const open = button('Review phase →', 'phase-open', () => navigate({ view: 'phase', phase: phase.id }));
    open.setAttribute('aria-label', `Open phase ${String(phase.id).padStart(2, '0')}: ${phase.title}`);
    card.append(open); grid.append(card);
  }
  result.append(grid); return result;
}
function requirement(step: Step): HTMLDetailsElement {
  const detail = el('details', 'requirement'); detail.id = `step-${step.id}`; detail.dataset.testid = step.id;
  const summary = el('summary'); summary.append(el('code', 'step-code', step.id), el('span', 'step-title', step.title), badge(step.status)); detail.append(summary);
  const body = el('div', 'requirement-body'); body.append(el('p', 'step-note', step.note), el('div', 'section-label', 'ASSOCIATED FEATURES'), chips(step.features), el('div', 'section-label', step.status === 'accepted' ? 'ACCEPTANCE EVIDENCE' : 'ACCEPTANCE STILL REQUIRED'), el('p', '', step.verification));
  if (step.acceptance) body.append(el('p', 'step-note', `Accepted by ${step.acceptance.reviewer} on ${step.acceptance.date}. ${step.acceptance.evidence}`));
  const work = workFor(step);
  if (step.status === 'planned' && work.length) body.append(el('p', 'muted', 'Related preparation is recorded below. This requirement remains planned; links to shared work do not start a phase.'));
  body.append(el('h3', '', 'Related work & evidence'));
  if (!work.length) body.append(el('p', 'muted', 'No implemented increment is recorded for this requirement.'));
  for (const item of work) body.append(workCard(item));
  const issues = problemFor(step);
  if (issues.length) { body.append(el('h3', '', 'Problems, decisions & resolutions')); for (const issue of issues) body.append(issueCard(issue)); }
  detail.append(body); return detail;
}
function phaseView(phase: Phase): HTMLElement {
  const result = el('div'); result.append(header(`PHASE ${String(phase.id).padStart(2, '0')} / ${phase.id <= 5 ? 'CORE PLATFORM' : phase.id <= 10 ? 'SECURITY & OPERATIONS' : 'ENDPOINT SERVICES'}`, phase.title, 'Open a requirement to inspect its features, work and problems.'));
  const meta = el('div', 'phase-meta'); meta.append(badge(phase.status), el('span', 'muted', `${phase.steps.filter(s => s.status === 'accepted').length} of ${phase.steps.length} requirements accepted`), link('Canonical specification →', phase.url, 'text-link')); result.append(meta, notice());
  const architecture = el('details', 'design-notes'); const summary = el('summary', '', 'Design, dependencies & operational constraints'); architecture.append(summary);
  const notes = el('div', 'notes-body');
  for (const name of ['Scope and entry', 'Design and interfaces', 'Data and lifecycle', 'Security and failure handling', 'Capacity and operations', 'Dependencies and traceability']) {
    notes.append(el('h3', '', name), el('p', '', phase.sections[name] ?? ''));
  }
  notes.append(el('p', 'muted', `Accountable roles: ${phase.owner}`)); architecture.append(notes); result.append(architecture);
  const featureDetails = el('details', 'design-notes'); featureDetails.append(el('summary', '', `${phase.features.length} associated capabilities`), chips(phase.features)); result.append(featureDetails);
  const steps = filtered(phase);
  const listHead = el('div', 'list-heading');
  const toggle = button('Expand all', 'button secondary compact', () => {
    const details = [...result.querySelectorAll<HTMLDetailsElement>('.requirement')];
    const open = !details.every(item => item.open); for (const item of details) item.open = open;
  });
  toggle.disabled = steps.length === 0;
  listHead.append(el('h2', '', 'Requirements & acceptance'), el('span', 'muted', `${steps.length} of ${phase.steps.length} shown`), toggle); result.append(listHead);
  result.addEventListener('toggle', () => {
    const details = [...result.querySelectorAll<HTMLDetailsElement>('.requirement')];
    const all = details.length > 0 && details.every(item => item.open);
    toggle.textContent = all ? 'Collapse all' : 'Expand all'; toggle.setAttribute('aria-expanded', String(all));
  }, true);
  if (!steps.length) result.append(empty('No requirements match the current filters.'));
  for (const step of steps) result.append(requirement(step));
  const issues = board.problems.filter(item => item.phases.includes(phase.id));
  if (issues.length) { result.append(el('h2', 'section-heading', 'Phase-wide problems & decisions')); for (const issue of issues) result.append(issueCard(issue)); }
  else result.append(el('p', 'muted', 'No phase-specific incident is recorded. Entry dependencies and acceptance gates still apply.'));
  return result;
}
function logView(): HTMLElement {
  const result = el('div'); result.append(header('IMPLEMENTATION JOURNAL', 'Evidence, decisions & lessons', 'Recorded work explains what was built, how it was verified, and its limits. Resolved setup issues are retained alongside open blockers.'), notice());
  const work = board.workItems.filter(item => matches([item.id, item.title, item.how, item.verification, ...item.requirements].join(' ')));
  result.append(el('h2', 'section-heading', `Recorded increments (${work.length})`));
  for (const item of work) {
    const card = workCard(item); const related = el('div', 'chips');
    for (const id of item.requirements) related.append(button(id, 'chip', () => openStep(id))); card.append(related); result.append(card);
  }
  const controls = el('div', 'list-heading'); controls.append(el('h2', '', 'Problems encountered'));
  const group = el('div', 'segments'); group.setAttribute('role', 'group'); group.setAttribute('aria-label', 'Problem status');
  for (const status of ['all', 'open', 'resolved'] as const) {
    const control = button(status === 'all' ? 'All issues' : status === 'open' ? 'Open' : 'Resolved', 'segment', () => { issueStatus = status; render(); });
    control.setAttribute('aria-pressed', String(issueStatus === status)); group.append(control);
  }
  controls.append(group); result.append(controls);
  const problems = board.problems.filter(item => (issueStatus === 'all' || issueStatus === item.status) && matches([item.id, item.title, item.detail, item.resolution, item.next_action].join(' ')));
  for (const problem of problems) result.append(issueCard(problem));
  if (!work.length && !problems.length) result.append(empty('No implementation record or problem matches this search.'));
  return result;
}
function renderNav(): void {
  for (const [id, view] of [['overview-tab', 'overview'], ['log-tab', 'log']]) {
    const tab = get(id ?? ''); if (state.view === view) tab.setAttribute('aria-current', 'page'); else tab.removeAttribute('aria-current');
  }
}
function render(): void {
  renderNav();
  get<HTMLInputElement>('search').value = state.q;
  get<HTMLSelectElement>('status').value = state.status;
  get('status-field').hidden = state.view === 'log';
  get<HTMLSelectElement>('mobile-phase').value = state.view === 'phase' ? `phase:${state.phase}` : state.view;
  const current = board.phases.find(phase => phase.id === state.phase);
  get('content').replaceChildren(state.view === 'log' ? logView() : state.view === 'phase' && current ? phaseView(current) : overview());
  get('announcer').textContent = state.view === 'phase' && current ? `Phase ${current.id}: ${filtered(current).length} requirements shown` : state.view === 'log' ? 'Implementation journal displayed' : 'Delivery phase board displayed';
  if (state.step && /^P\d{2}-\d{2}$/.test(state.step)) {
    const target = document.getElementById(`step-${state.step}`);
    if (target instanceof HTMLDetailsElement) { target.open = true; target.scrollIntoView({ block: 'start' }); }
  }
}
get('overview-tab').addEventListener('click', () => navigate({ view: 'overview', phase: null }));
get('log-tab').addEventListener('click', () => navigate({ view: 'log', phase: null }));
get<HTMLInputElement>('search').addEventListener('input', event => navigate({ q: (event.target as HTMLInputElement).value }, false));
get<HTMLSelectElement>('status').addEventListener('change', event => navigate({ status: (event.target as HTMLSelectElement).value as State['status'] }, false));
get('close-dialog').addEventListener('click', () => get<HTMLDialogElement>('feature-dialog').close());
const picker = get<HTMLSelectElement>('mobile-phase');
for (const [value, label] of [['overview', 'Phase board'], ['log', 'Implementation & issues'], ...board.phases.map(p => [`phase:${p.id}`, `${String(p.id).padStart(2, '0')} · ${p.title}`])]) {
  const option = el('option', '', label); option.value = value ?? ''; picker.append(option);
}
picker.addEventListener('change', () => picker.value.startsWith('phase:') ? navigate({ view: 'phase', phase: Number(picker.value.split(':')[1]) }) : navigate({ view: picker.value as 'overview' | 'log', phase: null }));
get('download').addEventListener('click', () => {
  const url = URL.createObjectURL(new Blob([JSON.stringify(board, null, 2)], { type: 'application/json' }));
  const anchor = el('a'); anchor.href = url; anchor.download = `babel-progress-${board.snapshot.date}.json`; anchor.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
});
get('snapshot-short').textContent = `Snapshot ${board.snapshot.date} · ${board.snapshot.commit.slice(0, 7)}`;
const footer = get('footer');
footer.append(el('span', '', `Evidence snapshot: ${board.snapshot.date} · ${board.snapshot.commit.slice(0, 7)}. `), link(`Evidence snapshot CI: ${board.snapshot.ci_result} · ${board.snapshot.checks_passed} passing checks →`, board.snapshot.ci_url), el('p', '', board.snapshot.note), el('small', '', `Design build ${board.buildRevision.slice(0, 7)} · Offline report; no live GitHub connection.`));
window.addEventListener('popstate', () => { state = readState(); render(); });
window.addEventListener('hashchange', () => { state = readState(); render(); });
render();
