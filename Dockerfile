FROM python:3.9.6-alpine3.14
WORKDIR /app
COPY * .
VOLUME /home/docker/proxy
ENV BUFFER_SIZE = 8192
ENV CONNECTIONS = 200
ENV SERVER_WAIT = 30
ENV TIMEOUT_MAX = 30
ENV BLACK_LIST_PATH = /home/docker/proxy/blacklist
ENV STATISTIC_PATH = /home/docker/proxy/statistic
ENV STATISTIC_WAIT = 180
ENV SERVER_PORT = 9090
CMD ["python","./proxy_core.py"]