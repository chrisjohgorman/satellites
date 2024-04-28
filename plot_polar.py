#!/usr/bin/env python3
import argparse
import datetime
import matplotlib.pyplot as plt

from dateutil.parser import parse

from skyfield.api import load, wgs84, EarthSatellite
from pytz import timezone

def parse_args():
    parser = argparse.ArgumentParser(
        description='Generates a graph of Satellite pass on a polar plot' )
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
    
    # Set up the polar plot.
    ax = plt.subplot(111, projection='polar')
    ax.set_rlim([0, 90])
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    # Draw line and labels.
    θ = az.radians
    r = 90 - alt.degrees
    ax.plot(θ[i:j+1], r[i:j+1], 'ro--')
    for k in range(i, j+1):
        text = t[k].astimezone(tz).strftime('%H:%M:%S')
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

    time0 = datetime.datetime.utcfromtimestamp(float(args.start_timestamp))
    time1 = datetime.datetime.utcfromtimestamp(float(args.start_timestamp)) + datetime.timedelta(0, int(args.length_pass))
    ts = load.timescale()
    t0 = ts.utc(time0.year, time0.month, time0.day, time0.hour, time0.minute, time0.second)
    t1 = ts.utc(time1.year, time1.month, time1.day, time1.hour, time1.minute, time1.second)
    t = ts.linspace(t0, t1, (int(args.length_pass) // 90))
    satellite = EarthSatellite(lines[1], lines[2], 'satellite', ts)
    groundstation = wgs84.latlon(args.lat, args.lon, args.alt)
    orbit = (satellite - groundstation).at(t)
    alt, az, distance = orbit.altaz()

    plot_sky([0, len(t) -1], t, tz, az, alt)

    plt.show()


if __name__ == '__main__':
    main()
