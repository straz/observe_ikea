# build with
# docker build -t zigchart .

# run with
# docker run -it -p 3000:3000 zigchart


FROM node:22.9
EXPOSE 3000

WORKDIR /app

COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm install
COPY . .


CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
