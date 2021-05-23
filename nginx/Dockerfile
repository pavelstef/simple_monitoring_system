# Base on offical NGINX Alpine image
FROM nginx:alpine

RUN mkdir -p /opt/www/
WORKDIR /opt/www/
COPY .sms.conf /etc/nginx/conf.d/default.conf

# Expose the listening port
EXPOSE 80
EXPOSE 443

# Launch NGINX
CMD [ "nginx", "-g", "daemon off;" ]