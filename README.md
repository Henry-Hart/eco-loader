# eco-loader
 A simple (and buggy) implementation of a server that automatically caches webpages on the client.
## Why?
- Reloading webpages (taking into account 304s and automatic caching) uses data
- Sending data across a network uses large amounts of energy, which produces carbon
- Caching webpages means that no extra data is sent across a network on reload => saving energy
## How it works
- When a page/asset is loaded, `server.py` checks if the request is comming from a service worker or a human
- If a human loaded the page, `server.py` redirects to `swloader.html` which loads the service worker `sw.js`
- `sw.js` intercepts fetch requests, deciding whether to pull them from a cache or to replay them with custom headers
- If `server.py` notices these custom headers, it knows `sw.js` sent them and sends the original page/asset
## More info
- If `swloader.js` detects that the service worker can't run, it redirects to the originally requested page with a custom query parameter that bypasses `server.py` redirects.
- This originally contained a game as another example, but it sometimes didn't fully work/load properly. However, **this server can do much more than just load `index.html`**, so I recommend you experiment.
- `sw.js` does not automatically check for updated pages in its cache. However, this could easily be done by sending the hashes of pages/assets to the server for comparison. It would still save (lots of) energy.
- If you wanted, you could make the server *only load `.html` files*, which would make this much more reliable for loading online games efficiently. There wouldn't be much extra data sent here either, as the assets would still be cached (but the service worker would **only start when the user loaded an `.html` file**, but that's extremely likely to be the first thing they do anyway).
## Running
- Use python3 and a browser