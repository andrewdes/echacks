import cv2
from multiprocessing import Queue, Process
import control
import cProfile
import config
from size import GridPoints

commands = Queue()


def move_camera(x, y, w, h):
    midx = x + (w/2)
    midy = y + (h/2)

    # Hardcoded values here correspond to thirds of the resolution values
    if midx < 240:
        commands.put('d')
    elif midx > 480:
        commands.put('a')

    # y-axis is at top
    if midy < 160:
        commands.put('s')
    elif midy > 320:
        commands.put('w')


def get_size(obj):
    # Index 2 references the x-width of a face
    return obj[2]

def draw_on(image, faces, grid):
    # Draw rectangle on faces and square at centers
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.rectangle(image, (x + (w/2), y + (h/2)), (x + 1 + (w/2), y + 1+ (h/2)), ( 0, 0, 255), 3)

    # Draw image split
    color = (0, 0, 0)  # Black
    cv2.line(image, (grid.minx, 0), (grid.minx, grid.sizey), color, 2)
    cv2.line(image,  (grid.maxx, 0), (grid.maxx, grid.sizey), color, 2)
    cv2.line(image, (0, grid.miny), (grid.sizex, grid.miny), color, 2)
    cv2.line(image, (0, grid.maxy), (grid.sizex, grid.maxy), color, 2)

    # Displays image
    cv2.imshow("preview", image)
    cv2.waitKey(1)



def main():
    # Config stuff
    camera_port = 1  # Port 0 is built-in, port 1 is eternal
    camera = cv2.VideoCapture(camera_port)

    if not camera.isOpened():
        print "External camera not found, please plug one in"
        return


    camera.set(3,config.sizex)
    camera.set(4,config.sizey)



    # Start arduino control process
    cmd = Process(target=control.run_control, args=((commands),))
    cmd.start()

    # Setup image processing
    frontCasc = "cascades/detection_cascade.xml"
    frontCascade = cv2.CascadeClassifier(frontCasc)
    cv2.startWindowThread()
    cv2.namedWindow("preview")

    grid = GridPoints(config.sizex, config.sizey)

    for i in range(1000):
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
        draw_on(image, faces, grid)

if __name__ == '__main__':
    cProfile.run("main()")

