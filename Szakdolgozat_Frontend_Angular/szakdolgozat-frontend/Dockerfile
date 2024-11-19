FROM node:18 as build

WORKDIR /app

COPY package*.json ./

RUN npm install -g @angular/cli
RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist/szakdolgozat-frontend/browser /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf
