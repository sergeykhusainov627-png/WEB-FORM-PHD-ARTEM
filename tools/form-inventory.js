// form-inventory.js — инвентаризация .fore-модуля веб-формы (ANALIZ_TEP_FORM_ON_SHOW).
// Запуск: node analiz-tep/tools/form-inventory.js [путь-к-модулю]
// Печатает: контролы по типам, обработчики (и пустые), соответствие «контрол ↔ обработчик»,
// константы C_PARAM_* и их фактическое использование в живом коде, параметры, уходящие в гиперссылку,
// поля p_* и статистику по коду/отладке.

const fs = require('fs');
const path = require('path');

const file = process.argv[2] || 'C:/Users/Manya/Downloads/backup.txt';
const text = fs.readFileSync(file, 'utf8');
const lines = text.split(/\r?\n/);

// --- разметка строк: код / комментарий / внутри { } ---
const kind = []; // 'code' | 'comment' | 'brace' | 'blank'
let inBrace = false;
lines.forEach(raw => {
	const line = raw.trim();
	if (inBrace) { kind.push('brace'); if (line.includes('}')) inBrace = false; return; }
	if (line === '') return kind.push('blank');
	if (line.startsWith('//')) return kind.push('comment');
	const o = (line.match(/\{/g) || []).length, c = (line.match(/\}/g) || []).length;
	if (o > c) { inBrace = true; return kind.push('brace'); }
	kind.push('code');
});

// --- 1. Объявления контролов (строки вида "Имя: Тип;" до первого Sub/Function/Property) ---
const controls = [];
let declEnded = false;
lines.forEach((raw, i) => {
	const line = raw.trim();
	if (/^(Sub|Function|Property)\b/i.test(line)) declEnded = true;
	if (!declEnded && kind[i] === 'code') {
		const m = line.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*([A-Za-z_][A-Za-z0-9_]*)\s*;\s*$/);
		if (m) controls.push({ name: m[1], type: m[2], line: i + 1 });
	}
});

// --- 2. Обработчики: Sub/Function верхнего уровня класса (с учётом вложенных — по отступу) ---
const handlers = [];
lines.forEach((raw, i) => {
	if (kind[i] !== 'code') return;
	const m = raw.match(/^\t(Sub|Function)\s+([A-Za-z_][A-Za-z0-9_]*)/);
	if (m) handlers.push({ kind: m[1], name: m[2], line: i + 1 });
});
// тело обработчика: от "Begin" до "End Sub/Function <имя>"
handlers.forEach(h => {
	const endRe = new RegExp('^\\tEnd\\s+' + h.kind + '\\s+' + h.name + '\\s*;', 'i');
	const endIdx = lines.findIndex((l, i) => i > h.line - 1 && endRe.test(l));
	const body = lines.slice(h.line, endIdx === -1 ? lines.length : endIdx);
	h.bodyLines = body.filter((l, i) => {
		const t = l.trim();
		const gi = h.line + i;
		return t !== '' && kind[gi] !== 'comment' && kind[gi] !== 'brace' &&
			!/^(Begin|Var|Const|End\s+(Sub|Function)\b)/i.test(t) && !/^[A-Za-z_][A-Za-z0-9_]*\s*:\s*[A-Za-z_][A-Za-z0-9_]*\s*;?$/.test(t);
	});
	h.empty = h.bodyLines.length === 0;
});

// --- 3. Соответствие контрол ↔ обработчик ---
const handlerNames = handlers.map(h => h.name);
const matched = new Map();
for (const c of controls) {
	const cand = handlerNames.filter(h => h.startsWith(c.name) && h.length > c.name.length).sort((a, b) => b.length - a.length);
	if (cand.length) matched.set(c.name, cand[0]);
}
const handlerToControl = new Map();
for (const [ctrl, h] of matched) {
	if (!handlerToControl.has(h)) handlerToControl.set(h, []);
	handlerToControl.get(h).push(ctrl);
}
const orphanHandlers = handlers.filter(h => !handlerToControl.has(h.name));

// --- 4. Константы C_PARAM_*: использование только в живом коде ---
const consts = [];
lines.forEach((raw, i) => {
	if (kind[i] === 'comment' || kind[i] === 'brace') return;
	const m = raw.trim().match(/^Const\s+(C_[A-Z0-9_]+)\s*=\s*"([^"]*)"/);
	if (m) consts.push({ name: m[1], value: m[2], line: i + 1 });
});
const liveCode = lines.filter((l, i) => kind[i] === 'code').join('\n');
const constsUses = consts.map(c => ({ ...c, uses: (liveCode.match(new RegExp('\\b' + c.name + '\\b', 'g')) || []).length - 1 }));

// --- 5. Параметры, уходящие в гиперссылку (живой код) ---
const sentParams = new Map();
function push(k, lineNo, how) {
	if (!sentParams.has(k)) sentParams.set(k, []);
	sentParams.get(k).push(how + '@' + lineNo);
}
lines.forEach((raw, i) => {
	if (kind[i] !== 'code') return;
	const line = raw.trim();
	let m;
	if ((m = line.match(/UpdateOpenDefHlinkFromSelection\(\s*"([^"]+)"/))) push(m[1], i + 1, 'UPD');
	if ((m = line.match(/Hyperlink\.SetParamValueFromSelection\(\s*"([^"]+)"/))) push(m[1], i + 1, 'SetParamsFromSel');
	if ((m = line.match(/SetParamValue\(\s*(C_PARAM_[A-Z0-9_]+|"[^"]+")/))) {
		const raw2 = m[1];
		const c = consts.find(x => x.name === raw2);
		push(c ? c.value : raw2.replace(/"/g, ''), i + 1, 'SetParamValue');
	}
});

// --- 6. Поля p_* : присваивание и использование ---
const pFields = [];
lines.forEach((raw, i) => {
	if (kind[i] !== 'code') return;
	const m = raw.trim().match(/^(p_[a-z0-9_]+)\s*:\s*Variant\s*;/i);
	if (m) pFields.push({ name: m[1], line: i + 1, assign: 0, read: 0 });
});
for (const f of pFields) {
	lines.forEach((raw, i) => {
		if (kind[i] !== 'code') return;
		const re = new RegExp('\\b' + f.name + '\\b', 'g');
		const n = (raw.match(re) || []).length;
		if (n === 0) return;
		if (new RegExp('\\b' + f.name + '\\s*:=', 'i').test(raw)) f.assign += n;
		else f.read += n;
	});
}

// --- 7. Вывод ---
const out = [];
const p = s => out.push(s);
const byType = {};
for (const c of controls) (byType[c.type] = byType[c.type] || []).push(c.name);

const stat = t => kind.filter(k => k === t).length;
p('=== ФАЙЛ: ' + file);
p('строк: ' + lines.length + ' | кода: ' + stat('code') + ' | // комментариев: ' + stat('comment') +
	' | строк в { }-комментариях: ' + stat('brace') + ' | пустых: ' + stat('blank'));
p('строк с TextArea1 (отладочный вывод вживую): ' + lines.filter((l, i) => kind[i] === 'code' && /TextArea1/.test(l)).length);
p('');
p('=== КОНТРОЛЫ ПО ТИПАМ (всего ' + controls.length + ')');
for (const t of Object.keys(byType).sort()) p('  ' + t + ' — ' + byType[t].length + ': ' + byType[t].join(', '));
p('');
p('=== ОБРАБОТЧИКИ (всего ' + handlers.length + ': Sub ' + handlers.filter(h => h.kind === 'Sub').length +
	', Function ' + handlers.filter(h => h.kind === 'Function').length + '); пустых: ' + handlers.filter(h => h.empty).length);
for (const h of handlers.filter(h => h.empty)) p('  ПУСТОЙ: ' + h.kind + ' ' + h.name + ' (стр. ' + h.line + ')');
p('');
const noHandler = controls.filter(c => !matched.has(c.name));
p('=== КОНТРОЛЫ БЕЗ ОБРАБОТЧИКА (' + noHandler.length + ' из ' + controls.length + ')');
for (const c of noHandler) p('  ' + c.type + ' ' + c.name + ' (стр. ' + c.line + ')');
p('');
p('=== ОБРАБОТЧИКИ БЕЗ КОНТРОЛА (' + orphanHandlers.length + ')');
for (const h of orphanHandlers) p('  ' + h.kind + ' ' + h.name + ' (стр. ' + h.line + ')');
p('');
p('=== КОНСТАНТЫ C_PARAM_* (' + consts.length + '), использование в ЖИВОМ коде:');
for (const c of constsUses) p('  ' + (c.uses > 0 ? '[+]' : '[ ]') + ' ' + c.name + ' = "' + c.value + '" — ' + c.uses);
p('');
p('=== ПАРАМЕТРЫ, РЕАЛЬНО УХОДЯЩИЕ В ГИПЕРССЫЛКУ (' + sentParams.size + ')');
for (const [k, v] of [...sentParams.entries()].sort()) p('  ' + k.padEnd(14) + ' ← ' + v.join(', '));
p('');
p('=== ПОЛЯ p_* (всего ' + pFields.length + '): присваиваний / чтений в живом коде');
for (const f of pFields) p('  ' + f.name.padEnd(18) + ' := ' + f.assign + '   чтений: ' + f.read + (f.read === 0 ? '   <-- только пишется' : ''));

fs.mkdirSync(path.join(__dirname, '..', 'out'), { recursive: true });
const outFile = path.join(__dirname, '..', 'out', 'form-inventory.txt');
fs.writeFileSync(outFile, out.join('\r\n') + '\r\n', 'utf8');
console.log(out.join('\n'));
console.log('\n(сохранено: ' + outFile + ')');
