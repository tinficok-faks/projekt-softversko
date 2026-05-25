FROM node:22-alpine

# Postavljanje radnog direktorija unutar kontejnera
WORKDIR /app

# Kopiranje package.json i package-lock.json
COPY package*.json ./

# Instalacija ovisnosti
RUN npm install

# Kopiranje ostatka frontend koda
COPY . .

# Konfiguriranje porta koji Vite koristi
EXPOSE 5173

# Pokretanje aplikacije i izlaganje hosta na lokalnu mrežu dockera
CMD ["npm", "run", "dev", "--", "--host"]
