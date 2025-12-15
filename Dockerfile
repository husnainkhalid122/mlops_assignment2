FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python create_dataset.py && python src/train.py

CMD ["python", "src/train.py"]
