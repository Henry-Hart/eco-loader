
# libs => for servery stuff
import http.server
import socketserver

# port
PORT = 8000

# don't do anything fancy with these
REDIRECT_BLACKLIST = [
    "/sw.js", # service worker file
    "/swloader.html", # service worker loading page
    "/favicon.ico", # even though we don't have one
]

# check if the service worker loaded
# not very idiomatic I know...
def is_sw_able_to_load(self, split_path):
    
    # check the url
    if len(split_path) > 1:

        # if our webpage tells us it can't load the sw...
        if split_path[1].find("82946291_sw_cantload=1") != -1:

            # ... tell our parent function the same thing
            return False
    
    # check the referer url
    referer = self.headers.get("Referer")
    if isinstance(referer, str):
        ref_split = referer.split("?")
        if len(ref_split) > 1:
            
            # if we CAN find this, then the sw DIDN'T LOAD
            # and thus return False
            return ref_split[1].find("82946291_sw_cantload=1") == -1
    
    # didn't find anything, so we assume everything's ok
    return True

# config
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    # we only handle GET
    def do_GET(self):

        print(self.headers.get("From-ServiceWorker"))
        # if we're not using a service worker...
        if self.headers.get("From-ServiceWorker") != "1":

            split_path = self.path.split("?")

            # get the a.b/c part of a.b/c?d=e
            # ... and check it's not in the blacklist
            print(split_path[0])
            if split_path[0] not in REDIRECT_BLACKLIST:
                
                # check we can actually load the service worker
                if is_sw_able_to_load(self, split_path):
                    self.send_response(302)
                    self.send_header('Location', "/swloader.html?to="+self.path)
                    self.end_headers()
                
        print(self.path)
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


# handler
Handler = MyHttpRequestHandler
 
# start the server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Http Server Serving at port", PORT)
    httpd.serve_forever()