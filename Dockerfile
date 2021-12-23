###########################################################################
# Build dev base image
###########################################################################
FROM tiangolo/uvicorn-gunicorn:python3.8-slim AS dev-base

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y \
  curl \
  gcc \
  netcat \
  && apt-get clean \
  && pip install --upgrade pip

# Install Poetry (append poetry bin path)
ENV PATH="/root/.local/bin:$PATH"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python - && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry install --no-root

COPY ./ActionTemplate-Python3/ /opt/action_template/
RUN pip install /opt/action_template/

# use default /gunicorn_conf.py
ENV PORT 8080
# use default /start.sh
# exec gunicorn -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE"
COPY ./src /app

###########################################################################
# Build lint image
###########################################################################
# FROM dev-base AS dev-linter

# RUN pycodestyle --max-line-length 140 --statistics .
###########################################################################
# Build utest coverage image
###########################################################################
FROM dev-base AS dev-coverage

RUN coverage run -m pytest -p no:warnings --cov=. --cov-report html --cov-report xml
###########################################################################
# Build security check image
###########################################################################
FROM dev-base AS dev-security

COPY bandit.yml /app
RUN python -m bandit -r /app -c bandit.yml
RUN python -m safety check
###########################################################################
# Build production image - api
###########################################################################
# FROM dev-base

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
