FROM node:20-alpine AS build

WORKDIR /app/web

COPY ./src /app/web/src/
COPY index.html package*.json tsconfig.json postcss.config.js tailwind.config.js vite.config.ts /app/web/

RUN npm cache clean --force
RUN npm install
RUN npm run build

FROM nginx:alpine

COPY --from=build /app/web/dist /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
