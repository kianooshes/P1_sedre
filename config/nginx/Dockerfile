FROM nginx:latest
LABEL MAINTAINER="Kianoosh eskandari nezhad"

COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
