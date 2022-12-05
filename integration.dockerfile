FROM python:3.9-slim AS build

WORKDIR /integration

# install system dependencies
RUN apt-get update \
  && apt-get -y install --no-install-recommends \
  curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --upgrade pip

# Install python dependencies
ENV PATH="/root/.local/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python - && \
  poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /integration/
COPY ./ActionTemplate-Python3/ /integration/ActionTemplate-Python3
RUN poetry install --no-root

COPY ./integration /integration
CMD ["/bin/bash", "startTest.sh"]
