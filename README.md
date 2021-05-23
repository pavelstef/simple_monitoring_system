# SIMPLE MONITORING SYSTEM

A simple application designed to control the availability of network devices in your home / small office.
The application has a simple and convenient interface. A lot of windows and settings will not annoy you. :)

Default Admin user - admin/password123


# Installation manual

 
 
# Description 
 
Components:
+ The core web application - http://<your_server_ip>:80/
+ Flower (Celery monitoring system) - http://<your_server_ip>:5555/
+ REST API - http://<your_server_ip>:80/api/v1/sms/devices
+ REST API Token auth - http://<your_server_ip>:80/api/v1/auth-token/token/login/
+ REST API Documentation - http://<your_server_ip>:80/api/v1/sms/docs