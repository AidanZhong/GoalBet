FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

LABEL maintainer="Aidan Zhong" \
    version="1.0.0" \
    description="GoalBet production image"