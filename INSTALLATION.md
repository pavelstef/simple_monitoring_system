# Installation.

The application was developed and tested on computers Linux Mint 19.3 (python 3.6.9) and Ubuntu 19.10 (python 3.7.5).

+ Installation of packages.
```
        sudo apt update
        sudo apt install -y python3-pip python3-venv redis-server nginx supervisor postgresql postgresql-contrib
```

+ App.

Pull the project from the github and prepare a virtual environment.
```
        cd home
        git pull project
        cd project_folder
        python3 -m venv venv
        . ./env/bin/activate
        pip install -U pip
        pip install -r requirement.txt
```

Make sure that you set parameters such as SECRET_KEY and DB_PASSWORD in the environment variables,
or edit the file **project_folder/sms/.env**

Use https://djecrety.ir/ to generate your own SECRET_KEY

Edit the scripts in the folder **<project_folder>/sms/bin/** according to your settings

Edit the gunicorn configuration file - **<project_folder>/sms/gunicorn_config.py**

+ PostgreSQL.

Make sure that PostgreSQL is running:
```
        pavel@gb-ubuntu-01:~$ sudo systemctl status postgresql
        ● postgresql.service - PostgreSQL RDBMS
            Loaded: loaded (/lib/systemd/system/postgresql.service; enabled; vendor preset: enabled)
            Active: active ...
```

Create database and user for django application:
```
        sudo -i -u postgres
        psql
        CREATE DATABASE sms;
        CREATE USER sms_user WITH PASSWORD <put_your_password_here>;
        ALTER ROLE sms_user SET client_encoding TO 'utf8';
        ALTER ROLE sms_user SET default_transaction_isolation TO 'read committed';
        ALTER ROLE sms_user SET timezone TO 'UTC+3';
        GRANT ALL PRIVILEGES ON DATABASE sms TO sms_user;
```

If you are going to run test cases, you need to grant privileges to the django user to access the test database:
```
        GRANT ALL PRIVILEGES ON DATABASE test_sms TO sms_user;
```


Initialize the database from the django shell and create your first admin user.

How to use django shell:
```
        cd project_folder/sms/
         . venv/bin/activate
        python manage.py makemigrations
        python manage.py migrate
        python manage.py createsuperuser
        <username>
        <password>
        <password>
```

+ Redis.

Edit **/etc/redis/redis.conf**
```
        bind 0.0.0.0
        protected-mode yes
        port 6379
        timeout 0
```

Make sure that Redis is running:
```
        pavel@gb-ubuntu-01:~$ sudo systemctl status redis
        ● redis-server.service - Advanced key-value store
           Loaded: loaded (/lib/systemd/system/redis-server.service; enabled; vendor preset: enabled)
           Active: active (running) since Sun 2020-04-12 18:23:03 MSK; 3s ago
```

+ Nginx.

Edit **/etc/nginx/sites-enabled/default**
```
        server {
                listen 80 default_server;
                listen [::]:80 default_server;

                server_name _;

                location /static/ {
                        alias /home/<project_folder>/sms/static/;
                }

                location / {
                        proxy_pass http://127.0.0.1:8001;
                        proxy_set_header X-Forwarded-Host $server_name;
                        proxy_set_header X-Real-IP $remote_addr;
                        add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
                        add_header Access-Control-Allow-Origin *;
                }
        }
```

Make sure that Nginx is running:
```
        pavel@gb-ubuntu-01:~$ sudo systemctl status nginx
        ● nginx.service - A high performance web server and a reverse proxy server
          Loaded: loaded (/lib/systemd/system/nginx.service; disabled; vendor preset: enabled)
          Active: active (running) since Wed 2020-04-15 19:25:53 MSK; 5min ago
```
+ Supervisor.

Edit the files in the "conf.d" folder according to your settings and copy these files to **/etc/supervisor/conf.d/**
```
        sudo supervisorctl reread
        sudo supervisorctl update
        sudo supervisorctl start all
```

Make sure that Supervisor is running:
```
        pavel@gb-ubuntu-01:~$ sudo systemctl status supervisor
        ● supervisor.service - Supervisor process control system for UNIX
          Loaded: loaded (/lib/systemd/system/supervisor.service; enabled; vendor preset: enabled)
          Active: active (running) since Wed 2020-04-15 19:55:03 MSK; 1min 20s ago
```

# It should works!
You should have an access to:
+ The core web application - http://<your_server_ip>:80/
+ Flower (Celery monitoring system) - http://<your_server_ip>:5555/
+ REST API - http://<your_server_ip>:80/api/v1/sms/devices
+ REST API Token auth - http://<your_server_ip>:80/api/v1/auth-token/token/login/
+ REST API Documentation - http://<your_server_ip>:80/api/v1/sms/docs

