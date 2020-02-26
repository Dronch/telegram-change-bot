FROM python:3.7-slim-buster

WORKDIR /app
RUN pip install pipenv

RUN useradd -m bot
RUN chown -R bot:bot /app
USER bot
ENV PATH="/home/bot/.local/bin:${PATH}"


COPY Pipfile ./
RUN pipenv install
COPY ./telegram_change_bot ./telegram_change_bot
COPY ./app.py ./app.py

ENTRYPOINT [ "pipenv", "run", "python", "app.py" ]
