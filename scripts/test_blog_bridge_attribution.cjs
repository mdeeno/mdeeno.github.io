const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const vm = require('node:vm');
const html = execFileSync('python3', ['-c',
  'from build_blog_bridge import bridge_html; print(bridge_html("https://mdeeno.com/blog/posts/example"))'],
  {cwd: __dirname, encoding: 'utf8'});
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
function redirect(search, hash = '') {
  const calls = [];
  vm.runInNewContext(script, {URL, URLSearchParams,
    document: {querySelector: () => ({href: 'https://mdeeno.com/blog/posts/example'})},
    location: {search, hash, replace: (url) => calls.push(url)},
  });
  return calls;
}
assert.deepEqual(redirect(''), []);
assert.deepEqual(redirect('?utm_source=Blog&utm_medium=post_cta&utm_campaign=weekly_202609&utm_content=w37', '#핵심-답변'),
  ['https://mdeeno.com/blog/posts/example?utm_source=blog&utm_medium=post_cta&utm_campaign=weekly_202609&utm_content=w37#%ED%95%B5%EC%8B%AC-%EB%8B%B5%EB%B3%80']);
assert.deepEqual(redirect('?next=https://evil.example&url=//evil.example&email=person@example.invalid&token=secret&utm_source=blog&utm_term=private', '#section-2'),
  ['https://mdeeno.com/blog/posts/example?utm_source=blog#section-2']);
assert.deepEqual(redirect('?utm_source=01012345678&utm_medium=person%40example.invalid&utm_campaign=900101-1234567&utm_content=https://evil.example'),
  ['https://mdeeno.com/blog/posts/example']);
assert.deepEqual(redirect('', '#//evil.example'), ['https://mdeeno.com/blog/posts/example#//evil.example']);
assert.match(html, /<meta name="referrer" content="no-referrer">/);
assert.match(html, /http-equiv="refresh" content="0; url=https:\/\/mdeeno.com\/blog\/posts\/example"/);
console.log('bridge UTM4·앵커 보존, open redirect·PII 쿼리 차단, meta fallback PASS');
