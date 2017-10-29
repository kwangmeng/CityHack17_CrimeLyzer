import face_recognition
import cv2
import json
import os
from urllib.request import urlopen, Request
from urllib.parse import urlencode
# This is a running face recognition on live video using your webcam.
# Slightly complicated but it includes some performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This function requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# function.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
video_capture.set(3,1280)
video_capture.set(4,1024)
# url = 'https://randomuser.me/api/?results=5'
# response = urlopen(url).read().decode('utf8')
# remote_data = json.loads(response)

image_list = ["kenny.jpg","json.jpg","brandon.jpg","imran.jpg"]
name_list=["Kenny","Jason","Brandon","Imran"]
# for result in remote_data['results']:
#     print(result['picture']['large'])
#     image_list.append(result['picture']['large'])
#     name_list.append(result['name']['last'])

image_dict = []
a = 0
for img in image_list:
    lol = face_recognition.load_image_file(img,"file")
    # print(lol)
    # print("between images")
    image_dict.append(lol)
    a += 1

# Load a sample picture and learn how to recognize it.
# jason_image = face_recognition.load_image_file("json.jpg")
#
# jason2_image = face_recognition.load_image_file("json2.jpg")
# kenny_image = face_recognition.load_image_file("brandon.jpg")
# imran_image = face_recognition.load_image_file("imran.jpg","file")

encoding = []
b = 0

for imgd in image_dict:
    lol = imgd
    temp = face_recognition.face_encodings(lol)[0]
    encoding.append(temp)
    b += 1

# jason_face_encoding = face_recognition.face_encodings(jason_image)[0]
# jason2_face_encoding = face_recognition.face_encodings(jason2_image)[0]
# kenny_face_encoding = face_recognition.face_encodings(kenny_image)[0]
# imran_face_encoding = face_recognition.face_encodings(imran_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
#screencount = 0
sent = False
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.2, fy=0.2)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces(encoding, face_encoding)
            name = "No Threat"
            c=0

            for item in name_list:
                if match[c]:
                    name = item
                    face_names.append(name)
                c += 1

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 5
        right *= 5
        bottom *= 5
        left *= 5

        # Face of Criminal Suspect
        if name == "Jason":
            # Draw a red box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            #Send data to server
            if sent == False:
                print("sending data")
                sent = True
                data = {
                'name' : name,
                'cctvid' : '1'
                }
                data = bytes( urlencode( data ).encode() )
                handler = urlopen( 'https://kennynkm.com/cityhack/test.php', data );
                print( handler.read().decode( 'utf-8' ) );

        # Normal Faces
        else:
            # Draw a green box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # # Play sound when found matching face
            # duration = 1  # second
            # freq = 400  # Hz
            # os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))

            # Save the current image as suspect#.jpg
            #criminal = "storage/suspect.jpg"
            #criminal = "storage/suspect%d.jpg"%screencount
            #cv2.imwrite(criminal, frame)
            #screencount +=1

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
