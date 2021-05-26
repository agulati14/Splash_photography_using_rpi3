import time
import RPi.GPIO as GPIO
from sh import gphoto2 as gp
import signal, os, subprocess

beam_pin = 17
triggerCommand = ["--trigger-capture"]

def stopgp():
    p = subprocess.Popen(['ps', '-A'],stdout=subprocess.PIPE)
    out, err = p.communicate()
    # search for gphoto process and kill if b'gvfsd-gphoto2" in line:
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            pid= int(line.split(None,1)[0])
            os.kill (pid, signal.SIGKILL)

def beam_breaks(channel):
    if GPIO.input(beam_pin):
        print('beam unbroken')
    else:
        print('beam broken')
        time.sleep(0.5)
        gp(triggerCommand)


stopgp()
GPIO.setmode(GPIO.BCM)
GPIO.setup(beam_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(beam_pin, GPIO.BOTH, callback=beam_breaks)

message = input("press enter to quit\n\n")
GPIO.cleanup()