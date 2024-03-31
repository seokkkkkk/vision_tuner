import numpy as np
import cv2 as cv


def select_img_from_video(video, pattern, select_all=False, wait_msec=10, wnd_name='Camera Calibration'):
    # Open video
    video = cv.VideoCapture(video)
    assert video.isOpened()

    # Select image
    img_select = []
    while True:
        # Grab an images from the video
        valid, img = video.read()
        if not valid:
            break

        if select_all:
            img_select.append(img)
        else:
            # Show images
            display = img.copy()
            cv.putText(display, f'NSelect: {len(img_select)}', (10, 150), cv.FONT_HERSHEY_DUPLEX, 5, (0, 255, 0))
            cv.imshow(wnd_name, display)

            # Process the key event
            key = cv.waitKey(wait_msec)
            if key == ord(' '):
                complete, pts = cv.findChessboardCorners(img, pattern)
                cv.drawChessboardCorners(display, pattern, pts, complete)
                cv.imshow(wnd_name, display)
                key = cv.waitKey()
                if key == ord('\r'):
                    img_select.append(img)
            if key == 27:
                break

    cv.destroyAllWindows()
    return img_select


def calib_camera_from_chessboard(images, pattern, cellsize, K=None, dist_coeff=None, calib_flags=None):
    # Find 2D corner points from given images
    img_points = []
    for img in images:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        complete, pts = cv.findChessboardCorners(gray, board_pattern)
        if complete:
            img_points.append(pts)
    assert len(img_points) > 0

    # Prepare 3D points of the chess board
    obj_pts = [[c, r, 0] for r in range(pattern[1]) for c in range(pattern[0])]
    obj_points = [np.array(obj_pts, dtype=np.float32) * cellsize] * len(img_points) # Must be `np.float32`

    # Calibrate the camera
    return cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], K, dist_coeff, flags=calib_flags)


def undistort_video(video_file, K, dist_coeff):
    # Open a video
    video = cv.VideoCapture(video_file)
    assert video.isOpened(), 'Cannot read the given input, ' + video_file

    # Run distortion correction
    show_rectify = True
    map1, map2 = None, None
    while True:
        # Read an image from the video
        valid, img = video.read()
        if not valid:
            break

        # Rectify geometric distortion (Alternative: `cv.undistort()`)
        info = "Original"
        if show_rectify:
            if map1 is None or map2 is None:
                map1, map2 = cv.initUndistortRectifyMap(K, dist_coeff, None, None, (img.shape[1], img.shape[0]), cv.CV_32FC1)
            img = cv.remap(img, map1, map2, interpolation=cv.INTER_LINEAR)
            info = "Rectified"
        cv.putText(img, info, (10, 150), cv.FONT_HERSHEY_DUPLEX, 5, (0, 255, 0))

        # Show the image and process the key event
        cv.imshow("Geometric Distortion Correction", img)
        key = cv.waitKey(10)
        if key == ord(' '):     # Space: Pause
            key = cv.waitKey()
        if key == 27:           # ESC: Exit
            break
        elif key == ord('\t'):  # Tab: Toggle the mode
            show_rectify = not show_rectify

    video.release()
    cv.destroyAllWindows()


def save_calibration_results(filepath, rms, K, dist_coeff, img_count):
    with open(filepath, 'w') as file:
        file.write('## Camera Calibration Results\n')
        file.write(f'* The number of selected images = {img_count}\n')
        file.write(f'* RMS error = {rms}\n')
        file.write(f'* Camera matrix (K) = \n{K}\n')
        dist_coeff_flat = dist_coeff.flatten()
        file.write(f'* Distortion coefficient (k1, k2, p1, p2, k3, ...) = {dist_coeff_flat}\n')


if __name__ == '__main__':
    video_file = '../sample/IPhone12Pro_4k_30fps.MOV'
    output_video_file = '../sample/undistorted_output.MP4'
    board_pattern = (10, 7)
    cellsize = 0.025

    img_select = select_img_from_video(video_file, board_pattern)
    assert len(img_select) > 0, 'No selected images!'
    rms, K, dist_coeff, rvecs, tvecs = calib_camera_from_chessboard(img_select, board_pattern, cellsize)

    # Save calibration results
    save_path = '../sample/calibration_results.txt'
    save_calibration_results(save_path, rms, K, dist_coeff, len(img_select))
    print(f'Calibration results saved to {save_path}')

    # Undistort and save the video
    print('Undistorting and saving the video...')
    undistort_video(video_file, K, dist_coeff)
    print(f'Video saved to {output_video_file}')
