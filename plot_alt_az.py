#!/usr/bin/env python3
import argparse
import datetime
import matplotlib.pyplot as plt
import numpy as np

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
    print('Rises:   ', t[i].astimezone(tz), '\t\tAz:', round(az.degrees[i]), 
          '\u00b0', ' Alt:', round(alt.degrees[i], 1), '\u00b0' )
    print('1/4:     ', t[int((j+1)/4)].astimezone(tz), '\tAz:', 
          round(az.degrees[int((j+1)/4)]), '\u00b0', ' Alt:', 
          round(alt.degrees[int((j+1)/4)], 1), '\u00b0' )
    print('Midpoint:', t[int((j+1)/2)].astimezone(tz), '\tAz:', 
          round(az.degrees[int((j+1)/2)]), '\u00b0', ' Alt:', 
          round(alt.degrees[int((j+1)/2)], 1), '\u00b0' )
    print('3/4:     ', t[int(3*(j+1)/4)].astimezone(tz), '\tAz:', 
          round(az.degrees[int(3*(j+1)/4)]), '\u00b0', ' Alt:', 
          round(alt.degrees[int(3*(j+1)/4)], 1), '\u00b0' )
    print('Sets:    ', t[j].astimezone(tz), '\t\tAz:', round(az.degrees[j]), 
          '\u00b0', ' Alt:', round(alt.degrees[j], 1), '\u00b0' )
    
    time = []
    for k in range(i, j+1):
        time.append(t[k].astimezone(tz).strftime('%H:%M:%S'));

    fig1, ax1 = plt.subplots()
    color = 'tab:red'
    ax1 = plt.gca()
    ax1.set_ylim([0, 90])
    ax1.set_xlabel('time')
    #ax1.set_ylabel('alt', color=color)
    ax1.plot(time, alt.degrees, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    # set maximum 5 time elements on the x axis
    xtick = np.linspace(0, len(t), 7).astype(int)
    # remove the first element from xticks
    xtick = xtick[1:-1:1]
    plt.title("Altitude")
    plt.xticks(xtick)

    fig2, ax2 = plt.subplots()
    color = 'tab:blue'
    ax2 = plt.gca()
    ax2.set_ylim([0, 360])
    #ax2.set_ylabel('az', color=color)
    ax2.plot(time, az.degrees, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    plt.title("Azimuth")
    plt.xticks(xtick)

def main():
    args = parse_args()
    with open(args.tle_file) as f:
        lines = f.readlines()
    if len(lines) != 3:
        raise RuntimeError('TLE file must have 3 lines')

    if(args.utc):
        tz = timezone('GMT')
    else: 
        tz = timezone('Canada/Eastern')

    time0 = datetime.datetime.fromtimestamp(float(args.start_timestamp), datetime.UTC)
    time1 = datetime.datetime.fromtimestamp(float(args.start_timestamp), datetime.UTC) + datetime.timedelta(0, int(args.length_pass))
    ts = load.timescale()
    t0 = ts.utc(time0.year, time0.month, time0.day, time0.hour, time0.minute, time0.second)
    t1 = ts.utc(time1.year, time1.month, time1.day, time1.hour, time1.minute, time1.second)
    t = ts.linspace(t0, t1, int(args.length_pass))
    satellite = EarthSatellite(lines[1], lines[2], 'satellite', ts)
    groundstation = wgs84.latlon(args.lat, args.lon, args.alt)
    orbit = (satellite - groundstation).at(t)
    alt, az, distance = orbit.altaz()

    plot_sky([0, len(t) -1], t, tz, az, alt)
    plt.show()


if __name__ == '__main__':
    main()
