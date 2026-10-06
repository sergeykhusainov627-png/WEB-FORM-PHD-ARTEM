// pefx-extract.js — разбор выгрузки окружения Форсайт (.pefx / папка с content.xml + pefN.xml).
// Запуск: node analiz-tep/tools/pefx-extract.js "<папка с распакованным .pefx>"
// Что делает:
//   1) читает content.xml и строит карту: файл pefN.xml -> объект репозитория (KEY/ID/NAME/CLASS/PARENT);
//   2) из каждого pefN.xml вытаскивает текст модуля из <T><![CDATA[ ... ]]></T> в analiz-tep/pefx/pefN.fore;
//   3) собирает ссылки на сборки (<AT RE="...">) и мета-объект (<O I= N= D= S=>);
//   4) пишет analiz-tep/pefx/INDEX.md — сводную таблицу.

const fs = require('fs');
const path = require('path');

const src = process.argv[2] || 'C:/Users/Manya/Downloads/full_env_web_form_06102026';
const outDir = path.join(__dirname, '..', 'pefx');
fs.mkdirSync(outDir, { recursive: true });

// --- 1. content.xml -> карта файлов ---
const content = fs.readFileSync(path.join(src, 'content.xml'), 'utf8');
const meta = new Map(); // pefN -> {id,name,cls,parent,key,oi,on}
{
	// Идём по документу последовательно: FILE_NAME_TAG="pefN" ... <OBJECT KEY=... ID=... NAME=... CLASS=.../>
	const re = /FILE_NAME_TAG="(pef\d+)"[\s\S]*?<OBJECT\s+([^>]*?)\/>/g;
	let m;
	while ((m = re.exec(content)) !== null) {
		const file = m[1];
		const attrs = {};
		for (const a of m[2].matchAll(/([A-Za-z_]+)="([^"]*)"/g)) attrs[a[1]] = a[2];
		if (!meta.has(file)) {
			meta.set(file, {
				id: attrs.ID || '', name: attrs.NAME || '', cls: attrs.CLASS || '',
				parent: attrs.PARENT || '', key: attrs.KEY || '',
				oi: (m[0].match(/OI="([^"]*)"/) || [])[1] || '',
				on: (m[0].match(/\sON="([^"]*)"/) || [])[1] || ''
			});
		}
	}
}

// --- 2. разбор pefN.xml ---
const rows = [];
const files = fs.readdirSync(src).filter(f => /^pef\d+\.xml$/i.test(f))
	.sort((a, b) => parseInt(a.match(/\d+/)[0], 10) - parseInt(b.match(/\d+/)[0], 10));

for (const f of files) {
	const xml = fs.readFileSync(path.join(src, f), 'utf8');
	const tag = f.replace(/\.xml$/i, '');
	const m = meta.get(tag) || {};

	// текст модуля
	const cdata = [...xml.matchAll(/<T><!\[CDATA\[([\s\S]*?)\]\]><\/T>/g)].map(x => x[1]);
	const code = cdata.join('\n');

	// объект-владелец и ссылки
	const obj = (xml.match(/<O\s+I="([^"]*)"\s+N="([^"]*)"(?:\s+D="([^"]*)")?(?:\s+S="([^"]*)")?\s*\/>/) || []);
	const refs = (xml.match(/<AT\s+RE="([^"]*)"/) || [])[1] || '';

	if (code.trim() !== '') fs.writeFileSync(path.join(outDir, tag + '.fore'), code, 'utf8');

	// что объявлено в модуле
	const decls = [...code.matchAll(/^\s*(?:Public\s+|Private\s+|Friend\s+)?(Class|Interface|Enum|Delegate)\s+([A-Za-z_][A-Za-z0-9_]*)/gm)]
		.map(x => x[1] + ' ' + x[2]);
	const consts = [...code.matchAll(/^\s*(?:Public\s+)?Const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=/gm)].map(x => x[1]);
	const subs = [...code.matchAll(/^\s*(?:Public\s+|Private\s+|Shared\s+)*?(Sub|Function)\s+([A-Za-z_][A-Za-z0-9_]*)/gm)].map(x => x[2]);

	rows.push({
		file: tag, bytes: Buffer.byteLength(xml, 'utf8'),
		objId: m.id || obj[1] || '', objName: m.name || obj[2] || '', cls: m.cls || '', parent: m.parent || '',
		owner: obj[1] ? obj[1] + ' / ' + obj[2] : '', refs,
		codeLines: code === '' ? 0 : code.split(/\r?\n/).length,
		decls, consts, subs, hasCode: code.trim() !== ''
	});
}

// --- 3. INDEX.md ---
const L = [];
L.push('# Выгрузка окружения `.pefx` — карта объектов');
L.push('');
L.push('Источник: `' + src + '`');
L.push('Объектов в `content.xml`: ' + meta.size + '; разобрано файлов: ' + files.length +
	'; с текстом модуля: ' + rows.filter(r => r.hasCode).length);
L.push('');
const byClass = {};
for (const r of rows) { const k = r.cls || '?'; byClass[k] = (byClass[k] || 0) + 1; }
L.push('Распределение по `CLASS` из манифеста: ' + Object.entries(byClass).map(([k, v]) => k + '→' + v).join(', '));
L.push('');
L.push('| файл | объект (ID) | название | CLASS | строк кода | что объявлено |');
L.push('|---|---|---|---:|---:|---|');
for (const r of rows) {
	const decl = r.decls.length ? r.decls.join('; ') : (r.hasCode ? '— (без Class/Interface)' : '(без текста)');
	L.push('| ' + r.file + ' | `' + r.objId + '` | ' + (r.objName || '').replace(/\|/g, '/') + ' | ' + r.cls + ' | ' + r.codeLines + ' | ' + decl.replace(/\|/g, '/') + ' |');
}
L.push('');
L.push('## Модули с исходниками (выгружены в `analiz-tep/pefx/<файл>.fore`)');
L.push('');
for (const r of rows.filter(x => x.hasCode)) {
	L.push('* **' + r.file + '** — `' + r.objId + '` «' + r.objName + '»: ' + (r.decls.join('; ') || 'Class/Interface не найден'));
}
L.push('');
fs.writeFileSync(path.join(outDir, 'INDEX.md'), L.join('\r\n') + '\r\n', 'utf8');

console.log('объектов в манифесте: ' + meta.size + ', файлов: ' + files.length + ', с кодом: ' + rows.filter(r => r.hasCode).length);
console.log('извлечено .fore: ' + rows.filter(r => r.hasCode).length + ' -> ' + outDir);
for (const r of rows) {
	if (r.decls.some(d => /Class/.test(d)) || r.objName)
		console.log((r.file + '          ').slice(0, 12) + ' CLASS=' + (r.cls + '   ').slice(0, 5) + ' ' +
			(r.objId + '                              ').slice(0, 32) + ' ' + (r.objName + '                              ').slice(0, 34) +
			' ' + (r.decls.join('; ') || '').slice(0, 60));
}
