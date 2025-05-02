Nathan Dinh  
CS-174 Section 02 – Server Web Programming  
Spring 2025  

HW4 – Server-Side JSON Processing with Apache and Python (mod_wsgi)

=============================================================

Hosted Application URL:
http://ec2-44-247-221-104.us-west-2.compute.amazonaws.com/

How to Use:
-----------
1. Open the hosted URL above in a browser.
2. Enter a JSON filename (example: truckinglist.json) in the text input.
3. Click "Submit Query".
4. A new popup window will display an HTML table of trucking company data.

Overview:
---------
This project enhances the trucking company table functionality by moving JSON file processing to the server side using Apache and Python.

JavaScript uses the Fetch API to send the JSON filename to the server (`/myapp`), where:
- Python reads and parses the specified JSON file.
- It returns the data as an HTML table.
- The frontend displays the table in a new browser popup.

Files Included:
---------------
- index.html – Frontend interface for file input
- script.js – JavaScript with fetch logic and popup handling
- server.py – Python backend to read the JSON and return HTML
- myapp.wsgi – WSGI script connecting Apache to `server.py`
- truckinglist.json – Sample JSON file with mock trucking company data
- README.txt – This file

Notes:
------
- The Python script is accessed via Apache using mod_wsgi.
- JSON files are read from `/var/www/html/` on the EC2 instance.
- Apache must be restarted after changes to `server.py` or `myapp.wsgi` using:
  `sudo systemctl restart httpd`
- JSON must be valid and follow the correct structure (a list of objects).

