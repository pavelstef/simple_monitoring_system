# SIMPLE MONITORING SYSTEM

A simple application designed to control the availability of network devices in your home / small office.
The application has a simple and convenient interface. A lot of windows and settings will not annoy you. :)

# Installation and run

1. Install the Docker
https://docs.docker.com/engine/install/
   
2. Create an environment file or export environment variables
```
SMS_DEBUG=<True/False>
SMS_SECRET_KEY=<key>
SMS_DATABASE_NAME=<name>
SMS_DATABASE_USER=<user>
SMS_DATABASE_PASSWORD=<password>
SMS_REDIS_DB_NUM=<num>
SMS_TZ=<timezone>
```

3. Build the docker images
```
docker-compose -f docker-compose.yml --env-file <an environment file> build
```

4. Run the app
```
docker-compose -f docker-compose.yml --env-file <an environment file> up -d
```
 
Now the app is running and you should have an access to it on http://<your_server_ip>:80/
The default admin user\password = admin\password123

# Stopping and remove

1. Stopping without removing a data
```
docker-compose -f docker-compose.yml --env-file <an environment file> down
```

2. Stopping with removing a data
```
docker-compose -f docker-compose.yml --env-file <an environment file> down --volumes
```
 
# Description 
 
Components:
+ The core web application - http://<your_server_ip>:80/
+ Flower (Celery monitoring system) - http://<your_server_ip>:5555/
+ REST API - http://<your_server_ip>:80/api/v1/sms/devices
+ REST API Token auth - http://<your_server_ip>:80/api/v1/auth-token/token/login/
+ REST API Documentation - http://<your_server_ip>:80/api/v1/sms/docs