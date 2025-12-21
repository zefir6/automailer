FROM python:3
# ADD requirements.txt templates config.py mailer_run.py get_template.py mailgun.py wsgi.py /app
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:80", "wsgi:app"]

