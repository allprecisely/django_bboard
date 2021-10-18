FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN python3 -m pip install -r requirements.txt

COPY utils/entrypoint.sh /usr/src/bin/entrypoint.sh

RUN chmod +x /usr/src/bin/entrypoint.sh
