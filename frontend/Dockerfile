FROM node:16-alpine

WORKDIR /app

COPY src/ .

RUN npm install
RUN npm run build

CMD ["npm", "start"]

