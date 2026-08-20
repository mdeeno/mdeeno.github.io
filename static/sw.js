// M-DEENO Blog Service Worker
// Network-first for HTML/CSS/JS, Cache-first for versioned media assets

const CACHE_VERSION = 'mdeeno-v2';
const STATIC_CACHE = CACHE_VERSION + '-static';
const PAGES_CACHE = CACHE_VERSION + '-pages';

// Pre-cache on install
const PRECACHE_URLS = [
  '/',
  '/offline.html',
  '/css/custom.css',
  '/manifest.json'
];

// Install: pre-cache essential resources
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

// Activate: clean up old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys
          .filter((key) => key !== STATIC_CACHE && key !== PAGES_CACHE)
          .map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch strategy
self.addEventListener('fetch', (event) => {
  const { request } = event;

  // Skip non-GET requests
  if (request.method !== 'GET') return;

  // Skip external requests (analytics, CDN fonts loaded separately)
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  // HTML pages: Network-first (fresh content), fallback to cache, then offline page
  if (request.headers.get('Accept')?.includes('text/html')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const clone = response.clone();
          caches.open(PAGES_CACHE).then((cache) => cache.put(request, clone));
          return response;
        })
        .catch(() => {
          return caches.match(request)
            .then((cached) => cached || caches.match('/offline.html'));
        })
    );
    return;
  }

  // CSS/JS는 네트워크 우선으로 갱신해 설치형 PWA에 UI 수정이 오래 남지 않게 한다.
  if (request.destination === 'style' || request.destination === 'script') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (!response || response.status !== 200) return response;
          const clone = response.clone();
          caches.open(STATIC_CACHE).then((cache) => cache.put(request, clone));
          return response;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

  // 이미지·기타 정적 자산: Cache-first, fallback to network
  event.respondWith(
    caches.match(request)
      .then((cached) => {
        if (cached) return cached;
        return fetch(request).then((response) => {
          // Only cache successful responses
          if (!response || response.status !== 200) return response;

          // Don't cache chart images (too many, too large)
          if (url.pathname.startsWith('/images/chart-')) return response;

          const clone = response.clone();
          caches.open(STATIC_CACHE).then((cache) => cache.put(request, clone));
          return response;
        });
      })
  );
});
