### Build and install packages
FROM python:3.8 as build-python

RUN apt-get -y update \
    && apt-get install -y \
    gettext \
    # Cleanup apt cache
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements-dev.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

### Final image
FROM python:3.8-slim

RUN groupadd -r mipunto && useradd -r -g mipunto mipunto

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    gettext \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libmagic1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libssl1.1 \
    libxml2 \
    mime-support \
    shared-mime-info \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
COPY --from=build-python /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/
WORKDIR /app

RUN python3 manage.py collectstatic --no-input

RUN mkdir -p /app/media /app/static \
    && chown -R mipunto:mipunto /app/

EXPOSE 8000
EXPOSE 8888
ENV PORT 8000
ENV PYTHONUNBUFFERED 1
ENV PROCESSES 4

# Setup properly django container
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mipunto.wsgi"]
