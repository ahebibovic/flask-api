FROM python:3.8-alpine

RUN apk update
RUN pip install --no-cache-dir pipenv

WORKDIR /app
COPY Pipfile Pipfile.lock ./
COPY . .

RUN pipenv install --system --deploy

EXPOSE 5000

CMD ["pipenv", "run", "flask", "--debug", "run", "-h", "0.0.0.0"]