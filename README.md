# flask-gunicorn-nginx-wsgi


This is a deployment scenario where **Flask**, **Gunicorn**, **Nginx**, **WSGI**, and **Certbot** are used together to serve [this manually-administrated website](https://app.ericrxu.com) on HTTPS.


### Part definitions
- **Flask:** Flask is a Python web application framework. You write your web application with Flask, and it will handle the routing, request handling, and response generation for your application.

- **Gunicorn:** Gunicorn is a WSGI HTTP server for Python web applications. It serves as the interface between your Flask application and an actual web server (in this case, Nginx). It takes care of managing worker processes to handle incoming requests and then forwards those requests to your Flask application.

- **Nginx:** Nginx is a powerful, efficient, and robust web server, often used as a reverse proxy and load balancer. It can handle and distribute incoming requests to one or more Gunicorn instances, serve static files, handle SSL/TLS encryption, and manage other high-level HTTP features.

- **WSGI (Web Server Gateway Interface):** This is the specification that Flask applications adhere to. It allows applications to communicate with web servers, forwarding HTTP requests from the server to the application and responses from the application back to the server.

- **Certbot:**  free, open source software tool for automatically using Let’s Encrypt certificates on manually-administrated websites to enable HTTPS.


### how these parts work together:


- **A client makes a request:** A client (like a web browser) sends an HTTP request. This request is received by Nginx because it's the exposed server listening for HTTP(S) requests.

- **Request routing by Nginx:** Nginx checks the incoming request. If the request is for a static file (like a CSS, JS, or image file), Nginx will handle this itself: it finds the file and sends it back in the HTTP response. If the request is not for a static file (i.e., it requires running some Python code), Nginx forwards the request to Gunicorn. This is the reverse proxy functionality of Nginx in action.

- **HTTP to HTTPS redirection**: Nginx is configured to redirect HTTP requests to HTTPS. So, if a client makes an HTTP request, Nginx automatically redirects it to an HTTPS request.

- **Request handling by Gunicorn:** Gunicorn, running your Flask application, receives the request from Nginx. Gunicorn is a WSGI server, and its job is to translate the HTTP request into a format the Flask application can understand (per the WSGI spec), call the appropriate code in the Flask application, and then take the application's response and translate it back into an HTTP response.

- **Flask generates a response:** The Flask application receives the request data from Gunicorn, processes it as required (running your route functions, calling into databases, and so on), and then generates an HTTP response.

- **Response routing:** The HTTP response from Flask goes back to Gunicorn, which sends it back to Nginx.

- **Nginx responds to the client:** Finally, Nginx receives the HTTP response from Gunicorn and sends it back to the client (the web browser).  With the addition of HTTP to HTTPS redirection in the Nginx configuration via Certbot, any HTTP requests will be automatically redirected to the corresponding HTTPS requests to ensure secure communication between the client and the server.
