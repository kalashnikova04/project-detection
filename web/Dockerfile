FROM python:3

ENV PYTHONUNBUFFERED 1
ENV APP_HOME /lp_detection

RUN mkdir -p $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media

RUN addgroup --system lp_detection && adduser --system --group lp_detection

COPY /lp_detection $APP_HOME
WORKDIR $APP_HOME

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ADD docker-entrypoint.sh $APP_HOME/docker-entrypoint.sh
RUN chmod +x $APP_HOME/docker-entrypoint.sh

RUN chown -R lp_detection:lp_detection $APP_HOME

USER lp_detection

ENTRYPOINT ["/lp_detection/docker-entrypoint.sh"]