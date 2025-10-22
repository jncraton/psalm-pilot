const CACHE_NAME = 'psalm-pilot-cache-v1'

self.addEventListener('install', e => {
  e.waitUntil(
    caches
      .open(CACHE_NAME)
      .then(cache => {
        const base = self.registration.scope
        return cache.addAll([
          new URL('index.html', base).toString(),
          new URL('style.css', base).toString(),
        ])
      })
      .then(() => self.skipWaiting()),
  )
})

self.addEventListener('activate', e => {
  e.waitUntil(
    caches
      .keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cache => {
            if (cache !== CACHE_NAME) {
              console.log('Deleting old cache:', cache)
              return caches.delete(cache)
            }
          }),
        )
      })
      .then(() => self.clients.claim()),
  )
})

self.addEventListener('fetch', e => {
  console.log(e.request.url)
  e.respondWith(
    caches.match(e.request).then(response => response || fetch(e.request)),
  )
})
