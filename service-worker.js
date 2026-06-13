// service-worker.js – basic offline support
const CACHE_NAME = 'ai-it-interview-v1';
const FILES_TO_CACHE = [
  '/',
  '/index.html',
  '/style.css',
  '/app.js',
  '/manifest.json'
];

self.addEventListener('install', evt => {
  evt.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(FILES_TO_CACHE)));
});

self.addEventListener('fetch', evt => {
  evt.respondWith(caches.match(evt.request).then(response => response || fetch(evt.request)));
});
