import time
import serial
import config

def run_control(commands):
    ardunio = serial.Serial()
    ardunio.baudrate = config.baudrate
    ardunio.port = config.port
    try:
        ardunio.open()
    except serial.SerialException as e:
        print "Port " + ardunio.port + " not found"
        return

    while True:
        if commands.empty():
            continue
        else:
            cmd = commands.get()
            print cmd
            ardunio.write(cmd)

        time.sleep(0.02)