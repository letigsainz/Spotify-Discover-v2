FROM python:3.13-alpine

WORKDIR /app

ENV FLASK_APP=spotipy/app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["python", "-m", "flask", "run"]