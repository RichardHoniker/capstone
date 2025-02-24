import cv2
from datetime import datetime
import os


def gather_data(letter_to_capture, num_samples, file_dir):
    """Gather sequence creation and loop

    Variable(s):
        to_capture: String given for classification label
        num_samples: The amount of sequential captures per click
        file_dir: Directory to create and save file with images"""

    # Initialize camera
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    trigger_rec = False
    counter = 0
    image_num = num_samples

    # Interest size, images are saved as capture_zone -10
    capture_zone = 234

    # Width of frame from camera properties
    width = int(capture.get(3))

    # Date And Directory Creation
    now = datetime.now()
    cur_dir = file_dir + now.strftime("Session - %d.%m.%Y")
    try:
        os.mkdir(cur_dir)
    except FileExistsError:
        pass
    os.chdir(cur_dir)

    while True:
        ret, frame = capture.read()
        frame = cv2.flip(frame, 1)

        if counter == num_samples:
            trigger_rec = not trigger_rec
            counter = 0

        # Defining interest area
        cv2.rectangle(frame, (width-capture_zone, 0), (width, capture_zone), (0, 250, 150), 2)

        if trigger_rec:
            interest = frame[5: capture_zone-5, width-capture_zone+5: width-5]

            counter += 1
            image_num += 1

            # Ensure existing Files in Session aren't overwritten
            while os.path.exists(now.strftime("%d.%m.%Y %H;%M;%S ") + class_name + str(image_num) + ".jpg"):
                image_num += 1

            cv2.imwrite((now.strftime("%d.%m.%Y %H;%M;%S ") + class_name + str(image_num) + ".jpg"), interest)

        else:
            cv2.imshow("Collecting images", frame)
            k = cv2.waitKey(1)

            if k == ord(' '):
                trigger_rec = not trigger_rec
                class_name = letter_to_capture

            if k == ord('q'):
                break

            try:
                try:
                    os.chdir(cur_dir)
                    os.mkdir(class_name)
                    os.chdir(cur_dir + "/" + class_name)
                except FileExistsError:
                    os.chdir(cur_dir + "/" + class_name)
            except UnboundLocalError:
                pass

    capture.release()
    cv2.destroyAllWindows()