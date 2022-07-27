FROM python:3.9-slim-buster AS build

WORKDIR /integration

RUN pip install pytest httpx

COPY ./integration /integration
CMD ["/bin/bash", "startTest.sh"]
