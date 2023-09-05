from __future__ import absolute_import

import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, __dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, '../..')))

from src.libs.PaddleOCR.paddleocr import PPStructure,save_structure_res


class TextExtractor:
    def __init__(self, device: str, rec_model_dir: str, det_model_dir: str, rec_char_dict_path: str):
        use_gpu = (device == "cuda")
        self.model = PPStructure(table = False, ocr = True, show_log = False, use_gpu = use_gpu, rec_model_dir = rec_model_dir, det_model_dir = det_model_dir, rec_char_dict_path = rec_char_dict_path, warm_up = True)
        
    def get_document_content(self, image):
        result = self.model(image)
        content = []
        res = p["res"]
        for p in result:
            if p["type"] not in ["text", "title", "header"] or not res:
                continue
            text = []
            for line in res:
                text.append(line["text"])
            content.append(" ".join(text))
        
        return content
    

if __name__ == "__main__":
    import cv2
    
    model = TextExtractor("cpu", "/home/tri/work/Document-Analysis/models/en_PP-OCRv3_rec_infer", "/home/tri/work/Document-Analysis/models/en_PP-OCRv3_det_infer", "/home/tri/work/Document-Analysis/models/en_dict.txt")
    
    image = cv2.imread('/home/tri/work/Document-Analysis/src/test/DocBank_samples/2.tar_1801.00617.gz_idempotents_arxiv_4_ori.jpg')
    print(model.get_document_content(image))
    