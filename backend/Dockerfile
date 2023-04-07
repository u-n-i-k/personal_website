FROM python:3.10-alpine as build-stage
WORKDIR /app
COPY README.md ./
COPY pyproject.toml ./
RUN pip install .[build]
COPY . .
RUN python -m build


FROM python:3.10 as production-stage
ARG environment
# ENV ENVIRONMENT=${environment:?error}
WORKDIR /app
RUN mkdir secrets
COPY secrets/${environment} ./secrets
RUN mkdir alembic
COPY src/personal_website/alembic ./alembic
COPY --from=build-stage /app/dist/personal_website-0.0.1-py3-none-any.whl .
RUN pip install personal_website-0.0.1-py3-none-any.whl
COPY config-docker-${environment}.json ./config.json

ENTRYPOINT ["python", "-m", "personal_website"]
