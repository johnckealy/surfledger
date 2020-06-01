from django.test import TestCase
from scripts.process_gribs import find_gridpoint, process_gribs, iterate_spots, get_data
import os
from django.conf import settings
import pygrib
import numpy as np
from .models import Spot, Forecast
from datetime import datetime
# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from first import first



class GribQueryTests(TestCase):

    def setUp(self):
        self.grib = pygrib.open(os.path.join(settings.BASE_DIR, 'dataapi/test_gribfiles/samplef000.grib'))

    def tearDown(self):
        self.grib.close()

    def test_find_gridpoint_combined_ww_and_swell_positive_lon(self):
        spot_lon = 115.133193 # Canngu, Bali coords
        spot_lat = -8.656691
        sig_ht_comb = self.grib.select(name='Significant height of combined wind waves and swell')[0]

        self.lats = np.array(sig_ht_comb.latlons()[0])
        self.lons = np.array(sig_ht_comb.latlons()[1])
        self.data = np.array(sig_ht_comb.data()[0])
        result = find_gridpoint(self.lons, self.lats, spot_lon, spot_lat, self.data)

        self.assertEqual((self.lats[result], self.lons[result]), (-9.0, 115.0))

    def test_find_gridpoint_mean_period_swellwaves_negative_lon(self):
        spot_lon =  -97.0 # puerto escondido coords
        spot_lat = 15.5
        sig_ht_comb = self.grib.select(name='Mean period of swell waves')[0]

        self.lats = np.array(sig_ht_comb.latlons()[0])
        self.lons = np.array(sig_ht_comb.latlons()[1])
        self.data = np.array(sig_ht_comb.data()[0])
        result = find_gridpoint(self.lons, self.lats, spot_lon, spot_lat, self.data)

        self.assertEqual((self.lats[result], self.lons[result]), (15.5, -97.0+360))




class GribDownloadTests(TestCase):
    fixtures = ["spots.json"]

    def setUp(self):
        self.grbs = pygrib.open(os.path.join(settings.BASE_DIR, 'dataapi/test_gribfiles/samplef000.grib'))

    def tearDown(self):
        self.grbs.close()

    def test_get_data(self):
        ref_time, valid_time, lons, lats, data = get_data(self.grbs, name='Significant height of wind waves', level=1)
        self.assertIsInstance(ref_time, datetime)
        self.assertIsInstance(valid_time, datetime)
        self.assertEqual(lons[200,200], 100.0)
        self.assertEqual(lats[200,200], -22.5)
        self.assertEqual(data[200,200], 1.49)
