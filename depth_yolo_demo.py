from custom_yolov7_inference import custom_yolov7_run, Cuda_Check
from real_sense_camera import real_sense
import cv2

Cuda_Check()
RealSense = real_sense()
filter = None
model = custom_yolov7_run(model_path='weights/yolov7.pt', center_point=None, roi_box=None, conf_thresh=0.25, nms_thresh=0.45, filter = filter)
while True:
    RealSense.get_cam() # 카메라 수신
    color_img = RealSense.get_color_img()
    result = model.detect(bgr_img = color_img)
    result_img = model.draw()
    _ = RealSense.get_depth_img()
    depth_color_map = RealSense.get_depth_color_map()
    concat_img = cv2.hconcat([result_img, depth_color_map])
    print(result)
    cv2.imshow('YOLOv7 test', concat_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break