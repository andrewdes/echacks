import cv2
from multiprocessing import Queue, Process

commands = Queue()

def move_camera(x, y, w, h):
    midx = x + (w/2)
    midy = y + (h/2)

    if midx < 427:
        commands.put('d')
    elif midx > 835:
        commands.put('a')

    # y-axis is at top
    if midy < 240:
        commands.put('s')
    elif midy > 480:
        commands.put('w')

    if not commands.empty():
        print commands.get()

def get_size(obj):
    return obj[2]

def main():
    # 0 is integrated, 1 is usb
    camera_port = 1
    camera = cv2.VideoCapture(camera_port)
    camera.set(3,1280)
    camera.set(4,720)

    frontCasc = "cascades/detection_cascade.xml"
    frontCascade = cv2.CascadeClassifier(frontCasc)
    cv2.startWindowThread()
    cv2.namedWindow("preview")

    while True:
        retval, image = camera.read()

        if image is None:
            continue

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = frontCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(40, 40),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        if len(faces) > 0:
            # Draw a rectangle around the faces
            faces = sorted(faces, key=get_size, reverse=True)
            largest = faces[0]
            move_camera(largest[0], largest[1], largest[2], largest[3])
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow("preview", image)
            # Process images as quickly as possible
            cv2.waitKey(1)

if __name__ == '__main__':
    main()

