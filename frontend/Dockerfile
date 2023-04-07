FROM node:lts-alpine as build-stage
ARG environment
# ENV ENVIRONMENT=${environment:?error}
WORKDIR /app
COPY package.json ./
# RUN npm install
COPY package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build-${environment}

FROM nginx:1.25 as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf