FROM python:3.14-slim-trixie

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    WORKDIR=/code

WORKDIR $WORKDIR

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y gettext sqlite3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies first so that this layer is cached between code changes.
COPY requirements.txt $WORKDIR/
RUN pip install --no-cache-dir -r requirements.txt

COPY . $WORKDIR

RUN useradd -d "$WORKDIR" -s /bin/bash bigfive && \
    mkdir -p "$WORKDIR/data" && \
    chown -R bigfive:bigfive "$WORKDIR/data"

USER bigfive
EXPOSE 9200
CMD ["gunicorn", "--bind", "0:9200", "bigfive.wsgi"]
