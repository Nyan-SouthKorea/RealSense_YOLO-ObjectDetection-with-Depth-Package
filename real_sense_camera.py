# 240514 Real Sense 카메라 사용 모듈
import pyrealsense2 as rs
import numpy as np
import cv2

class real_sense:
    def __init__(self):
        '''
        Get cv2 numpy image by Real Sense camera
        '''
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        self.pipeline.start(config)
        print('Real Sense Camera set done!')

    def get_cam(self):
        '''
        get frames from Real Sense camera.
        we get various images like rgb, depth, etc from here.
        this frame does not returned. used as self variable
        '''
        self.frames = self.pipeline.wait_for_frames()
    
    def get_color_img(self):
        '''
        this function should be activated after 'get_cam' run
        because we need 'self.frame' to get no error
        '''
        color_frame = self.frames.get_color_frame()
        if color_frame:
            self.color_image = np.asanyarray(color_frame.get_data())
            return self.color_image
        else:
            print('get_color_img 에러 발생!')
        
    def get_depth_img(self):
        '''
        this function should be ran after 'get_cam' run
        '''
        depth_frame = self.frames.get_depth_frame()
        if depth_frame:
            self.depth_image = np.asanyarray(depth_frame.get_data())
            return self.depth_image
        else:
            print('get_depth_img 에러 발생!')

    def get_depth_color_map(self):
        '''
        make color_map from 'self.depth_image'
        this function should be ran after 'get_depth_img'
        '''
        self.depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(self.depth_image, alpha=0.03), cv2.COLORMAP_JET)
        return self.depth_colormap
    
    def concat_all(self):
        '''
        concat 3 images(color_img, depth_map, depth_color_map)
        this 3 images should be made before this fuction is called
        if you call it without preparing this 3 images, the previous frame can be concated
        '''
        # checkt maximum value of depth image and scale to 8it
        scaled_depth_image = cv2.convertScaleAbs(self.depth_image, alpha=(255.0/np.max(self.depth_image)))
        depth_3d = cv2.cvtColor(scaled_depth_image, cv2.COLOR_GRAY2BGR) # change 1d depth image to 3d
        concatenated_image = cv2.hconcat([self.color_image, depth_3d, self.depth_colormap])
        return concatenated_image


if __name__ == "__main__":
    # Real Sense camera streaming
    RealSense = real_sense()
    while True:
        RealSense.get_cam() # get video from camera
        color_img = RealSense.get_color_img()
        depth_img = RealSense.get_depth_img()
        depth_color_map = RealSense.get_depth_color_map()
        cv2.imshow('Concat All', RealSense.concat_all())
        cv2.imshow('depth map', RealSense.depth_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break