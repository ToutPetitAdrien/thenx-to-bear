FROM python:3.9.1

WORKDIR /app/
RUN pip3 install pipenv
COPY . /app
RUN pipenv install --system --dev
CMD ["gunicorn", "--chdir", "app", "server:APP", "-w", "2", "--threads", "2", "-b", "0.0.0.0:8000"]