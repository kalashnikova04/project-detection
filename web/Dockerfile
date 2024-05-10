FROM python:3

COPY /lp_detection /lp_detection
WORKDIR /lp_detection

EXPOSE 8098

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ADD docker-entrypoint.sh /lp_detection/docker-entrypoint.sh
RUN chmod +x /lp_detection/docker-entrypoint.sh

ENTRYPOINT ["/lp_detection/docker-entrypoint.sh"]