FROM node as build

ENV HOME=/home/app
ENV APP_HOME=/home/app/front
WORKDIR $APP_HOME

COPY ./mhq-front/package.json .
RUN npm install --legacy-peer-deps
COPY ./mhq-front .

RUN npm run build

FROM nginx:1.19.0

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

COPY --from=build /home/app/front/build /usr/share/nginx/html