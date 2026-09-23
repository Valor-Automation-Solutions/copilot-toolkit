const assert = require('node:assert/strict');
const fs = require('node:fs');

require('./frontier-public.js');
const selector = globalThis.FrontierPublic;
const indexed = JSON.parse(fs.readFileSync(__dirname + '/frontier-public-index.json', 'utf8')).items;
const added = {
  id: 's6-new', session: 'מושב 6', title: 'נציגת שירות במוקד מטפלת בפניות',
  what: 'נציגת שירות ממיינת פניות חדשות.',
  detail: 'צוות השירות בודק את הטיפול בלקוח.',
  text: 'נציגת שירות במוקד מטפלת בפניות. נציגת שירות ממיינת פניות חדשות.',
  source: 'https://guycoful.github.io/microsoft-frontier-2026/#s6'
};
const selected = selector.rank(indexed.concat(added), 'נציגת שירות');
assert(selected.length <= 5);
assert(selected.some(item => item.id === added.id), 'A newly indexed public section must appear');
assert.equal(selector.decision(added, {}).label, 'דורש תקציב או אישור');
assert.equal(selector.decision({...added, title: 'Copilot Credits', what: 'נדרשים Copilot Credits.'}, {credits: 'excluded'}).label, 'לא רלוונטי לנו');
console.log('Public selector acceptance checks passed');
