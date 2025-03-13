FROM node:22-alpine
EXPOSE 5173:5173
WORKDIR /app
COPY ./package.json .
RUN npm install
# Библиотека для работы с http запросами
RUN npm install axios
COPY . .
CMD ["npm", "run", "dev"]