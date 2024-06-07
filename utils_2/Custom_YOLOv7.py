from hubconf import custom
import time
import cv2
import math
import torch
import torchvision
import time
import os
import requests

class custom_yolov7:
    '''
    240604
    학습된 YOLOv7 모델의 mAP를 측정하고 시각화 하기 위해 만들어진 패키지
    '''
    def __init__(self, model_path, img_size=None):
        '''
        model_path: YOLOv7 weight파일 경로
        conf_thresh: Set the confidence threshold for object recognition
        nms_thresh: Set the non-maximum suppression threshold for object recognition
        img_size: 입력 이미지 사이즈. resize에 사용됨. 예시: {'w':640, 'h':480}
        '''
        self.model = custom(path_or_model = model_path, conf_thresh=0.01, nms_thresh=0.45)
        self.img_size = img_size

    def detect(self, bgr_img, conf_thresh=0.25, filter=None):
        '''
        입력된 이미지로 YOLOv7 사물인식을 추론하여 결과를 dic_list로 반환한다
        img: cv2로 읽어온 bgr 형식의 이미지
        filter: 감지하고 싶은 사물만 감지 가능. 사용 예시: ['person', 'cable']
        '''
        # 이미지 리사이즈
        if self.img_size != None:
            bgr_img = cv2.resize(bgr_img, (self.img_size['w'], self.img_size['h']))
            self.resize_img = bgr_img
        # bgr-> rgb 변경
        img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        # 추론
        start = time.time()
        results = self.model(img).pandas().xyxy[0]
        inf_time = round(time.time() - start, 3)
        # 전처리
        dic_list = []
        for idx, row in results.iterrows():
            bbox = [int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])]
            conf = round(row['confidence'], 3)
            # conf를 만족하지 않으면 감지 안한 것으로 처리
            if conf < conf_thresh:
                continue
            class_no = row['class']
            name = row['name']
            # 필터 적용
            if filter != None:
                if not name in filter:
                    continue
            dic_list.append({'bbox':bbox, 'conf':conf, 'class_no':class_no, 'name':name, 'inf_time':inf_time})
        return dic_list
    
    def draw(self, img, dic_list, color):
        '''
        입력된 img에 dic_list의 결과에 따라 그림을 그린다
        img: 입력 cv2 bgr 이미지
        dic_list: 감지 결과 또는 gt
        color: 바운딩박스와 글씨의 색깔.(b, g, r) 순서의 tuple로 입력할 것
        '''
        for dic in dic_list:
            cv2.rectangle(img, (dic['bbox'][0], dic['bbox'][1]), (dic['bbox'][2], dic['bbox'][3]), color, 1)
            text = f'{dic["name"]}:{dic["conf"]}'
            cv2.putText(img, text, (dic['bbox'][0], dic['bbox'][1]+10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1) # font_scale, color, thickness
        if len(dic_list) > 0:
            cv2.putText(img, f'inf. time: {dic["inf_time"]}', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1) # font_scale, color, thickness
        return img