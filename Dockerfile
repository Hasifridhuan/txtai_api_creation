FROM python:3.9-slim

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

RUN apt-get update

COPY main.py ./
COPY data ./data
COPY final ./final

EXPOSE 5555

CMD ["python", "main.py"]