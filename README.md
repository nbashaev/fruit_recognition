# fruit_recognition

Basically, it's a Flask server intended to store a tensorflow object detection model. What it does is:

- Provides API for inference
- Allows users to manually label images
- Converts newly collected data to tf-records

This server was written solely for educational purposes and I do realize that it contains a lot of vulnerabilities. See the live demo [here](http://ucomputingchain.com:5000) and do not crash it intentionally ;) Note that it is able to recognize only watermelon, pineapple, grape, banana, starfruit and dragon fruit.

I should mention here that labelling part originated from [simple_image_annotator](https://github.com/sgp715/simple_image_annotator). It was noticeably redesigned though.