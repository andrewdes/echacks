import cv2
from multiprocessing import Queue, Process
import control

commands = Queue()


def move_camera(x, y, w, h):
    midx = x + (w/2)
    midy = y + (h/2)

    # Hardcoded values here correspond to thirds of the resolution values
    if midx < 427:
        commands.put('d')
    elif midx > 835:
        commands.put('a')

    # y-axis is at top
    if midy < 240:
        commands.put('s')
    elif midy > 480:
        commands.put('w')


def get_size(obj):
    # Index 2 references the x-width of a face
    return obj[2]


def main():
    # Config stuff
    camera_port = 1  # Port 0 is built-in, port 1 is eternal
    camera = cv2.VideoCapture(camera_port)
    camera.set(3,1280)
    camera.set(4,720)

    # Start arduino control process
    cmd = Process(target=control.run_control, args=((commands),))
    cmd.start()

    # Setup image processing
    frontCasc = "cascades/detection_cascade.xml"
    frontCascade = cv2.CascadeClassifier(frontCasc)
    cv2.startWindowThread()
    cv2.namedWindow("preview")

    while True:
        # Read in image
        retval, image = camera.read()
        if image is None:
            continue

        # Convert image to greyscale temporarily to find faces
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = frontCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(40, 40),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # Process the faces that are found
        if len(faces) > 0:
            # Sort faces in order of size
            faces = sorted(faces, key=get_size, reverse=True)
            largest = faces[0]

            # Based off the largest face, determine if camera should be moved
            move_camera(largest[0], largest[1], largest[2], largest[3])
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Displays image
            cv2.imshow("preview", image)
            cv2.waitKey(1)

if __name__ == '__main__':
    main()

