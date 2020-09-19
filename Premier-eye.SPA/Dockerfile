### STAGE 1: Build ###
FROM node:14 as build
WORKDIR /usr/src/app
COPY package.json .
RUN yarn install

ARG configuration=dev

COPY . .
RUN yarn build:${configuration}


### STAGE 2: Production Environment ###
FROM nginx:alpine
ENV configuration=Development
#!/bin/sh

COPY nginx.conf /etc/nginx/nginx.conf

## Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

COPY --from=build /usr/src/app/dist /usr/share/nginx/html
RUN cd /usr/share/nginx/html && ls
EXPOSE 5000

ENTRYPOINT ["nginx", "-g", "daemon off;"]
