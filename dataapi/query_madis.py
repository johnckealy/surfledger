import pygrib
from datetime import datetime as dt
from matplotlib import pyplot as plt
import numpy as np
from scipy import spatial
from models import Spot



def find_gridpoint(lons, lats, lonpoint, latpoint, data):
    ''' Find the closest grid index on the 2D latlon grid to
    the specified lat lon point. '''
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
    raise ValueError('Couldn\'t find a result. The point is too far from the ocean. ')


def read_grib(filepath, wave):
    """
    """
    grbs = pygrib.open(filepath)

    sig_ht_comb = grbs.select(name='Significant height of combined wind waves and swell')[0]
    lons = np.array(sig_ht_comb.latlons()[1])
    lats = np.array(sig_ht_comb.latlons()[0])
    data = np.array(sig_ht_comb.data()[0])
    for spot in Spot.objects.all():
        print(spot)
        spot_lon = spot['longitude']
        spot_lat = spot['latitude']
        index = find_gridpoint(lons, lats, spot_lon, spot_lat, data)

    return  data[index]




    # wave['sig_ht_comb'].append()
    # wave['prim_wave_period'].append(grbs.select(name='Primary wave mean period')[0])
    # wave['prim_wave_dir'].append(grbs.select(name='Primary wave direction')[0])
    # wave['sig_ht_windwaves'].append(grbs.select(name='Significant height of wind waves')[0])
    # wave['sig_ht_swellwaves1'].append(grbs.select(name='Significant height of swell waves', level=1)[0])
    # wave['sig_ht_swellwaves2'].append(grbs.select(name='Significant height of swell waves', level=2)[0])
    # wave['mean_windwave_period'].append(grbs.select(name='Mean period of wind waves')[0])
    # wave['mean_swellwave_period1'].append(grbs.select(name='Mean period of swell waves', level=1)[0])
    # wave['mean_swellwave_period2'].append(grbs.select(name='Mean period of swell waves', level=2)[0])
    # wave['windwave_dir'].append(grbs.select(name='Direction of wind waves')[0])
    # wave['swellwave1_dir'].append(grbs.select(name='Direction of swell waves', level=1)[0])
    # wave['swellwave2_dir'].append(grbs.select(name='Direction of swell waves', level=2)[0])
    # # Canngu, Bali coords
    # spot_lon = 115.133193
    # spot_lat = -8.656691
    # sig_ht_comb = grbs.select(name='Significant height of combined wind waves and swell')[0]
    # return wave







date = '20200513'
model_base_time = '06'
tplus = '48'

nomads_url = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/wave/prod/multi_1.{}/multi_1.glo_30m.t{}z.f{}.grib2".format(date, model_base_time, tplus)

sample = 'sample.grib'




wave = {
    'sig_ht_comb': [],
    'prim_wave_period': [],
    'prim_wave_dir': [],
    'sig_ht_windwaves': [],
    'sig_ht_swellwaves1': [],
    'sig_ht_swellwaves2': [],
    'mean_windwave_period': [],
    'mean_swellwave_period1': [],
    'mean_swellwave_period2': [],
    'windwave_dir': [],
    'swellwave1_dir': [],
    'swellwave2_dir': [],
}



if __name__=='__main__':
    for tplus in [0]:#, 3, 6, 9, 12, 15, 18, 21, 24]:
        tplus = str(tplus).zfill(3)
        wave = read_grib('/home/jokea/code/surfledger/dataapi/test_gribfiles/samplef{}.grib'.format(tplus), wave)
