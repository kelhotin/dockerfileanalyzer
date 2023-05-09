# syntax=docker/dockerfile:1
   
# FROM node:14
FROM mySuspiciousBaseImage
WORKDIR /app
ADD . .
RUN yarn install --production
CMD ["node", "src/index.js"]
EXPOSE 10