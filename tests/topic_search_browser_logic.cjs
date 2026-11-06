/* Exercise production event handlers and filtering with a minimal DOM contract. */
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const handlers = {};
function element(name, props = {}) { return {hidden: false, value: '', addEventListener(event, fn) { handlers[name + ':' + event] = fn; }, ...props}; }
const query = element('query', {focus() {}});
const language = element('language', {options: [{value:''},{value:'nb'},{value:'en'}]});
const form = element('form');
const result = element('result');
const empty = element('empty');
const entries = [element('a', {dataset:{search:'Måltid — Brødtekst med økotun og skolemat',languages:'nb en'}}),element('b',{dataset:{search:'Mortgage payments and interest rates',languages:'en'}})];
const jump = element('jump');
const section = element('section', {id:'stories',querySelectorAll(){return entries;}});
const ids = {'map-query':query,'map-language':language,'map-results':result,'map-empty':empty};
let address = 'https://experimentalnewsroom.org/sitemap.html?q=okotuN&lang=nb';
const context = {document:{documentElement:{lang:'nb'},getElementById(id){return ids[id];},querySelector(s){return s === '.map-search' ? form : jump;},querySelectorAll(s){return s === '.map-section' ? [section] : entries;}},window:{location:{href:address,search:'?q=okotuN&lang=nb'},history:{replaceState(_,__,url){address=String(url);}}},URL,URLSearchParams,setTimeout(fn){fn();return 1;},clearTimeout(){}};
vm.runInNewContext(fs.readFileSync('public/reader-navigation.js','utf8'),context);
assert.equal(query.value,'okotuN'); assert.equal(entries[0].hidden,false);assert.equal(entries[1].hidden,true);
query.value='MÅLTID skolemat';handlers['query:input']();assert.equal(entries[0].hidden,false);
query.value='missing';handlers['query:input']();assert.equal(empty.hidden,false);assert.equal(section.hidden,true);
let prevented=false;handlers['form:reset']({preventDefault(){prevented=true;}});assert.ok(prevented);assert.equal(query.value,'');assert.equal(language.value,'');assert.equal(empty.hidden,true);assert.ok(entries.every(e=>!e.hidden));assert.equal(new URL(address).search,'');
language.value='en';query.value='mortgage';handlers['form:submit']({preventDefault(){}});assert.equal(entries[1].hidden,false);assert.equal(entries[0].hidden,true);assert.equal(new URL(address).searchParams.get('lang'),'en');
console.log('Topic search browser logic: PASS (URL state, accent/AND matching, language, empty/reset).');
