# This is a comment 

FROM node:14
WORKDIR /app
ADD . .
USER root
RUN yarn install --production
CMD ["node", "src/index.js"]
EXPOSE 10