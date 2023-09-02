FROM paddlepaddle/paddle:2.5.0rc0-gpu-cuda11.7-cudnn8.4-trt8.4

WORKDIR /docrev

COPY requirements.txt requirements.txt

RUN pip install -U pip && pip install -r requirements.txt

COPY models models

COPY . docrev

RUN apt install git 

RUN git clone https://github.com/PaddlePaddle/PaddleOCR.git ./src/libs

EXPOSE 5000

CMD ["./script/run.sh"]
