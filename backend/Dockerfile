FROM python:3.10-slim-bullseye AS base

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

ENV FLASK_PORT=5100
ENV FLASK_HOST=0.0.0.0
ENV CSRF_SECRET_KEY=0wkamvVia0?n$NqIRVWOG
ENV DB_USERNAME=appuser
ENV DB_USER_PASSWORD=appuser1
ENV DB_HOST=mysql-db
ENV DB_NAME=weather_db
ENV DB_PORT=3306

COPY . . 
RUN rm requirements.txt

FROM base
WORKDIR /app
# Copy the installed dependencies from the previous stage
COPY --from=base /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=base /app  .
# Define app_user group and user
RUN groupadd -g 500 app_user && useradd --shell /bin/bash -u 500 -g 500 -o -c "" -m app_user && \
chmod -R 774 /app &&  \
chown -R  app_user:app_user /app
# define app.log as STDOUT
RUN ln -sf /dev/stdout  app.log
USER app_user

EXPOSE 5100
CMD ["python", "main.py"]
