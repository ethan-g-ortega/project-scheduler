# ./frontend/Dockerfile
FROM node:20-alpine
WORKDIR /usr/src/app

# Install dependencies
COPY package*.json ./
RUN rm -rf node_modules package-lock.json && npm install

# Copy source code
COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]