# 
FROM python:3.9.18-bullseye

ARG PROJECT_ENVIRON
ARG PROJECT_ID
ARG DEPLOY

ENV PROJECT_ENVIRON=$PROJECT_ENVIRON
ENV PROJECT_ID=$PROJECT_ID
ENV DEPLOY=$DEPLOY

ENV APP_HOME=/code
WORKDIR $APP_HOME

COPY ./requirements.txt $APP_HOME/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r $APP_HOME/requirements.txt

RUN useradd appuser && chown -R appuser $APP_HOME
USER appuser

RUN chmod +w $APP_HOME

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]