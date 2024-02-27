FROM python:3.12.2-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y
RUN pip install pyaudio

COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 96

CMD ["streamlit", "run", "--server.enableCORS", "false", "--server.address", "0.0.0.0", "--server.port", "96", "main.py"]