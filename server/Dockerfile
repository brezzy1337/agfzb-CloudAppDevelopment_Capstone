FROM python:3.8.2

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

RUN apt-get update ` \
    && apt-get install -y netcat

ENV APP=/app 

WORKDIR $APP 

COPY requirement.txt $APP 
RUN pip install --upgrade pip
RUN pip install -r requirement.txt

COPY . $APP

EXPOSE 8000

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Starts Gunicorn(Python WSGI HTTP Server for UNIX), binds the serveer to port 8000, serves the Djancgo appilcation with a WSGI entry point
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djancgobackend.wsgi"]