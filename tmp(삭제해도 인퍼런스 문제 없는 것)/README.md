# RealSense YOLOv7 Package
Real Sense카메라를 이용하여, 일정 높이(약 30cm)에서 YOLOv7으로 사물인식을 하여 값을 전달해주는 패키지

### 전달 값 상세 정보

1.	input 데이터는 numpy 이미지
2.	return 데이터는 사물인식 결과가 담긴 list
class_name = 감지된 사물의 이름
bbox = 감지된 사물의 Bounding Box 픽셀 좌표
conf = 감지된 사물의 confidence
dist = 카메라와 감지된 사물의 centerpoint와의 픽셀 직선 거리 계산(이 거리가 짧은 순으로 sort하기로 함)
기타: 1개의 사물 당 1개의 dictionary로 구성되어 list를 이룸
Return 데이터 예시) [{‘class_name’: pee, ‘bbox’:[x1, y1, x2, y2], ‘conf’:0.79, ‘dist’:50}]
3.	사물인식 패키지 설정 인자
1.	conf_thresh = 설정된 confidence 이상만 사물인식
2.	jitter_cnt = 설정된 counter만큼 사물이 연속적으로 인식되어야 인정
3.	roi = Region Of Interest. x1, y1, x2, y2로 구성된 박스 형태이며 이 영역 내에서만 사물인식을 수행함
4.	nms_thresh = 동일 class인 여러 사물이 겹치는 경우, 중복된 사물을 제거하기 위한 임계값 IOU
기타: 위 인자들은 필요에 따라 변경 예정