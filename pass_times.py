#!/usr/bin/env python
import argparse
import datetime
from dateutil.parser import parse

from skyfield.api import load, wgs84
from skyfield.api import EarthSatellite

def parse_args():
    parser = argparse.ArgumentParser(
        description='Generates a list of Satellite pass times')
    parser.add_argument(
        '--tle-file', required=True,
        help='Input TLE file')
    parser.add_argument(
        '--start-date', required=True,
        help='Start date in format YYYY-MM-DD')
    parser.add_argument(
        '--end-date', required=True,
        help='End date in format YYYY-MM-DD')
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


def main():
    args = parse_args()
    with open(args.tle_file) as f:
        lines = f.readlines()
    if len(lines) != 3:
        raise RuntimeError('TLE file must have 3 lines')
    print("Table of Satellite pases for", lines[0])
    print("Date (UTC)           Timestamp           Pass time in Seconds")

    start = parse(args.start_date)
    end = parse(args.end_date)

    ts = load.timescale()
    groundstation = wgs84.latlon(args.lat, args.lon, args.alt)
    t0 = ts.utc(start.year, start.month, start.day)
    t1 = ts.utc(end.year, end.month, end.day)
 
    satellite = EarthSatellite(lines[1], lines[2], 'satellite', ts)

    t, events = satellite.find_events(groundstation, t0, t1, altitude_degrees=0.0)
    for ti, event in zip(t, events):
        if event == 0:
            dt0 = ti.utc_datetime()
            #FIXME should I be adding a timedelta?
            #dt2 = ti.utc_datetime() + datetime.timedelta(0,1)
            dt2 = ti.utc_datetime()
        elif event == 2:
            dt1 = ti.utc_datetime()
            dt3 = dt1 - dt0
            print(dt2.strftime('%Y %b %d %H:%M:%S'), dt2.timestamp(), "\t",dt3.seconds)


if __name__ == '__main__':
    main()
