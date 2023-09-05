#!/bin/bash

wget https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_det_infer.tar -P ./models
wget https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_rec_infer.tar -P ./models
cd models
tar -xvf en_PP-OCRv3_det_infer.tar
tar -xvf en_PP-OCRv3_rec_infer.tar
cd ..