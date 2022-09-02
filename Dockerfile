# syntax = edrevo/dockerfile-plus
###########################################################################
# Build uut operation proxy base image (temp solution for ssh)
###########################################################################
INCLUDE+ ./ActionTemplate-Python3/UUTOperationProxy/DockerfileAction

###########################################################################
# Build dev base image
###########################################################################
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim AS dev-base

# set working directory
WORKDIR /app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MAX_WORKERS=1
ENV LOG_LEVEL=debug
ENV PORT 8080
EXPOSE 8080

# install system dependencies
RUN apt-get update \
  && apt-get -y install --no-install-recommends \
  curl \
  colorized-logs \
  daemontools \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --upgrade pip

# Install Poetry (append poetry bin path)
ENV PATH="/root/.local/bin:$PATH"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python - && \
  poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/
COPY ./ActionTemplate-Python3/ /app/ActionTemplate-Python3
# Install python dependencies include ActionTemplate-Python3
RUN poetry install --no-root --no-dev

###########################################################################
# Build dev env image
###########################################################################
FROM dev-base AS dev-env
RUN poetry install --no-root
COPY ./src /app

###########################################################################
# Build lint image
###########################################################################
FROM dev-env AS dev-linter
RUN pylama -o setup.cfg app

###########################################################################
# Build utest coverage image
###########################################################################
FROM dev-env AS dev-coverage
RUN coverage run -m pytest -p no:warnings --junitxml=junit.xml --cov=app --cov-report html --cov-report xml

###########################################################################
# Build security check image
###########################################################################
FROM dev-env AS dev-security
RUN python -m bandit -r /app/app
RUN python -m safety check

###########################################################################
# Build production image - api
###########################################################################
FROM dev-base AS prd
VOLUME [ "/data" ]
COPY ./src /app

# setup uut operation proxy binary
COPY --from=uut-operation-proxy-base /UUTOperationProxy/dist/uut-operation-proxy-linux /opt/uut-operation-proxy-linux

# zip all sub folder in static folder
RUN python3 /app/static/make_archive.py

# use Gunicorn running Uvicorn workers in the container
# CMD /start.sh

# running Uvicorn with auto reload in the container
CMD /start-reload.sh
