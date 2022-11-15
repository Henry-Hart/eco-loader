
// install event => kick any other service workers out
self.addEventListener('install', e => {
  self.skipWaiting();
});


// claim the current page for intercepting fetch requests
// perhaps not neccessary in this case though...
self.addEventListener('activate', e => {
    e.waitUntil(self.clients.claim());
});


// start intercepting fetch requests
self.addEventListener('fetch', (e) => {
  e.respondWith((async () => {

    // check if requested url is in cache
    const r = await caches.match(e.request);
    if (r) return r;

    // it isn't, so find the resource ourselves (with a custom header)
    const response = await fetch(e.request, {headers: {"From-ServiceWorker": "1"}});
    const cache = await caches.open("eco_webpage_cache");
    cache.put(e.request, response.clone());
    return response;
  })());
});