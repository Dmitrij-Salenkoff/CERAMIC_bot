FROM python:3.10

COPY . ./Test_docker
WORKDIR ./Test_docker

ENV API_TOKEN = ""

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "telegram_bot.py" ] 
