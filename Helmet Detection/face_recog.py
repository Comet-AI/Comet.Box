# face_recog.py

import face_recognition
import cv2
import camera
import os
import numpy as np

class FaceRecog():
    def __init__(self, train_path):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.

        # Extract face list from directory
        face_list = [face for face in os.listdir(train_path)
                     if os.path.isdir(os.path.join(train_path, face))]

        # There must be at least one registered face
        assert face_list.__len__() > 0
        print('Number of Faces :: ', face_list.__len__())
        print('Registered Face :: ', face_list)


        self.known_face_encodings = []
        self.known_face_names = []

        # Load sample pictures and learn how to recognize it.
        #dirname = train_path
        #files = os.listdir(dirname)
        #for filename in files:
        #    name, ext = os.path.splitext(filename)
        #    if ext == '.jpg':
        #        self.known_face_names.append(name)
        #        pathname = os.path.join(dirname, filename)
        #        img = face_recognition.load_image_file(pathname)
        #        face_encoding = face_recognition.face_encodings(img)[0]
        #        self.known_face_encodings.append(face_encoding)

        for face in face_list:
            for img in os.listdir(os.path.join(train_path, face)):
                img_path = train_path + '/' + face + '/' + img
                image_file = face_recognition.load_image_file(img_path)
                face_locations = face_recognition.face_locations(image_file)
                face_encodings = face_recognition.face_encodings(image_file, face_locations)
                if face_encodings.__len__() > 0:
                    self.known_face_encodings.append(face_encodings[0])
                    self.known_face_names.append(face)
                else:
                    print('Encoding Exception :: No face in image file (', img_path, ')')


        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

    def get_frame(self, frame):

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                min_value = min(distances)

                # tolerance: How much distance between faces to consider it a match. Lower is more strict.
                # 0.6 is typical best performance.
                name = "Unknown"
                if min_value < 0.6:
                    index = np.argmin(distances)
                    name = self.known_face_names[index]

                self.face_names.append(name)

        self.process_this_frame = not self.process_this_frame
        return self.display_results(frame)

    def get_box(self, frame):

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                min_value = min(distances)

                # tolerance: How much distance between faces to consider it a match. Lower is more strict.
                # 0.6 is typical best performance.
                name = "Unknown"
                if min_value < 0.6:
                    index = np.argmin(distances)
                    name = self.known_face_names[index]

                self.face_names.append(name)

        self.process_this_frame = not self.process_this_frame
        return zip(self.face_locations, self.face_names)

    def display_results(self, frame):
        # Display the results
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        return frame

    def get_jpg_bytes(self, frame):
        postFrame = self.get_frame(frame)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpg = cv2.imencode('.jpg', postFrame)
        return jpg.tobytes()


if __name__ == '__main__':
    face_recog = FaceRecog('./img/knowns')
    print(face_recog.known_face_names)
    cam = camera.VideoCamera(0)

    while True:
        frame = cam.get_frame()
        postFrame = face_recog.get_frame(frame)

        # show the frame
        cv2.imshow("Frame", postFrame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    print('finish')
