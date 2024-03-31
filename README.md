# vision_tuner
VisionTuner that uses Python to calibrate the camera and correct distortion using the checker board

## Demo
I used a 25mm, 10*7 checkerboard, and I did a demo test with a 4k video taken using IPhon 12Pro.

### Camera Calibration Results
* The number of selected images = 60
* RMS error = 1.15726953706536
* Camera matrix (K) = 
[[3.18816909e+03 0.00000000e+00 1.11076247e+03]
 [0.00000000e+00 3.19612695e+03 1.90043191e+03]
 [0.00000000e+00 0.00000000e+00 1.00000000e+00]]
f_x : 3.18816909e+03, f_y : 3.19612695e+03, c_x : 1.11076247e+03, c_y : 1.90043191e+03
* Distortion coefficient (k1, k2, p1, p2, k3, ...) = [ 0.22125843 -1.01097428 -0.00255046  0.00553067  1.87040275]

### Distortion Correction
* Original
![스크린샷 2024-03-31 오후 11 04 23](https://github.com/seokkkkkk/vision_tuner/assets/66684504/a0374990-511a-4a33-b0fd-b477fb2f852b)
* Rectified
![스크린샷 2024-03-31 오후 11 04 08](https://github.com/seokkkkkk/vision_tuner/assets/66684504/80af2b62-33f6-4222-88da-d73b55e76769)
* Video
https://github.com/seokkkkkk/vision_tuner/assets/66684504/105cc515-1877-419d-b1e0-d948adf9a617

