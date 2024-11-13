self.addEventListener("install", (event) => {
    event.waitUntil(
      caches.open("static-cache").then((cache) => {
        return cache.addAll(["/", "/favicon192.png", "favicon256.png"]);
      })
    );
  });
  
  self.addEventListener("fetch", (event) => {
    event.respondWith(
      caches.match(event.request).then((response) => {
        return response || fetch(event.request);
      })
    );
  });
  