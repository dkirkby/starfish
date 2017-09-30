Regenerate a weak wifi signal using a directional antenna.

## Directional Antenna

Build a 15-element Yagi tuned to 2.450GHz. Follow [these instructions](https://www.ab9il.net/wlan-projects/wifi6.html) for the assembly.

You only need about 3 ft of 14 awg copper, which could be just 1 ft of grounded cable if you don't mind stripping two of the conductors.

![grounded cable]
(https://raw.githubusercontent.com/dkirkby/starfish/master/img/IMG_2404.JPG)

Instead of drilling parallel holes, I used a small file to make parallel grooves in a piece of 0.75" x 1.5" x 1.5' poplar ($2),
and glued the antenna conductors in place.

![groove assembly]
(https://raw.githubusercontent.com/dkirkby/starfish/master/img/IMG_2403.JPG)

## Wifi Transceiver

Any USB dongle with an external antenna connection will work.  A dual 2.4/5 GHz device will work, but only 2.4GHz is needed
(since the antenna is tuned to 2.4GHz).  I got the [Panda Wireless PAU06](https://www.amazon.com/Panda-Wireless-PAU06-300Mbps-Adapter/dp/B00JDVRCI0)
for $15 since it is popular on RPi.

## Router

Use a RPi3 for the router. An older model w/o onboard wifi (which we won't use) would probably be ok, but is less
useful for other projects.  Should measure the CPU usage under load to see if the RPi faster clock is necessary.

Use [PiBakery](http://www.pibakery.org/) to pre-configure an SD card will full Raspian and hostname `starfish`.
