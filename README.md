# AcuRiteSDR
Use a SDR receiver to decode, store, and post to wunderground data from Acurite 5-in-1 weather stations


Use the following cron tasks to run the application

    #upload latest data to wunderground every 10 mins
    */10 * * * * /usr/bin/python /home/pi/wund.py > wund.log 2>&1
    #restart rtl process nightly. Prevents memory leaks and resets rain gauge to 0.
    00 00 * * * cd /home/pi; kill `pgrep rtl_433`; sleep 15;  /usr/bin/python /home/pi/wx.py > wxrestart.log 2>&1

