// 공통 클릭 핸들러를 실행해 내부 위클리 이동과 제품 클릭의 중복을 검사한다.
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const {runInNewContext} = require('node:vm');
const {join} = require('node:path');
const footer = readFileSync(join(__dirname, '../layouts/partials/extend_footer.html'), 'utf8');
const script = [...footer.matchAll(/<script>([\s\S]*?)<\/script>/g)]
  .map(match => match[1]).find(text => text.includes('blog_to_mvp_click'));
let handler;
const events = [];
const window = {location: {pathname: '/calculators/calc_interest/', href: 'https://tech.mdeeno.com/calculators/calc_interest/', origin: 'https://tech.mdeeno.com'},
  gtag: (...args) => {if (args[0] === 'event') events.push(args);}};
runInNewContext(script, {window, URL, document: {title: '이자 계산기', addEventListener: (_, fn) => {handler = fn;}}});
function click(href, weekly = false, inline = '') {
  events.length = 0;
  const link = {href, closest: () => null, hasAttribute: name => weekly && name === 'data-weekly-link', getAttribute: () => inline};
  handler({target: {closest: () => link}});
}
click('https://tech.mdeeno.com/posts/market/weekly/', true);
assert.equal(events.length, 1);
assert.equal(events[0][1], 'blog_weekly_click');
assert.equal(events[0][2].destination, '/posts/market/weekly/');
click('https://mdeeno.com/member?utm_source=blog');
assert.equal(events.length, 1);
assert.equal(events[0][1], 'blog_to_mvp_click');
click('https://other.example/posts/weekly/', true);
assert.equal(events.length, 0);
click('https://mdeeno.com/member', false, "gtag('event', 'blog_to_mvp_click')");
assert.equal(events.length, 0);
console.log('blog funnel: internal weekly / product / external / duplicate checks passed');
