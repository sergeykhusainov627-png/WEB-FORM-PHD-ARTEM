// pefx-scan.js — второй проход по выгрузке .pefx: полный список объектов из content.xml
// и поиск XML-структуры формы (компоненты/привязки событий) в файлах выгрузки.
// Запуск: node analiz-tep/tools/pefx-scan.js "<папка>"

const fs = require('fs');
const path = require('path');

const src = process.argv[2] || 'C:/Users/Manya/Downloads/full_env_web_form_06102026';
const outDir = path.join(__dirname, '..', 'pefx');
const content = fs.readFileSync(path.join(src, 'content.xml'), 'utf8');

// --- 1. Все OBJECT из манифеста (без привязки к NODE) ---
const objects = [];
for (const m of content.matchAll(/<OBJECT\s+([^>]*?)\/>/g)) {
	const a = {};
	for (const x of m[1].matchAll(/([A-Za-z_]+)="([^"]*)"/g)) a[x[1]] = x[2];
	objects.push(a);
}
const lines = ['# Объекты выгрузки (content.xml)', '', 'Всего OBJECT: ' + objects.length, '',
	'| KEY | ID | NAME | CLASS | PARENT |', '|---|---|---|---:|---|'];
for (const o of objects) lines.push('| ' + (o.KEY || '') + ' | `' + (o.ID || '') + '` | ' + (o.NAME || '').replace(/\|/g, '/') + ' | ' + (o.CLASS || '') + ' | ' + (o.PARENT || '') + ' |');
fs.writeFileSync(path.join(outDir, 'OBJECTS.md'), lines.join('\r\n') + '\r\n', 'utf8');

// --- 2. Что интересного среди объектов ---
const interesting = objects.filter(o => /ANALIZ|PRX_|WEB|ASSM_|FORM|HYPERLINK|TEP/i.test((o.ID || '') + ' ' + (o.NAME || '')));
console.log('=== OBJECT всего: ' + objects.length + '; интересных: ' + interesting.length);
for (const o of interesting) console.log('  CLASS=' + (o.CLASS + '    ').slice(0, 6) + ' ' + (o.ID + ' '.repeat(40)).slice(0, 40) + ' ' + (o.NAME || '').slice(0, 60));

// --- 3. Разбор XML-структуры интересных файлов ---
function scanFile(f) {
	const xml = fs.readFileSync(path.join(src, f), 'utf8');
	const tags = {};
	for (const m of xml.matchAll(/<([A-Z_][A-Z0-9_]*)(?=[\s>])/g)) tags[m[1]] = (tags[m[1]] || 0) + 1;
	const attrs = {};
	for (const m of xml.matchAll(/\s([A-Z_][A-Z0-9_]*)="/g)) attrs[m[1]] = (attrs[m[1]] || 0) + 1;
	return { tags, attrs };
}

console.log('');
console.log('=== структура файлов выгрузки (топ-теги) ===');
for (const f of fs.readdirSync(src).filter(x => /^pef\d+\.xml$/i.test(x))
	.sort((a, b) => parseInt(a.match(/\d+/)[0], 10) - parseInt(b.match(/\d+/)[0], 10))) {
	const st = fs.statSync(path.join(src, f));
	if (st.size < 5000) continue;
	const { tags, attrs } = scanFile(f);
	const top = Object.entries(tags).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([k, v]) => k + ':' + v).join(' ');
	const ev = /EVENT|COMPONENT|CMP|FORM/i.test(Object.keys(tags).join(' '));
	console.log((f + '          ').slice(0, 12) + (st.size + '      ').slice(0, 8) + (ev ? '[EVENTS?] ' : '         ') + top);
}

// --- 4. Признаки описания формы (привязки событий) во всей выгрузке ---
console.log('');
console.log('=== поиск описаний компонентов/событий формы ===');
const markers = ['COMPONENT.EVENTS', '_CMP', '<COMPONENT', 'EVENTS', 'ON_SHOW', 'OnShow', 'D101', 'FORM_XML', 'IForm'];
for (const f of fs.readdirSync(src).filter(x => /\.(xml|mod)$/i.test(x))) {
	const buf = fs.readFileSync(path.join(src, f));
	const txt = buf.toString('utf8');
	const hits = markers.filter(m => txt.includes(m));
	if (hits.length) console.log('  ' + f + ' -> ' + hits.join(', '));
}
