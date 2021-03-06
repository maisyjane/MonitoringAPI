FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5002
ENTRYPOINT ["python3"]
CMD ["src/app.py"]