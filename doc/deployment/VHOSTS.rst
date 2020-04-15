Apache + mod-wsgi configuration
===============================

An example Apache2 vhost configuration follows::

    WSGIDaemonProcess objecttypes-<target> threads=5 maximum-requests=1000 user=<user> group=staff
    WSGIRestrictStdout Off

    <VirtualHost *:80>
        ServerName my.domain.name

        ErrorLog "/srv/sites/objecttypes/log/apache2/error.log"
        CustomLog "/srv/sites/objecttypes/log/apache2/access.log" common

        WSGIProcessGroup objecttypes-<target>

        Alias /media "/srv/sites/objecttypes/media/"
        Alias /static "/srv/sites/objecttypes/static/"

        WSGIScriptAlias / "/srv/sites/objecttypes/src/objecttypes/wsgi/wsgi_<target>.py"
    </VirtualHost>


Nginx + uwsgi + supervisor configuration
========================================

Supervisor/uwsgi:
-----------------

.. code::

    [program:uwsgi-objecttypes-<target>]
    user = <user>
    command = /srv/sites/objecttypes/env/bin/uwsgi --socket 127.0.0.1:8001 --wsgi-file /srv/sites/objecttypes/src/objecttypes/wsgi/wsgi_<target>.py
    home = /srv/sites/objecttypes/env
    master = true
    processes = 8
    harakiri = 600
    autostart = true
    autorestart = true
    stderr_logfile = /srv/sites/objecttypes/log/uwsgi_err.log
    stdout_logfile = /srv/sites/objecttypes/log/uwsgi_out.log
    stopsignal = QUIT

Nginx
-----

.. code::

    upstream django_objecttypes_<target> {
      ip_hash;
      server 127.0.0.1:8001;
    }

    server {
      listen :80;
      server_name  my.domain.name;

      access_log /srv/sites/objecttypes/log/nginx-access.log;
      error_log /srv/sites/objecttypes/log/nginx-error.log;

      location /500.html {
        root /srv/sites/objecttypes/src/objecttypes/templates/;
      }
      error_page 500 502 503 504 /500.html;

      location /static/ {
        alias /srv/sites/objecttypes/static/;
        expires 30d;
      }

      location /media/ {
        alias /srv/sites/objecttypes/media/;
        expires 30d;
      }

      location / {
        uwsgi_pass django_objecttypes_<target>;
      }
    }
