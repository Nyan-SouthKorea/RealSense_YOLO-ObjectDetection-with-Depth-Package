# import
import cv2
import matplotlib.pyplot as plt

# 함수들
# %matplotlib inline # 쥬피터 노트북에서 사용 시 함수 위에 넣을 것
def show_matplot(cv2_image, title='', img_size=None):
    """
    OpenCV 이미지를 Matplotlib을 사용하여 표시하는 함수
    cv2_image: OpenCV로 읽어들인 이미지
    title: 이미지의 제목
    img_size: img_size를 넣으면 비율이 깨지지 않도록 최대한 맞춰준다
    """
    if img_size == None: # img_size를 설정하지 않을 경우 기본 10, 6으로 설정. 깨질수도 있음
        figsize = (10, 6)
    else: # 설정할 경우 가로가 10을 맞추어 최대한 비율을 맞춘다
        h = int(10 / img_size['w'] * img_size['h'])
        figsize = (10, h)
    # OpenCV는 기본적으로 BGR 형식을 사용하므로 이를 RGB 형식으로 변환
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    
    # Matplotlib을 사용하여 이미지 표시
    plt.figure(figsize=figsize)
    plt.imshow(rgb_image)
    plt.title(title)
    plt.axis('off')  # 축 제거
    plt.show()

class Txt2dic_list:
    def __init__(self, class_list, img_size):
        '''
        YOLO 형식의 txt 라벨을 dic_list로 변환
        class_list: 예시) ['person', 'cable', 'bottle'] (class 번호 순서대로)
        img_size: 정규화된 bbox값을 픽셀값으로 변환하기 위한 이미지 사이즈. 예) {'w':640,'h':480}
        '''
        self.class_dic = {}
        for i, name in enumerate(class_list):
            self.class_dic[i] = name
        self.img_size = img_size

    def transform(self, label_path):
        '''
        txt 경로를 넣으면 dic_list를 반환
        YOLO 데이터 형식 예시: class번호 x센터, y센터, x길이, y길이 (모두 0 ~ 1 정규화된 실수값)

        label_path: 레이블 경로
        '''
        with open(label_path, 'r') as f:
            full_txt = f.read()
        txt_list = full_txt.split('\n')
        dic_list = []
        for result_txt in txt_list:
            if result_txt == '': break
            class_no, w_center, h_center, w_length, h_length = result_txt.split(' ')
            class_no, w_center, h_center, w_length, h_length = int(class_no), float(w_center), float(h_center), float(w_length), float(h_length)
            class_name = self.class_dic[class_no]
            # bbox 계산 - 정규화 상태
            x1 = w_center - (w_length/2)
            y1 = h_center - (h_length/2)
            x2 = x1 + w_length
            y2 = y1 + h_length
            # bbox 계산 - 픽셀값
            x1 = int(x1 * self.img_size['w'])
            y1 = int(y1 * self.img_size['h'])
            x2 = int(x2 * self.img_size['w'])
            y2 = int(y2 * self.img_size['h'])
            # bbox 계산 - 사진 밖으로 나가지 않도록
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(self.img_size['w'], x2)
            y2 = min(self.img_size['h'], y2)
            dic_list.append({'name':class_name, 'class_no':class_no, 'bbox':[x1,y1,x2,y2], 'conf':'', 'inf_time':''})
        return dic_list
            
            
            
            
            
    