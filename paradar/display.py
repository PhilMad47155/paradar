#
# This file is part of paradar (https://github.com/blinken/paradar).
#
# Copyright (C) 2020 Patrick Coleman
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import time
import neopixel
import math

from math import sin, asin, cos, atan2, sqrt, floor, degrees, radians, isclose
from gpsd import NoFixError
from datetime import datetime, timedelta
from itertools import cycle

try:
  from RPi import GPIO
except ImportError:
  from gpio_stub import GPIO

try:
  import board
except ImportError:
  from gpio_stub import board

from config import Config

class Display:
  _GPIO_DATA = board.D18
  _PIXEL_COUNT = 36
  # From testing, we're 180 degrees off magnetic north for bearing=0.
  # This number is given in pixels (1 pixel = 10 degrees)
  # = 18 (180 degree rotation) + 4.5 (first pixel is top-left of board, not top-center)
  _PIXEL_ANGLE_OFFSET = 18 + 4.5
  _PIXEL_TDC_OFFSET = 5 # top-dead-center is just to the left of pixel 5

  _DEGREES_PER_PIXEL = 360.0/_PIXEL_COUNT

  _COLOUR_COMPASS_NORTH = (255, 255, 255) # white
  _COLOUR_AIRCRAFT_FAR = (0, 0, 255) # blue
  _COLOUR_AIRCRAFT_NEAR = (255, 0, 0) # red
  _COLOUR_HOME = (64, 255, 30) # light green
  _COLOUR_HOME_NEAR = (64, 255, 255) # lighter green
  _COLOUR_STARTUP = (255, 255, 255) # white

  # Ignore aircraft more than this many kilometers away.
  # Some research suggests that the best humans can spot is a B747 10->50km
  # away in perfect conditions. In most cases (small aircraft, low contrast
  # against busy background) humans can see the aircraft 1->5km distant.
  # https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0005594
  _DISTANCE_SQUELCH = 30.0

  # When flight mode is on, only show aircraft within 3000ft (above or below)
  # and 15km
  _FLIGHT_MODE_VERTICAL_SEP = 3000.0 # ft
  _FLIGHT_MODE_HORIZONTAL_SEP = 15.0 # km
  _FLIGHT_MODE_ALTIMETER_MIN = 20.0 # ft, minimum height to enable the altimeter
  _FLIGHT_MODE_ALTIMETER_MAX = 1000.0 # ft
  _FLIGHT_MODE_ALTIMETER_COLOUR = (255, 142, 43) # soothing orange

  # Begin to fade the LED to from COLOUR_AIRCRAFT_FAR to .._NEAR from this
  # distance (kilometers)
  _DISTANCE_WARNING = 15.0 # km

  # Don't display aircraft closer than this distance (they're probably our own
  # ADS-B transmitter), and clamp the home location indicator to 180 degrees.
  # This is to avoid display jitter - GPS isn't much more accurate than 5m.
  _IGNORE_CLOSER_THAN = 15.0/1000 # 15m, in km

  _TEST_COLOURS = (
    (255,0,0),     # R
    (0,255,0),     # G
    (0,0,255),     # B
    (255,255,255), # W
  )

  _HIGH_BRIGHTNESS = 1.0
  _LOW_BRIGHTNESS = 0.6
  _SELFTEST_BRIGHTNESS = 0.03
  _STARTUP_BRIGHTNESS = 0.2


  def __init__(self, gps, compass):
    print("display: starting up")
    GPIO.setmode(GPIO.BCM)

    self._vectors = None
    self._vectors_last_update = datetime(1970, 1, 1, 0, 0, 0)
    self._test_cycle = cycle(self._TEST_COLOURS)
    self._home_location = None
    self._initial_altitude = None

    self.pixels = neopixel.NeoPixel(self._GPIO_DATA, self._PIXEL_COUNT,
      auto_write=False,
      bpp=3,
      brightness=self._LOW_BRIGHTNESS,
    )

    self.off()
    self._refresh()

    self._gps = gps
    self._compass = compass

  def start(self):
    '''Display a startup animation'''

    while True:
      for i in range(self._PIXEL_COUNT):
        if not self._gps.is_fresh():
          self.off()
        self.pixels[i] = self._COLOUR_STARTUP
        # Limit brightness to avoid breaking the power supply on startup
        self._refresh(brightness=self._STARTUP_BRIGHTNESS)
        time.sleep(0.02)

      if self._gps.is_fresh():
        break

    for i in range(self._PIXEL_COUNT):
      self.pixels[i] = self._COLOUR_STARTUP
      self._refresh(brightness=self._STARTUP_BRIGHTNESS)
      time.sleep(0.02)

    time.sleep(0.1)

    self.off()
    self._refresh()

  def _refresh(self, brightness=None):
    if not brightness:
      brightness = (self._HIGH_BRIGHTNESS if Config.high_brightness() else self._LOW_BRIGHTNESS)

    self.pixels.brightness=brightness
    self.pixels.show()

  def _pixel_for_bearing(self, bearing):
    uncorrected_pixel = self._PIXEL_COUNT + bearing/self._DEGREES_PER_PIXEL

    # The offset is required because pixel 1 is at the top-left of the board,
    # whereas the compass indicates 0 degrees at the top-center.
    return int((uncorrected_pixel + self._PIXEL_ANGLE_OFFSET) % (self._PIXEL_COUNT))

  # Get the barometric altitude, if available - otherwise fall back to
  # geometric altitude. Returns altitude in ft. May return None
  def _altitude(self):
    if self._compass.get_altitude():
      return self._compass.get_altitude()
    else:
      try:
        gps_p = self._gps.position_detailed()
        return gps_p.altitude()*3.281 # gps_p returns metres
      except (NoFixError, UserWarning):
        return None

  # altitude in ft, relative to turn-on (can be negative)
  def _relative_altitude(self):
    altitude = self._altitude()

    if self._initial_altitude == None and altitude != 0.0:
      self._initial_altitude = altitude
    elif self._initial_altitude == None and altitude == 0.0:
      # No stored altitude & the altimiter may not be started yet
      raise NoFixError

    return altitude - self._initial_altitude

  def _haversine(self, lat1, lon1, lat2, lon2):
    # shamelessly stolen from SO, https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points

    R = 6372.8 # earth radius, km

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))

    return R * c

  # Throws GPS.NoFixError if the GPS is not yet running
  def _calculate_bearing(self, ac):
    # We're point A, and AC is point B
    (my_lat, my_lon) = self._gps.position()
    ac_lat = ac.get("lat", None)
    ac_lon = ac.get("lon", None)

    if not ac_lat or not ac_lon:
      return

    # Special case when track_home starts up
    if isclose(my_lat, ac_lat) and isclose(my_lon, ac_lon):
      ac["distance"] = 0
      ac["bearing"] = 180
      ac["bearing_updated"] = datetime.now()
      return ac

    delta_lon = radians(ac_lon - my_lon)
    my_lat_r = radians(my_lat)
    ac_lat_r = radians(ac_lat)

    x = cos(ac_lat_r) * sin(delta_lon)
    y = cos(my_lat_r) * sin(ac_lat_r) - sin(my_lat_r) * cos(ac_lat_r) * cos(delta_lon)
    bearing = degrees(atan2(x,y))

    ac["distance"] = self._haversine(my_lat, my_lon, ac_lat, ac_lon)
    ac["bearing"] = (degrees(atan2(x, y)) + 360) % 360
    ac["bearing_updated"] = datetime.now()

    #print("display: bearing ({:.6f}, {:.6f}) -> ({:.6f}, {:.6f}) is {:.1f}, distance={:.2f}km".format(
    #  my_lat, my_lon,
    #  ac_lat, ac_lon,
    #  bearing,
    #  distance,
    #))

    return ac

  def _colour_for_distance(self, distance):
    # Colour gradient is nonlinear: aircraft that are within squelch but
    # outside warning are all displayed the same colour.
    if distance > self._DISTANCE_WARNING:
      return self._COLOUR_AIRCRAFT_FAR

    # Otherwise, interpolate evenly from the far to the near distance
    multiplier = distance/self._DISTANCE_WARNING
    far_component = [x*multiplier for x in self._COLOUR_AIRCRAFT_FAR]
    near_component = [x*(1-multiplier) for x in self._COLOUR_AIRCRAFT_NEAR]
    return [int(sum(x)) for x in zip(near_component, far_component)]

  def off(self):
    self.pixels.fill((0, 0, 0))

  # Cycles through one of a number of colours on each call
  def self_test(self):
    self.pixels.fill(next(self._test_cycle))
    self.brightness = self._SELFTEST_BRIGHTNESS
    self.pixels.show()

  # Fill the pixels like a progress indicator with the specified colour. Value
  # should be between 0.0 and 1.0.
  #
  # The fill begins from _PIXEL_TDC_OFFSET, ie just to the right of
  # top-dead-center of the display.
  def fill_percent(self, colour, value):
    value = max(0.0, value)
    value = min(1.0, value)
    #print("fill pct %{}".format(value))

    for i in range(int(self._PIXEL_COUNT * value)):
      self.pixels[(i + self._PIXEL_TDC_OFFSET) % self._PIXEL_COUNT] = colour

  # Refresh the display with the value of self.pixels
  def update(self, aircraft_list):
    self.off()

    # One call to compass means less display weirdness on update
    azimuth = self._compass.get_azimuth()
    altitude = self._altitude()
    rel_altitude = self._relative_altitude()

    if Config.flight_mode():
      #print("rel altitude: {}".format(rel_altitude))
      if rel_altitude > self._FLIGHT_MODE_ALTIMETER_MIN and rel_altitude < self._FLIGHT_MODE_ALTIMETER_MAX:
        try:
          self.fill_percent(
            self._FLIGHT_MODE_ALTIMETER_COLOUR,
            rel_altitude/self._FLIGHT_MODE_ALTIMETER_MAX,
          )
        except NoFixError:
          pass

    # Indicate compass north
    if Config.show_north():
      self.pixels[self._pixel_for_bearing(azimuth)] = self._COLOUR_COMPASS_NORTH

    # Indicate bearing to home if enabled, and we know where home is.
    # Otherwise, attempt to update the home location (track_home switch has
    # just been enabled)
    if Config.track_home() and self._home_location:
      self._calculate_bearing(self._home_location)

      if self._home_location["distance"] < self._IGNORE_CLOSER_THAN:
        # display nearby home as due south to avoid display weirdness
        bearing = (180 + azimuth) % 360
        self.pixels[self._pixel_for_bearing(bearing)] = self._COLOUR_HOME_NEAR
      else:
        bearing = (self._home_location["bearing"] + azimuth) % 360
        self.pixels[self._pixel_for_bearing(bearing)] = self._COLOUR_HOME
    elif Config.track_home() and not self._home_location:
      try:
        (lat, lon) = self._gps.position()
        # The home location is recorded ~5m south of the current location, to
        # avoid 
        self._home_location = {"lat": lat, "lon": lon}
        print("display: updated home location to {}".format(self._home_location))
      except NoFixError:
        pass
    else:
      self._home_location = None


    try:
      for ac in aircraft_list.values():
        self._calculate_bearing(ac)
    except NoFixError:
      print("display: error updating bearings - GPS does not have a fix")
      vectors = []
    except RuntimeError:
      print("display: aircraft list changed during refresh, skipping update")
      return

    # Order the list of vectors to aircraft by distance, descending - so closer
    # aircraft are displayed over farther ones. If we don't know the altitude
    # yet, display the aircraft (assume 0)
    try:
      vectors = [ (x["bearing"], x["distance"], x.get("altitude", 0)) for x in filter(lambda x: "bearing" in x.keys(), aircraft_list.values()) ]
      vectors.sort(key=lambda x: x[1], reverse=True)
    except RuntimeError:
      print("display: aircraft list changed during refresh, skipping update")
      return

    for ac_bearing, ac_distance, ac_altitude in vectors:
      # Flight mode
      if Config.flight_mode():
        if altitude and math.fabs(ac_altitude - altitude) > self._FLIGHT_MODE_VERTICAL_SEP:
          continue

        if ac_distance > self._FLIGHT_MODE_HORIZONTAL_SEP:
          continue

      if ac_distance > self._DISTANCE_SQUELCH:
        continue

      if ac_distance < self._IGNORE_CLOSER_THAN:
        continue

      bearing = (ac_bearing + azimuth) % 360
      next_pixel = self._pixel_for_bearing(bearing)
      self.pixels[next_pixel] = self._colour_for_distance(ac_distance)

    self._refresh()

