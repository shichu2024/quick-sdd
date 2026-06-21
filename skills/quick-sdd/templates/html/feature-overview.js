/* Quick SDD Feature Overview — Canonical JS Template
 * Source of truth: skills/quick-sdd/templates/html/feature-overview.js
 */
function setActive(el) {
  document.querySelectorAll('.sidebar-nav a').forEach(a => a.classList.remove('active'));
  el.classList.add('active');
  if (window.innerWidth <= 860) document.getElementById('sidebar').classList.remove('open');
}

function toggleDetail(btn) {
  btn.classList.toggle('open');
  btn.closest('.card').querySelector('.task-detail').classList.toggle('open');
}

const secs = document.querySelectorAll('[id]');
const links = document.querySelectorAll('.sidebar-nav a[href^="#"]');
const obs = new IntersectionObserver(es => {
  es.forEach(e => {
    if (e.isIntersecting) {
      const id = e.target.getAttribute('id');
      links.forEach(l => { l.classList.toggle('active', l.getAttribute('href') === '#' + id); });
    }
  });
}, { rootMargin: '-80px 0px -60% 0px', threshold: 0 });
secs.forEach(s => obs.observe(s));

const backTop = document.getElementById('backTop');
window.addEventListener('scroll', () => { backTop.classList.toggle('show', window.scrollY > 400); }, { passive: true });
