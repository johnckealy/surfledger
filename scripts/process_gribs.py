import pygrib
from datetime import datetime as dt
# from matplotlib import pyplot as plt
import numpy as np
import pytz
from scipy import spatial
from dataapi.models import Spot, Forecast
from first import first
import warnings
from glob import glob
import re


def find_gridpoint(lons, lats, lonpoint, latpoint, data):
    """ Find the closest grid index on the 2D latlon grid to
    the specified lat lon point. This version of this method has
    converts the incoming lonpoint into a positive lon grid. """
    # convert longitude from -180/180 grid to 0/360 to match GRIB coords
    lonpoint = (lonpoint +360) if (lonpoint < 0) else lonpoint
    lonlats = np.array(list(zip(lons.flatten(), lats.flatten())))

    _, index = spatial.KDTree(lonlats).query([lonpoint, latpoint], k=100)
    for point in index:
        glat = lats[ lats==lonlats[point][1] ][0]
        glon = lons[ lons==lonlats[point][0] ][0]
        idx = np.where(np.logical_and(lons==glon, lats==glat))
        coords = idx[0][0], idx[1][0]
        if data[coords] != 9999:
            return coords
    raise ValueError('Couldn\'t find a result. The point is too far from the ocean.')


def get_data(grbs, name, level):
    """ Grabs the data and lat/lon grids. Also adds UTC timezone to the timestamps """
    grb = grbs.select(name=name, level=level)[0]
    data = np.array(grb.data()[0])
    lons = np.array(grb.latlons()[1])
    lats = np.array(grb.latlons()[0])
    ref_time = pytz.utc.localize(grb.analDate)
    valid_time = pytz.utc.localize(grb.validDate)

    return ref_time, valid_time, lons, lats, data


def iterate_spots(grbs, name, dbfield, level=1):
    """ First, get_data() is called to gain the data from the field. The the spots are
    iterated over using the spots database table. Each spot is located on the grib2
    grid using find_gridpoint(), and then the data point for each field is applied
    to the forecast db row. """
    ref_time, valid_time, lons, lats, data = get_data(grbs, name, level)

    for spot in Spot.objects.all():
        forecast = spot.forecast_set.filter(reference_time=ref_time).first()
        spot_lon = spot.longitude
        spot_lat = spot.latitude

        if dbfield == 'sig_ht_comb':  # only apply the valid time to the first field, preventing duplicates
            forecast.valid_times.append(valid_time)
        index = find_gridpoint(lons, lats, float(spot_lon), float(spot_lat), data)
        getattr(forecast, dbfield).append(data[index])
        forecast.save()


def read_grib(filepath):
    """ Opens the grib file, and creates a new forecast instance if the grib file
    is is the first one (t+0). Then a call to iterate_spots() will load up the
    database for each surf spot. This is done for each wave field. """
    grbs = pygrib.open(filepath)
    analdate = pytz.utc.localize(first(grbs).analDate)

    if 'f000' in filepath:
        for spot in Spot.objects.all():
            if spot.forecast_set.filter(reference_time=analdate).count() != 0:
                warnings.warn("A forecast for {} with analysis time {} already exists. It will be overridden, so please check this out.\n\n".format(spot.name, analdate))
            else:
                forecast = Forecast(reference_time=analdate, spot=spot)
                forecast.save()

    iterate_spots(grbs, 'Significant height of combined wind waves and swell', 'sig_ht_comb', level=1)
    iterate_spots(grbs, 'Primary wave mean period', 'prim_wave_period', level=1)
    iterate_spots(grbs, 'Primary wave direction', 'prim_wave_dir', level=1)
    iterate_spots(grbs, 'Significant height of wind waves', 'sig_ht_windwaves', level=1)
    iterate_spots(grbs, 'Significant height of swell waves', 'sig_ht_swellwaves1', level=1)
    iterate_spots(grbs, 'Significant height of swell waves', 'sig_ht_swellwaves2', level=2)
    iterate_spots(grbs, 'Mean period of wind waves', 'mean_windwave_period', level=1)
    iterate_spots(grbs, 'Mean period of swell waves', 'mean_swellwave_period1', level=1)
    iterate_spots(grbs, 'Mean period of swell waves', 'mean_swellwave_period2', level=2)
    iterate_spots(grbs, 'Direction of wind waves', 'windwave_dir', level=1)
    iterate_spots(grbs, 'Direction of swell waves', 'swellwave1_dir', level=1)
    iterate_spots(grbs, 'Direction of swell waves', 'swellwave2_dir', level=2)
    iterate_spots(grbs, 'Wind speed', 'wind_speed', level=1)
    iterate_spots(grbs, 'Wind direction', 'wind_dir', level=1)


GRIBFILES_PATH = '/home/jokea/code/surfledger/dataapi/Gribfiles/'



def process_gribs(leadtime_hrs, forecast_interval_hrs):
    start = dt.now()
    gribfile_regex = r"wavefile_(?P<date>\d{8})(?P<ref_time>\d{2})-f(?P<tplus>\d{3}).grib2$"
    tplus0_file = glob(GRIBFILES_PATH + "wavefile_*-f000.grib2")
    if len(tplus0_file) == 1:
        m = re.match(GRIBFILES_PATH + gribfile_regex, tplus0_file[0])
        date = m.groupdict()['date']
        ref_time = m.groupdict()['ref_time']
    else:
        raise ValueError("There should be one and only one t+0 grib file in the directory.")

    # this is done here as well as in download_gribs() to ensure all the files exist how they should
    expected_gribfiles = []
    for tplus in range(0, leadtime_hrs+forecast_interval_hrs, forecast_interval_hrs):
        tplus = str(tplus).zfill(3)
        expected_gribfiles.append(GRIBFILES_PATH+"wavefile_{}{}-f{}.grib2".format(date, ref_time, tplus))

    for glob_filename in glob(GRIBFILES_PATH+"*.grib2"):
        if glob_filename in expected_gribfiles:
            print("Opening " + glob_filename)
            read_grib(glob_filename)

    print("Completed in {}".format((dt.now() - start).total_seconds()))
