from custom_yolov7_inference import custom_yolov7_run
from real_sense_camera import real_sense
import cv2

RealSense = real_sense()
filter = ['person', 'bottle']
model = custom_yolov7_run(model_path='weights/yolov7.pt', center_point=None, roi_box=None, conf_thresh=0.25, nms_thresh=0.45, filter = filter)
while True:
    RealSense.get_cam() # 카메라 수신
    color_img = RealSense.get_color_img()
    print(color_img.shape)
    result = model.detect(bgr_img = color_img)
    print(result)
    cv2.imshow('YOLOv7 test', model.draw())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break