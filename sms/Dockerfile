# Flask docker file

# Base
FROM python:3.8-slim

# Commands
RUN mkdir -p /opt/flask_blog/
WORKDIR /opt/flask_blog/
COPY . /opt/flask_blog/
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod a+x ./run.sh

# Ports
EXPOSE 8088

# Enviroment
#ENV TZ Europe/Moscow
#ENV DEBUG True
#ENV DATABASE_URI "postgresql://flask_user:flask_user@127.0.0.1/flask_db"

# Run
#CMD ["python", "main.py"]
ENTRYPOINT ["./run.sh"]