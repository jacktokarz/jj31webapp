FROM node:24.0.2-alpine AS development-dependencies-env
COPY . /app
WORKDIR /app
RUN npm install
# RUN npm ci

FROM node:24.0.2-alpine AS production-dependencies-env
COPY ./package.json package-lock.json /app/
WORKDIR /app
RUN npm install
# RUN npm ci --omit=dev

FROM node:24.0.2-alpine AS build-env
COPY . /app/
COPY --from=development-dependencies-env /app/node_modules /app/node_modules
WORKDIR /app
RUN npm install
RUN npm run build

FROM node:24.0.2-alpine
COPY ./package.json package-lock.json /app/
COPY --from=production-dependencies-env /app/node_modules /app/node_modules
COPY --from=build-env /app/build /app/build
# RUN npm install
WORKDIR /app
EXPOSE 3000
EXPOSE 80
CMD ["npm", "run", "start"]