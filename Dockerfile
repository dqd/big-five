FROM python:3.12-bookworm

ENV WORKDIR=/code
WORKDIR $WORKDIR

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y sqlite3 gettext && \
    apt-get clean

COPY . $WORKDIR
RUN pip install -r requirements.txt

RUN useradd -d "$WORKDIR" -s /bin/bash bigfive
RUN mkdir -p "$WORKDIR/data" && chown -R bigfive:bigfive "$WORKDIR/data"

USER bigfive
CMD [ "gunicorn", "-b", "0:9200", "bigfive.wsgi" ]
