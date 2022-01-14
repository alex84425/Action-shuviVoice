###########################################################################
# Build dev base image
###########################################################################
FROM tiangolo/uvicorn-gunicorn:python3.8-slim AS dev-base

# set working directory
WORKDIR /app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8080
EXPOSE 8080


# install system dependencies
RUN apt-get update \
  && apt-get -y install --no-install-recommends \
  netcat \
  gcc \
  zip \
  curl \
  procps \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --upgrade pip


# Install Poetry (append poetry bin path)
ENV PATH="/root/.local/bin:$PATH"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python - && \
  poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry install --no-root --no-dev

# Install submodule
COPY ./ActionTemplate-Python3/ /opt/action_template/
RUN pip install -e /opt/action_template/

COPY ./src /app

###########################################################################
# Build dev env image
###########################################################################
FROM dev-base AS dev-env
RUN poetry install --no-root


###########################################################################
# Build lint image
###########################################################################
FROM dev-env AS dev-linter
COPY ./setup.cfg /app/
RUN pylama -o setup.cfg


###########################################################################
# Build utest coverage image
###########################################################################
FROM dev-env AS dev-coverage
RUN coverage run -m pytest -p no:warnings --cov=. --cov-report html --cov-report xml
RUN mkdir -p /var/src/htmlcov \
  && cp -r htmlcov  /var/src/htmlcov \
  && cp coverage.xml /var/src/coverage.xml

###########################################################################
# Build security check image
###########################################################################
FROM dev-env AS dev-security
RUN python -m bandit -r /var/src/app/.
RUN python -m safety check


###########################################################################
# Build debugger
###########################################################################
# FROM dev-base as debug
# RUN pip install debugpy

# WORKDIR /app/
# CMD python -m debugpy --wait-for-client --listen 0.0.0.0:5678 \
#   -m uvicorn app.main:app --reload --log-level debug --host 0.0.0.0 --port 8080 --root-path /


###########################################################################
# Build production image - api
###########################################################################
FROM dev-base as prd
VOLUME [ "/data" ]

# use Gunicorn running Uvicorn workers in the container
CMD /start.sh

# running a single Uvicorn process
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
