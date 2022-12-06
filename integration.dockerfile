###########################################################################
# Create requirements from poetry
###########################################################################
FROM python:3.9-slim as requirements-stage

WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN poetry export --with dev -f requirements.txt --output requirements-dev.txt --without-hashes

###########################################################################
# Build testing image
###########################################################################

FROM python:3.9-slim AS build

WORKDIR /integration

# install system dependencies
RUN apt-get update \
  && apt-get -y install --no-install-recommends \
  curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --upgrade pip

COPY --from=requirements-stage /tmp/requirements-dev.txt /opt/requirements-dev.txt
RUN pip install --no-cache-dir --upgrade -r /opt/requirements-dev.txt

COPY ./ActionTemplate-Python3/ /integration/ActionTemplate-Python3
RUN pip install -e /integration/ActionTemplate-Python3

COPY ./pyproject.toml ./poetry.lock* /integration/
COPY ./integration /integration
CMD ["/bin/bash", "startTest.sh"]
