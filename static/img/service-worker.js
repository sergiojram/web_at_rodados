const CACHE_NAME = 'rodados-at-v1';
const urlsToCache = [
  '/',
  '/static/css/styles.css',            // Si usás un CSS externo propio
  '/static/img/rodados.png',
  '/static/img/linde.png',
  '/static/img/still.png',
  '/static/icons/favicon-32x32.png',
  '/static/icons/favicon-16x16.png',
  '/static/icons/apple-touch-icon.png',
  '/static/manifest.json'
];

// Instalación del service worker y almacenamiento en caché
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('✅ Archivos cacheados correctamente');
        return cache.addAll(urlsToCache);
      })
  );
});

// Activación del service worker (limpieza de cachés antiguas si las hubiera)
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(name) {
          if (name !== CACHE_NAME) {
            console.log('🧹 Caché antigua eliminada:', name);
            return caches.delete(name);
          }
        })
      );
    })
  );
});

// Intercepción de peticiones
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Si está en caché, respondemos con eso
        if (response) {
          return response;
        }
        // Si no, hacemos la petición normal
        return fetch(event.request);
      })
  );
});
