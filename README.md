
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
