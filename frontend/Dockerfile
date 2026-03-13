FROM nginx:alpine3.23-slim
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/conf.d/shorty-nginx.conf /etc/nginx/conf.d/
COPY src/ /usr/share/nginx/html/
CMD ["nginx", "-g", "daemon off;"]