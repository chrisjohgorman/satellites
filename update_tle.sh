#!/bin/bash -x

if [ ! -d ~/doppler ]; then
    mkdir ~/doppler
fi

wget -O ~/doppler/iss.tle -q https://celestrak.org/NORAD/elements/gp.php?CATNR=25544
wget -O ~/doppler/noaa_15.tle -q https://celestrak.org/NORAD/elements/gp.php?CATNR=25338
wget -O ~/doppler/noaa_18.tle -q https://celestrak.org/NORAD/elements/gp.php?CATNR=28654
wget -O ~/doppler/noaa_19.tle -q https://celestrak.org/NORAD/elements/gp.php?CATNR=33591
wget -O ~/doppler/meteor_m2_3.tle -q https://celestrak.org/NORAD/elements/gp.php?CATNR=57166
wget -O ~/doppler/meteor_m2_4.tle -q https://celestrak.org/NORAD/elements/gp.php?CATNR=59051
wget -O ~/doppler/ao_73.tle -q https://celestrak.org/NORAD/elements/gp.php?CATNR=39444
wget -O ~/doppler/by02_2.tle -q https://celestrak.org/NORAD/elements/gp.php?CATNR=45857
