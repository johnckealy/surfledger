import wget
from datetime import datetime as dt, timedelta as td
from pathlib import Path
from .process_gribs import process_gribs


def download_gribs(leadtime_hrs=48, forecast_interval_hrs=3):
    """ A cron script for downloading the grib files into the Gribfiles folder, ready
    for processing by the query_nomads.py script. On each run, it checks the for what
    model run it expects to find based on the current time. If it's been 4+ hours since
    the desired analysis time, it starts trying to find the files."""

    now = dt.utcnow()
    now = dt(2020, 5, 12, 12)
    base_hours = [0, 6, 12, 18]

    x = [ now.hour-base_hour  for base_hour in base_hours ]
    y = min([ now.hour-base_hour  for base_hour in base_hours if now.hour-base_hour>=2 ])
    target_base_hour = base_hours[x.index(y)]

    date = dt.strftime(now, '%Y%m%d')


    if (now.hour - target_base_hour) >= 4:
        downloaded_files = []
        for tplus in range(0, leadtime_hrs+forecast_interval_hrs, forecast_interval_hrs):
            tplus = str(tplus).zfill(3)
            target_base_hour = str(target_base_hour).zfill(2)
            localpath = '/home/jokea/code/surfledger/dataapi/Gribfiles/wavefile_{}{}-f{}.grib2'.format(date, target_base_hour, tplus)
            if not Path(localpath).exists():
                nomads_url = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/wave/prod/multi_1.{}/multi_1.glo_30m.t{}z.f{}.grib2".format(date, target_base_hour, tplus)
                print("Downloading from", nomads_url)
                try:
                    url = wget.download(nomads_url, localpath)
                    downloaded_files.append(url)
                except:
                    print("Unable to attain file. ")

        breakpoint()            
        if len(downloaded_files) > 0 and len(downloaded_files) < int(leadtime_hrs/forecast_interval_hrs):
            print("Only {} files were downloaded".format(len(downloaded_files)))
            return "No new files"
        elif len(downloaded_files) > 0:
            print("No files have been downloaded".format(len(downloaded_files)))
            return "Retry"
        else:
            print('All files downloaded okay')
            return "Okay"
        return ""



def run():

    leadtime_hrs = 12
    forecast_interval_hrs = 3

    result = download_gribs(leadtime_hrs=leadtime_hrs, forecast_interval_hrs=forecast_interval_hrs)
    if result == "Okay":
        process_gribs(leadtime_hrs=leadtime_hrs, forecast_interval_hrs=forecast_interval_hrs)
    elif result == "Retry":
        download_gribs(leadtime_hrs=leadtime_hrs, forecast_interval_hrs=forecast_interval_hrs)
        if result == "Okay":
            process_gribs(leadtime_hrs=leadtime_hrs, forecast_interval_hrs=forecast_interval_hrs)
        else:
            ValueError("There was a problem with the grib loader. Attempted one retry.")
    elif result == "No new files":
        print("No new files. Doing nothing")
    else:
        ValueError("There was a problem with the grib loader.")
