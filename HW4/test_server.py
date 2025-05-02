from server import application
from wsgiref.simple_server import make_server

with make_server("", 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
