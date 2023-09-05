FROM paddlepaddle/paddle:2.5.0rc0-gpu-cuda11.7-cudnn8.4-trt8.4

# COPY models models

RUN apt update && apt upgrade -y \
    && apt install git wget

COPY . /docrev

WORKDIR /docrev

COPY requirements.txt requirements.txt

RUN pip install -U pip && pip install -r requirements.txt

RUN git clone https://github.com/PaddlePaddle/PaddleOCR.git ./src/libs/PaddleOCR

RUN ls script

RUN bash script/download.sh

EXPOSE 8501

CMD ["bash", "./script/run.sh"]
