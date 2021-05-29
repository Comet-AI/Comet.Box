import face_recognition
from PIL import Image, ImageDraw
import argparse
import os
import cv2 as cv
import camera
import face_recog
import numpy as np
import DBmanager


def display_result(frame, face_outs):
    # Display the results
    for (top, right, bottom, left), name in face_outs:
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        overlap = False

        avg = int(sum(frame[max(top-int((bottom-top)/5), 0)][left + int((right - left) / 2)]) / 3)
        if avg > 100:
            overlap = True

        # if there is overlap, then change box color
        if DBmanager.GetIDByName(name) is not None:
            ID = DBmanager.GetIDByName(name)[0]
            if overlap is True:
                DBmanager.UpdateRecent(ID)
                box_color = (0, 0, 255)
            else:
                DBmanager.AddWarnings(ID)
                box_color = (255, 0, 0)

            # Draw a box around the face
            cv.rectangle(frame, (left, top), (right, bottom), box_color, 2)

            # Draw a label with a name below the face
            cv.rectangle(frame, (left, bottom - 35), (right, bottom), box_color, cv.FILLED)
            font = cv.FONT_HERSHEY_DUPLEX
            cv.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    return frame

# Main Code
if __name__ == "__main__":
    # Define args property
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('--train', default='./img/knowns',
                        help='Input training image-set path')
    parser.add_argument('--test', type=int, default=0,
                        help='Input test web-cam number.')
    args = parser.parse_args()

    # Initialize Some Variables
    train_path = []
    test_path = []

    # Input Parameter Adequacy Check
    print('Camera Mode On')
    # Only existed path is allowed
    assert os.path.exists(args.train)
    print('Train Path :: ', args.train)
    train_path = args.train
    # Default Camera number is 0
    try:
        test_path = int(args.test)
    except ValueError:
        test_path = 0
    print('Camera Number :: ', test_path)

    # Set window
    winName = 'Frame'
    cv.namedWindow(winName, cv.WINDOW_NORMAL)

    # Set DB
    DBmanager = DBmanager.DBmanager("log.db")
    os.system('cls')
    DBmanager.ShowAllWorker()

    # Get known image from train_path
    cam = camera.VideoCamera(test_path)
    face_recog = face_recog.FaceRecog(train_path)

    frequency = 60
    frequency_count = 0
    while True:
        frequency_count += 1
        if frequency_count % frequency is 0:
            os.system('cls')
            DBmanager.ShowAllWorker()

        frame = cam.get_frame()
        frame = cv.resize(frame, dsize=(640, 480), interpolation=cv.INTER_AREA)

        face_recog_outs = face_recog.get_box(frame)
        frame = display_result(frame, face_recog_outs)
        # show the frame
        cv.imshow(winName, frame)
        key = cv.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv.destroyAllWindows()
    print('Finish')
    exit()

# End