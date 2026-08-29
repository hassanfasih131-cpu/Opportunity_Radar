import os
from apscheduler.schedulers.background import BackgroundScheduler
from main import main
SCHEDULER = BackgroundScheduler()
SCHEDULER.add_job(main, 'interval', hours=6)
print("\nStarting scheduler...")
print("Automatic Scans will run every 6 hours.")
print("TYPE 'q' AND PRESS ENTER AT ANY TIME TO QUIT\n")
SCHEDULER.start()
try:
    while True:
        user_input = input().strip().lower()
        if user_input == 'q':
            print("\nStopping scheduler...\n")
            SCHEDULER.shutdown()
            os._exit(0)
except (KeyboardInterrupt, SystemExit):
    print("\nSystem interrupt detected. Exiting...\n")
    os._exit(0)

#Test
#Replace hours with seconds in line 6 for faster results