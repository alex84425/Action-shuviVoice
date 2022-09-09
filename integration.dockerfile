FROM python:3.9-slim AS build

WORKDIR /integration

RUN pip install pytest httpx

ENV SMOKING_TEST_PLAN_ID=6274e188efe3eb00129c6f47

COPY ./integration /integration
CMD ["/bin/bash", "startTest.sh"]
