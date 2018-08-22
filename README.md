# fruit_recognition

Basically, it's a Flask server intended to store a tensorflow object detection model. What it does is:

- Provides API for inference
- Allows users to manually label images
- Fits the model to newly collected data (not implemented yet)

I should mention here that labelling part originated from [simple_image_annotator](https://github.com/sgp715/simple_image_annotator). It was noticeably redesigned though.

This server was written solely for educational purposes and I do realize that it contains a lot of vulnerabilities.