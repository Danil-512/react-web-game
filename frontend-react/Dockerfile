FROM node:22-alpine
EXPOSE 5173:5173
WORKDIR /app
COPY ./package.json .
RUN npm install
RUN npm init vite@latest my-react-app -- --template react
# Библиотека для работы с http запросами
RUN npm install axios
RUN npm install react-router-dom
COPY . .
CMD ["npm", "run", "dev"]