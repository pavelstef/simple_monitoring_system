# Base on offical NGINX Alpine image
FROM nginx:latest

RUN mkdir -p /opt/www/
WORKDIR /opt/www/
RUN rm /etc/nginx/conf.d/default.conf
COPY default.conf /etc/nginx/conf.d
