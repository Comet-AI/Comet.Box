import face_recognition
from PIL import Image, ImageDraw
import argparse
import os
import cv2
import camera
import face_recog
import numpy as np
import DBmanager
import random
# Define args property
parser = argparse.ArgumentParser()
parser.add_argument('name', help='Input face name')
parser.add_argument('-s', '--save', default='./img/knowns', help='Path to save face')
parser.add_argument('-c', '--camera', default=0, type=int, help='Camera number')
parser.add_argument('-i', '--id', default=0, type=int, help='ID number')

args = parser.parse_args()

# Main Code
if __name__ == "__main__":
    # Initialize Some Variables
    train_path = args.save
    camera_num = args.camera
    face_name = args.name
    process_this_frame = True
    count = 1
    # save path adequacy check
    assert os.path.exists(train_path)

    # Display properties
    print('Registration Module Properties {')
    print('Face Name :: ', face_name)
    print('Save Path :: ', train_path)
    print('Camera Number :: ', camera_num)
    print('}')

    # Define saving path
    face_path = train_path + '/' + face_name

    # Exception for overlapped folder name
    try:
        os.mkdir(face_path)
        print('Face directory is created :: ', face_path)
    except FileExistsError:
        print('Folder name exception :: already registered face')
    # Path adequacy check
    assert os.path.exists(face_path)

    # Set DB
    DBmanager = DBmanager.DBmanager("log.db")
    DBmanager.ShowAllWorker()

    # Set camera module
    cam = camera.VideoCamera(camera_num)
    # Camera loading assertion
    assert cam is not None

    # Camera loop
    while True:
        # Grab a single frame of video
        frame = cam.get_frame()
        # Frame loading assertion
        assert frame is not None
        copy_frame = frame.copy()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left) in face_locations:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)


        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        elif key == ord("s"):
            if face_locations.__len__() > 0:
                cv2.imwrite(face_path + '/%s%i.jpg' % (face_name, count), copy_frame)
                print('Registration Complete :: ',  '%s%i.jpg' % (face_name, count))
                count += 1
                DBmanager.InsertWorker(args.id, face_name)
                DBmanager.ShowAllWorker()
        elif key == ord("d"):
            count -= 1
            if count < 1:
                DBmanager.DeleteWorker(args.id)
                DBmanager.ShowAllWorker()
                print('Remove from DB')
            else:
                os.remove(face_path + '/%s%i.jpg' % (face_name, count))
                print('Remove Complete :: ',  '%s%i.jpg' % (face_name, count))


    # do a bit of cleanup
    cv2.destroyAllWindows()
    print('finish')