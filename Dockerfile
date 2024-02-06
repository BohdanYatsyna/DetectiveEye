FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get -y install libpq-dev gcc g++ git libgl1-mesa-glx libglib2.0-0 libgtk2.0-0

WORKDIR /DetectiveEye

COPY . /DetectiveEye

RUN apt-get update && \
    apt-get -y install libpq-dev gcc g++ git libgl1-mesa-glx libglib2.0-0 libgtk2.0-0 && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
#     Replace the above line with the next command if you have CUDA support.
#     It will give opportunity to use gpu instead of cpu for Detectron2:
#     pip3 install torch torchvision torchaudio && \
    python -m pip install 'git+https://github.com/facebookresearch/detectron2.git' && \
    pip install ultralytics

COPY . .

