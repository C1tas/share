# requirements

- pyenv
- supervisor
- gunicorn
- gem
- openresty

# pyenv

normal install

# supervisor

in arch supervisor

create a file 

`/etc/supervisor.d/django.ini`

```
[program:django]
command = /srv/http/lu4yu3/gunicorn_start
user = http
stdout_logfile = /srv/http/lu4yu3/logs/gunicorn_supervisor.log
redirect_stderr = true
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8
environment=PATH="/srv/http/.gem/ruby/2.4.0/bin:$PATH"
environment=GEM_PATH="/srv/http/.gem/ruby/2.4.0/"
```

# gunicorn

`create a file gunicorn_start`

```
#!/bin/bash

NAME="django-blog"                                  # Name of the application
DJANGODIR=/srv/http/lu4yu3/hackinmisc             # Django project directory
SOCKFILE=/srv/http/lu4yu3/run/gunicorn.sock  # we will communicte using this unix socket
USER=http                                     # the user to run as
GROUP=http                                    # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=hackinmisc.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=hackinmisc.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /srv/http/.pyenv/versions/3.6.1/envs/lu4yu3/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export PATH=/srv/http/.gem/ruby/2.4.0/bin:$PATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /srv/http/.pyenv/versions/3.6.1/envs/lu4yu3/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
```

# gem

in current user like `http` for me
```
gem install sass
```

# openresty

this is a extension versions fork nginx

`/usr/local/openresty/nginx/conf/servers-avaliable/c1tas.com`

```
upstream django_blog {
  # fail_timeout=0 means we always retry an upstream even if it failed
  # to return a good HTTP response (in case the Unicorn master nukes a
  # single worker for timing out).

  server unix:/srv/http/lu4yu3/run/gunicorn.sock fail_timeout=0;
}
server {
	listen 80;
    #listen [::]:80;
  	server_name c1tas.com;
	#root /usr/share/nginx/html;
	#return 301 https://$host$request_uri;

    client_max_body_size 4G;

    access_log /srv/http/lu4yu3/logs/nginx-access.log;
    error_log /srv/http/lu4yu3/logs/nginx-error.log;
    # path for static files
    root /srv/http/lu4yu3/hackinmisc;
    location /static/ {
        alias   /srv/http/lu4yu3/hackinmisc/static/;
    }

    location / {
      # checks for static file, if not found proxy to app
      try_files $uri @proxy_to_app;
    }

    location @proxy_to_app {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      # enable this if and only if you use HTTPS
      # proxy_set_header X-Forwarded-Proto https;
      proxy_set_header Host $http_host;
      # we don't want nginx trying to do something clever with
      # redirects, we set the Host: header above already.
      proxy_redirect off;
      proxy_pass http://django_blog;
    }

    error_page 500 502 503 504 /500.html;
    location = /500.html {
      root /path/to/app/current/public;
    }
}

server {
	listen 443;
	server_name c1tas.com;

	ssl on;
	ssl_certificate /etc/letsencrypt/live/c1tas.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/c1tas.com/privkey.pem;

	ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
	ssl_prefer_server_ciphers on;
	ssl_dhparam /etc/ssl/certs/dhparam.pem;
	ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
	ssl_session_timeout 1d;
	ssl_session_cache shared:SSL:50m;
	ssl_stapling on;
	ssl_stapling_verify on;
	add_header Strict-Transport-Security max-age=15768000;

    client_max_body_size 4G;

    access_log /srv/http/lu4yu3/logs/nginx-access.log;
    error_log /srv/http/lu4yu3/logs/nginx-error.log;

    location /static/ {
        alias   /srv/http/lu4yu3/hackinmisc/static/;
    }

    location / {
      # checks for static file, if not found proxy to app
      try_files $uri @proxy_to_app;
    }

    location @proxy_to_app {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      # enable this if and only if you use HTTPS
      # proxy_set_header X-Forwarded-Proto https;
      proxy_set_header Host $http_host;
      # we don't want nginx trying to do something clever with
      # redirects, we set the Host: header above already.
      proxy_redirect off;
      proxy_pass http://django_blog;
    }

    error_page 500 502 503 504 /500.html;
    location = /500.html {
      root /path/to/app/current/public;
    }


}
```
