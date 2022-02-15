FROM python:3.10-alpine

LABEL maintainer="Vladislav Kislitsyn"

RUN pip install --upgrade pip
ARG username=bot_user_app
RUN adduser -D $username
USER $username
WORKDIR /home/$username

ADD --chown=$username:$username requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

ENV PATH="/home/${username}/.local/bin:${PATH}"
ENV BOT_SLACK_TOKEN=
ENV APP_SLACK_TOKEN=
ENV SIGNING_SLACK_SECRET=

ENV PYTHONUNBUFFERED=1

EXPOSE 8080

ADD --chown=$username:$username . .

CMD ["gunicorn", "-c", "configs/gunicorn.conf", "app.main:get_web_app"]