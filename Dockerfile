FROM python:3.10-slim 

WORKDIR /var/www/taxi-bot

RUN pip install --no-cache-dir pipenv

COPY ./config_data ./config_data
COPY ./db_logic ./db_logic
COPY ./filters ./filters
COPY ./FSM_data ./FSM_data
COPY ./geo_location ./geo_location
COPY ./handlers ./handlers
COPY ./keyboards ./keyboards
COPY ./lexicon ./lexicon
COPY ./requirements.txt ./requirements.txt
COPY ./.env ./.env
COPY ./main.py ./main.py

RUN cd /var/www/taxi-bot \
    # && pipenv requirements > /tmp/requirements.txt \
    && pip install --no-cache-dir -r requirements.txt 
    # && rm /tmp/requirements.txt 

CMD ["python", "/var/www/taxi-bot/main.py"]