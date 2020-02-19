FROM python:3
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:80", "wsgi:app"]

