FROM node:18-alpine
WORKDIR /src
COPY . /src/
USER daemon
RUN npm install 
CMD ["node", "./index.js"]
