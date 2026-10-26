const CACHE='the-cut-v4-20261026';
const FILES=['./','./index.html','./styles.css','./app.js','./data.js','./metadata.js','./manifest.webmanifest','./assets/icon.svg'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))));self.clients.claim()});
self.addEventListener('fetch',e=>{if(e.request.method!=='GET'||new URL(e.request.url).origin!==self.location.origin)return;e.respondWith(caches.match(e.request).then(c=>c||fetch(e.request).then(r=>{if(r.ok){let clone=r.clone();caches.open(CACHE).then(cache=>cache.put(e.request,clone))}return r})))})
