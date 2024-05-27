
# Object Detection Package for Moving Platform

## Introduction

Hello, this is Ryan from the AI Convergence Technology Research Institute.

We had a meeting today with Mr. Kyunghun Kim and Mr. Sreejit regarding the development of an object detection model for the moving platform. Below is the summary of our discussion:

### Object Detection Test Environment

1. **Hardware**: 
   - Moving platform, RealSense camera with 2D RGB sensor, Jetson Orin Nano Developer Kit 8GB.
   - When the air purifier is installed: Change to NU4100 (2LL + 2D RGB sensor).

2. **Image Input Size for Object Detection AI Model**: 
   - YOLOv7 416x320 (same as the air purifier model).

3. **Obstacle Distance Detection Implementation**: 
   - Using pixel distance.

### Camera Specifications and Setup

- **Camera Specifications**: 
  - Image size should be confirmed and be 640x480 or less due to the large amount of image data. This minimizes the data load on the robot side.
  - The best model that can run on the NU4100, confirmed through various experiments, is YOLOv7 480x288, with a total of 138,240 pixels. The optimal image size for the NU4100, considering the modified global shutter image size and similar ratio, is 416x320 with 133,120 pixels.

- **Camera Setup**:
  - Two cameras are used to check two views simultaneously. The moving platform will have an upper view RealSense camera, while the air purifier will have an upper 2D RGB camera looking downwards.
  - The air purifier's 2D RGB camera will be installed at an angle looking down from above. Avoidance criteria will be created based on the pixel distance to detected objects. While the exact distance cannot be known, a rough avoidance method will be implemented.

## Development Details

We will develop an object detection package and deliver it to Mr. Sreejit.

1. **Input Data**: Numpy image.
2. **Return Data**: List containing the results of object detection.
   - `class_name`: Name of the detected object.
   - `bbox`: Bounding box pixel coordinates of the detected object.
   - `conf`: Confidence of the detected object.
   - `dist`: Calculated straight-line pixel distance between the camera and the center point of the detected object (sorted by shortest distance).
   - Example return data: `[{‘class_name’: 'pee', ‘bbox’:[x1, y1, x2, y2], ‘conf’:0.79, ‘dist’:50}]`
3. **Object Detection Package Configuration Parameters**:
   - `conf_thresh`: Only detects objects with confidence above this threshold.
   - `jitter_cnt`: The object must be detected continuously for the specified counter to be recognized.
   - `roi`: Region Of Interest. A box defined by x1, y1, x2, y2, where object detection is performed within this area.
   - `nms_thresh`: IOU threshold to remove duplicate objects when multiple objects of the same class overlap.
   - Note: These parameters may be changed as needed.

## Post-Development Plan

Using the provided object detection package, we plan to implement object avoidance during autonomous driving.

Thank you.

---

### (한글 번역)
# 이동 플랫폼용 물체 인식 패키지

## 소개

안녕하세요. AI 융합 기술 연구소의 라이언입니다.

오늘 이동 플랫폼을 위한 물체 인식 모델 개발과 관련하여 김경훈 책임님, 스리짓 책임님과 회의를 했습니다. 아래는 회의 내용 요약입니다.

### 물체 인식 테스트 환경

1. **하드웨어**:
   - 이동 플랫폼, 2D RGB 센서가 있는 RealSense 카메라, Jetson Orin Nano Developer Kit 8GB.
   - 공기 청정기 설치 시: NU4100 (2LL + 2D RGB 센서)로 변경.

2. **물체 인식 AI 모델 이미지 입력 크기**:
   - YOLOv7 416x320 (공기 청정기 모델과 동일).

3. **장애물 거리 감지 구현**:
   - 픽셀 거리를 사용.

### 카메라 사양 및 설정

- **카메라 사양**:
  - 이미지 크기는 많은 양의 이미지 데이터를 최소화하기 위해 640x480 이하로 확정되어야 합니다. 이는 로봇 측 데이터 부하를 최소화합니다.
  - 다양한 실험을 통해 NU4100에서 실행할 수 있는 최적의 모델은 총 138,240 픽셀의 YOLOv7 480x288로 확인되었습니다. 수정된 글로벌 셔터 이미지 크기 및 유사 비율을 고려할 때 NU4100에 최적의 이미지 크기는 133,120 픽셀의 416x320입니다.

- **카메라 설정**:
  - 두 대의 카메라는 동시에 두 개의 뷰를 확인하는 데 사용됩니다. 이동 플랫폼에는 상단 뷰 RealSense 카메라가, 공기 청정기에는 상단 2D RGB 카메라가 아래를 바라보는 방향으로 설치됩니다.
  - 공기 청정기의 2D RGB 카메라는 위에서 아래를 내려다보는 각도로 설치됩니다. 감지된 물체와의 픽셀 거리를 기준으로 회피 기준을 생성합니다. 정확한 거리를 알 수는 없지만 대략적인 회피 방법을 구현할 예정입니다.

## 개발 내용

우리는 물체 인식 패키지를 개발하여 스리짓 책임님께 전달할 예정입니다.

1. **입력 데이터**: Numpy 이미지.
2. **반환 데이터**: 물체 인식 결과가 담긴 리스트.
   - `class_name`: 감지된 물체의 이름.
   - `bbox`: 감지된 물체의 바운딩 박스 픽셀 좌표.
   - `conf`: 감지된 물체의 신뢰도.
   - `dist`: 카메라와 감지된 물체의 중심점 사이의 직선 픽셀 거리 (가장 짧은 거리 순으로 정렬).
   - 반환 데이터 예시: `[{‘class_name’: 'pee', ‘bbox’:[x1, y1, x2, y2], ‘conf’:0.79, ‘dist’:50}]`
3. **물체 인식 패키지 설정 파라미터**:
   - `conf_thresh`: 이 임계값 이상의 신뢰도를 가진 물체만 인식합니다.
   - `jitter_cnt`: 지정된 카운터만큼 연속적으로 물체가 인식되어야 합니다.
   - `roi`: 관심 영역. x1, y1, x2, y2로 정의된 박스로, 이 영역 내에서만 물체 인식을 수행합니다.
   - `nms_thresh`: 동일 클래스의 여러 물체가 겹치는 경우 중복된 물체를 제거하기 위한 IOU 임계값.
   - 주의: 필요에 따라 이러한 파라미터는 변경될 수 있습니다.

## 개발 후 계획

제공된 물체 인식 패키지를 사용하여 자율 주행 중 물체 회피를 구현할 계획입니다.

감사합니다.
