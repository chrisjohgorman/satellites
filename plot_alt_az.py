#!/usr/bin/env python3
import argparse
import datetime
import matplotlib.pyplot as plt

from dateutil.parser import parse

from skyfield.api import load, wgs84, EarthSatellite
from pytz import timezone

def parse_args():
    parser = argparse.ArgumentParser(
        description='Generates a graph of Satellite altitude and azimuth' )
    parser.add_argument(
        '--tle-file', required=True,
        help='Input TLE file')
    parser.add_argument(
        '--utc', action='store_true',
        help='Show pass time in UTC')
    parser.add_argument(
        '--start-timestamp', required=True,
        help='Start timestamp in seconds since epoch')
    parser.add_argument(
        '--length-pass', required=True,
        help='Pass time in seconds')
    parser.add_argument(
        '--lat', required=True, type=float,
        help='Groundstation latitude (degrees)')
    parser.add_argument(
        '--lon', required=True, type=float,
        help='Groundstation longitude (degrees)')
    parser.add_argument(
        '--alt', default=0.0, type=float,
        help='Groundstation altitude (meters) [default=%(default)r]')
    return parser.parse_args()


def plot_sky(pass_indices, t, tz, az, alt):
    i, j = pass_indices
    print('Rises:', t[i].astimezone(tz))
    print('Sets:', t[j].astimezone(tz))

    # Set up the polar plot.
    ax = plt.subplot(111, projection='polar')
    ax.set_rlim([0, 90])
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    # Draw line and labels.
    θ = az.radians
    r = 90 - alt.degrees
    ax.plot(θ[i:j], r[i:j], 'ro--')
    for k in range(i, j):
        text = t[k].astimezone(tz).strftime('%H:%M')
        ax.text(θ[k], r[k], text, ha='right', va='bottom')


def main():
    args = parse_args()
    with open(args.tle_file) as f:
        lines = f.readlines()
    if len(lines) != 3:
        raise RuntimeError('TLE file must have 3 lines')

    plt.rcParams['figure.figsize'] = 7, 7
    
    if(args.utc):
        tz = timezone('GMT')
    else: 
        tz = timezone('Canada/Eastern')

    seconds = range(0,int(args.length_pass),90)
    time = datetime.datetime.utcfromtimestamp(float(args.start_timestamp))
    ts = load.timescale()
    t = ts.utc(time.year, time.month, time.day, time.hour, time.minute, seconds)

    satellite = EarthSatellite(lines[1], lines[2], 'satellite', ts)
    groundstation = wgs84.latlon(args.lat, args.lon, args.alt)
    orbit = (satellite - groundstation).at(t)
    alt, az, distance = orbit.altaz()

    above_horizon = alt.degrees > 0

    indicies, = above_horizon.nonzero()

    plot_sky([indicies[0], indicies[-1]], t, tz, az, alt)

    plt.show()


if __name__ == '__main__':
    main()
