const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../static/sw.js'), 'utf8');

(async () => {
  for (const origin of ['https://tech.mdeeno.com', 'https://mdeeno.github.io', 'https://mdeeno.com']) {
    const events = new Map(); const removed = []; let unregistered = 0;
    const legacy = ['mdeeno-v1-static', 'mdeeno-v1-pages', 'mdeeno-v2-static', 'mdeeno-v2-pages'];
    vm.runInNewContext(source, {
      self: { location: {origin}, skipWaiting: async () => {},
        addEventListener: (name, handler) => events.set(name, handler),
        registration: { unregister: async () => { unregistered++; } } },
      caches: { keys: async () => [...legacy, 'mdeeno-v2-private', 'other-app-cache'],
        delete: async (key) => { removed.push(key); } },
    });
    let finished;
    events.get('activate')?.({waitUntil: (promise) => { finished = promise; }});
    await finished;
    assert.equal(events.has('fetch'), false);
    assert.deepEqual(removed, origin === 'https://mdeeno.com' ? [] : legacy);
    assert.equal(unregistered, origin === 'https://mdeeno.com' ? 0 : 1);
  }
  console.log('블로그 SW 퇴역: 기존 4개 캐시만 삭제, 다른 캐시·메인 도메인 보존 PASS');
})().catch((error) => { console.error(error); process.exitCode = 1; });
