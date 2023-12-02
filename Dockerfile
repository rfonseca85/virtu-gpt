# Use an official Python runtime as a parent image
FROM python:3.11.6-slim-bookworm

WORKDIR /usr/src/app

# Dependencies to build llama-cpp
RUN apt update && apt install -y \
  libopenblas-dev\
  ninja-build\
  build-essential\
  pkg-config\
  wget


# Copy the current directory contents into the container at /usr/src/app
COPY . .

RUN pip3 install -r requirements.txt
RUN pip3 install llama-cpp-python chroma-hnswlib

# Run Chat.py when the container launches
EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "Chat.py", "--server.port=8501", "--server.address=0.0.0.0"]

#docker build -t virtu_gpt .
#docker run -p 8501:8501 virtu_gpt




