# SafeScanEngine
## Overview
SafeScanEngine is a Python Library designed for identifying dangerous (non baby-proof) from a list of images. 
The engine was design to be an interface for more than one image processing solvers. 
For the time being, YoloV8 was implemented

## Key Features
- Can identify both lethal and non-lethal objects.

### Lethal:
- Electrical outlets
- Plastic bags (to be implemented)
- Cables/cords of any kind (to be implemented)

### Non-lethal:
- Sharp corners (to be implemented)

## Requirements
- Python 3.7 or higher
- Pillow

## Installation
To install, run: 
```shell
pip install SafeScanEngine
```

## Usage
```shell
from SafeScanEngine import YoloV8Resolver

model = YoloV8Resolver(images=["img_1.jpg", "img_no_danger.jpg", "img_2.jpg"])
results = model.return_detections()

# Process results list
for result in results:
    boxes = result["boxes"]  # Boxes as list for bbox outputs in json serializable form
    original_shape = result["original_shape"]  # Input image dimensions
    labels = result["names"]  # Labels detected (e.g. ElectricalOutlet) 
    result_image_with_label = result["encoded_image"]  # Result image (with boxes) encoded in base64
    was_danger_detected = result["danger_found"]  # Boolean always available even if nothing was detected (e.g. False)
```

## License
MIT License. See LICENSE for details.

## Contact
Reach out at dragosjosan@gmail.com for support or inquiries.
