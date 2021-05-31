FROM node as build

ENV APP_HOME=/home/app
WORKDIR $APP_HOME

COPY ./mhq-front .
RUN npm install --legacy-peer-deps
RUN npm run build

FROM nginx:1.19.0

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

COPY --from=build /home/app/build /usr/share/nginx/html