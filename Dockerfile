FROM python:3.12.2-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/* \

COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 80

CMD ["streamlit", "run", "--server.enableCORS", "false", "--server.address", "0.0.0.0", "--server.port", "80", "main.py"]