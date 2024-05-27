from hubconf import custom
import time
import cv2
import math

class custom_yolov7_run:
    '''
    240524
    A module has been created based on the official YOLOv7 repository to produce inference 
    results in the form of a list of dictionaries when a numpy image is input
    '''
    def __init__(self, model_path, center_point=None, roi_box=None, conf_thresh=0.25, nms_thresh=0.45):
        '''
        model_path: Path to the YOLOv7 weight file
        center_point: [x, y] The center point of the image for measuring the distance of an object (defaults to the bottom center if not provided)
        roi_box: [x1, y1, x2, y2] Set the region of interest for object recognition (views the entire area if not provided)
        conf_thresh: Set the confidence threshold for object recognition
        nms_thresh: Set the non-maximum suppression threshold for object recognition

        '''
        self.model = custom(path_or_model = model_path, conf_thresh=conf_thresh, nms_thresh=nms_thresh)
        self.center_point = center_point
        self.roi_box = roi_box

    def detect(self, bgr_img):
        '''
        return dic_list from image after inference
        img: bgr image from cv2 library
        '''
        # 이미지 bgr -> rgb
        self.bgr_img = bgr_img # 나중에 그릴 때 사용
        self.img = cv2.cvtColor(self.bgr_img, cv2.COLOR_BGR2RGB)
        # 인퍼런스
        start = time.time()
        results = self.model(self.img).pandas().xyxy[0]
        spent_time = round(time.time() - start, 3)
        # 후처리
        dic_list = []
        for idx, row in results.iterrows():
            bbox = [int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])]
            conf = round(row['confidence'], 3)
            class_no = row['class']
            name = row['name']
            dic_list.append({'bbox':bbox, 'conf':conf, 'class_no':class_no, 'name':name, 'inf_time':spent_time})
        # bbox가 roi_box에 걸쳐 있지 않을 경우 모두 삭제
        if self.roi_box != None:
            new_dic_list = []
            for dic in dic_list:
                if self.calculate_iou(dic['bbox'], self.roi_box) > 0:
                    new_dic_list.append(dic)
            dic_list = new_dic_list
        # center_point으로부터 각 사물의 직선 거리 계산
        if self.center_point == None:
            h, w, c = bgr_img.shape
            self.center_point = [int(w/2), h]
        for i, dic in enumerate(dic_list):
            x1, y1, x2, y2 = dic['bbox']
            dic_center_x = int((x1+x2)/2)
            dic_center_y = int((y1+y2)/2)
            dic_center = [dic_center_x, dic_center_y]
            dic_list[i]['distance_from_center'] = self.calculate_distance(self.center_point, dic_center)
        # distance_from_center가 짧은 순으로 sort
        self.dic_list = sorted(dic_list, key=lambda x: x['distance_from_center'])
        return self.dic_list
    
    def draw(self):
        '''
        draw result to self.img by self.dic_list
        '''
        for dic in self.dic_list:
            cv2.rectangle(self.bgr_img, (dic['bbox'][0], dic['bbox'][1]), (dic['bbox'][2], dic['bbox'][3]), (0,0,255), 2)
            text = f'{dic["name"]}:{dic["conf"]}, dist:{dic["distance_from_center"]}'
            cv2.putText(self.bgr_img, text, (dic['bbox'][0], dic['bbox'][1]+25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        return self.bgr_img
    
    def calculate_iou(self, bbox1, bbox2):
        """
        calculate iou from 2 bounding box
        bbox1, bbox2 form: [x1, y1, x2, y2]
        """
        # bbox 좌표 파싱
        x1_min, y1_min, x1_max, y1_max = bbox1
        x2_min, y2_min, x2_max, y2_max = bbox2
        # 교차 영역의 좌표 계산
        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)
        # 교차 영역의 너비와 높이 계산
        inter_width = max(0, inter_x_max - inter_x_min)
        inter_height = max(0, inter_y_max - inter_y_min)
        # 교차 영역의 면적 계산
        inter_area = inter_width * inter_height
        # 각 bbox의 면적 계산
        bbox1_area = (x1_max - x1_min) * (y1_max - y1_min)
        bbox2_area = (x2_max - x2_min) * (y2_max - y2_min)
        # 두 bbox의 합집합 면적 계산
        union_area = bbox1_area + bbox2_area - inter_area
        # IoU 계산
        iou = inter_area / union_area if union_area != 0 else 0
        return iou

    def calculate_distance(self, point1, point2):
        """
        A function to calculate the straight-line distance between two points
        point1, point2: Coordinate lists of the two points [x, y]
        """
        x1, y1 = point1
        x2, y2 = point2
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return int(distance) 

if __name__ == '__main__':
    from real_sense_camera import real_sense
    # Real Sense로 영상 받아서 YOLOv7 인퍼런스 테스트
    RealSense = real_sense()
    model = custom_yolov7_run(model_path = 'weights/240501_best.pt')
    while True:
        RealSense.get_cam() # 카메라 수신
        color_img = RealSense.get_color_img()
        # depth_img = RealSense.get_depth_img()
        # depth_color_map = RealSense.get_depth_color_map()
        result = model.detect(bgr_img = color_img)
        print(result)
        cv2.imshow('YOLOv7 test', model.draw())
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break