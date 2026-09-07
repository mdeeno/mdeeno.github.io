// tech.mdeeno.com 이전 후 기존 블로그 Service Worker를 퇴역한다.
// v1(e6cebd08)·v2(6df6c16e)에서 실제 사용한 캐시 이름만 정리한다.
const LEGACY_CACHES = new Set([
  'mdeeno-v1-static', 'mdeeno-v1-pages',
  'mdeeno-v2-static', 'mdeeno-v2-pages'
]);

if (['https://tech.mdeeno.com', 'https://mdeeno.github.io'].includes(self.location.origin)) {
  self.addEventListener('install', (event) => {
    event.waitUntil(self.skipWaiting());
  });
  self.addEventListener('activate', (event) => {
    event.waitUntil(
      caches.keys()
        .then((keys) => Promise.all(keys.filter((key) => LEGACY_CACHES.has(key)).map((key) => caches.delete(key))))
        .then(() => self.registration.unregister())
    );
  });
}
