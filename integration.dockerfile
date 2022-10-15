FROM python:3.9-slim AS build

WORKDIR /integration

RUN pip install pytest httpx

ENV SMOKING_TEST_PLAN_ID=63452b0a781df10011ca0170

COPY ./integration /integration
CMD ["/bin/bash", "startTest.sh"]
