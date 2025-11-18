from tools import *

import winsound
import chime
import time
import schedule

chime.theme("material")

chime.success()
time.sleep(3)

if __name__ == "__main__":

    w = 158
    cls()
    print("Welcome to Machinelearnia!")

    sl(w)
    chime.warning()
    time.sleep(3)

    sl(w)
    chime.error()
    time.sleep(3)

    sl(w)

    for i in range(5):
        print("Bip", end=" ", flush=True)
        winsound.Beep(1000, 500)
        # time.sleep(1)

    def job():
        print("Scheduled Task Executed!")

    schedule.every(5).minutes.do(job)
