FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


ENTRYPOINT ["flask"]

CMD ["run", "--host=0.0.0.0", "--port=5000"]
