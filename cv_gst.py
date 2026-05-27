import cv2
import signal
import sys

def gstreamer_pipeline():
    return (
        "rtspsrc location=rtsp://127.0.0.1:8080/test latency=0 ! "
        "rtph265depay ! h265parse ! nvv4l2decoder ! "
        "nvvidconv ! video/x-raw, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink emit-signals=true sync=false"
    )


def signal_exit_handler(signal, frame):
    print('Exiting...')
    video_capture.release()  # Assuming video_capture is your cv2.VideoCapture instance
    cv2.destroyAllWindows()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_exit_handler)


def show_camera():
    window_title = "RTSP Stream"
    print(gstreamer_pipeline())
    video_capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
        while True:
            ret_val, frame = video_capture.read()
            if not ret_val:
                print("No frame received")
                break  # Exit if no frame is received

            cv2.imshow(window_title, frame)

            # Check to see if the user closed the window
            if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) < 0:
                break  # Exit if window is closed

            keyCode = cv2.waitKey(10) & 0xFF
            # Stop the program on the ESC key or 'q'
            if keyCode == 27 or keyCode == ord('q'):
                break
    else:
        print("Error: Unable to open camera")
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    show_camera()
