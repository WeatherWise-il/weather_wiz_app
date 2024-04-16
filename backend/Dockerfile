FROM arm64v8/python:3.10-slim-bullseye

WORKDIR /app
COPY requirements.txt .
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

ENV FLASK_PORT=5100
ENV FLASK_HOST=0.0.0.0
ENV CSRF_SECRET_KEY=0wkamvVia0?n$NqIRVWOG
ENV DB_USERNAME=appuser
ENV DB_USER_PASSWORD=appuser1
ENV DB_HOST=mysql_db
ENV DB_NAME=weather_db
ENV DB_PORT=3306

COPY . .
# Define app_user group and user
RUN groupadd -g 500 app_user && useradd --shell /bin/bash -u 500 -g 500 -o -c "" -m app_user && \
chmod -R 774 /app &&  \
chown -R  app_user:app_user /app
# define app.log as STDOUT
RUN ln -sf /dev/stdout  app.log
USER app_user

EXPOSE 5100
CMD ["python", "main.py"]
