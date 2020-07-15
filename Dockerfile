FROM python:3.8-slim
ENV STORAGE_DIR /var/lib/databases

RUN apt-get update \
    && apt-get --no-install-recommends install dumb-init \
    && rm -rf /var/lib/apt/lists/*

ADD requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

RUN mkdir -p ${STORAGE_DIR}
VOLUME ${STORAGE_DIR}

ADD databases /srv

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD python /srv/entrypoint.py