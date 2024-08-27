# syntax=docker/dockerfile:1.4.1
FROM node:18.20-bullseye as builder

ARG WORKDIR
WORKDIR ${WORKDIR}

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy source files
COPY . .

# Build the application
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# Production stage
FROM nginx:alpine as production

# セキュリティ警告に対応するパッケージをインストール
RUN apk update && \
  apk upgrade && \
  apk add --no-cache \
  --repository=https://dl-cdn.alpinelinux.org/alpine/edge/main \
  curl libcurl

WORKDIR /usr/share/nginx/html

# Copy built files from the build stage
ARG WORKDIR
COPY --from=builder ${WORKDIR}/dist .

# Copy custom Nginx configuration if needed
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

# Expose the port the app runs on
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
