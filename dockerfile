FROM python:3.9.1

WORKDIR /app/
RUN pip3 install pipenv
COPY . .
RUN pipenv install --system --dev
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]