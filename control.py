import time

def run_control(commands):
    while True:
        if commands.empty():
            continue
        else:
            print commands.get()
            # Actually handle arduino stuff here
        time.sleep(0.02)