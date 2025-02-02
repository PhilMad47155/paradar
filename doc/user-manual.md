# paradar user manual

Last update: February 2021. See https://github.com/blinken/paradar/tree/master/doc/user-manual.md for the
latest version.

| Serial number |             |
| ------------- | ------------|

BLINKENLIGHT Ltd, Lytchett House, 13 Freeland Park, Wareham Road, Poole, BH16 6FA<br/>
info@paradar.co.uk

## Overview

Thanks for purchasing paradar! paradar is open-source hardware and software,
and your purchase funds further development.

paradar is a tiny, handheld, self-contained ADS-B indicator for paramotor,
paraglider, drone and general aviation pilots. It helps increase your
situational awareness by indicating aircraft in the sky around you, if they are
transmitting ADS-B.

**paradar does not replace your responsibility to look for, see and avoid other
aircraft. This device will not save your life. It is intended only to provide
additional situational awareness of some traffic around you when flying VFR. It
is not designed for and must not be used for IFR flight, and you must not rely
on it when flying in any conditions.**

paradar receives ADS-B radio transmissions from other aircraft, which contain
location information. It also contains a GPS receiver and a compass, and
calculates the bearing from your position to the other aircraft, which is then
indicated on a ring of bright LEDs. Because paradar relies on other aircraft
transmitting their position, it will pick up many aircraft but not all: some
older airframes are still not equipped with modern ADS-B transponders. This
proportion is decreasing, however, as ADS-B is mandated by regulators around
the world.

paradar is open source hardware and software. If you have an idea for a
feature or improvement, or encounter a bug, please report it at https://github.com/blinken/paradar/issues
(see the bug reports section below for more information).

For general queries, including bulk order discounts, you're welcome to contact
me at info@paradar.co.uk.

Happy flying!

*-Patrick*

<div style="page-break-after: always;"></div>

## Safety information
To prevent possible electrical shock, fire, personal injury, or damage to the
product, read this safety information carefully before attempting to install or
use the product. In addition, follow all generally accepted safety practices
and procedures for working with or near electricity.

### Symbols and terminology

The following safety descriptions and symbols are found thoughout this guide:

* A **WARNING** identifies conditions or practices that could result in injury
  or death.
* A **CAUTION** identifies conditions or practices that could result in damage
  to the product or equipment to which it is connected.

| Symbol | Description |
| :----: | ----------- |
| ![Electric shock](https://raw.githubusercontent.com/blinken/paradar/master/doc/symbol-shock.png) | Possibility of electric shock. Risk of injury or death. |
| ![Caution](https://raw.githubusercontent.com/blinken/paradar/master/doc/symbol-caution.png) | Caution. Risk of damage to the product or attached equipment. |
| ![WEEE](https://raw.githubusercontent.com/blinken/paradar/master/doc/WEEE.png) | Do not dispose of this product as unsorted muncipal waste. |

### General safety information

> ![Electric shock](https://raw.githubusercontent.com/blinken/paradar/master/doc/symbol-shock.png)
> 
> **WARNING** To prevent injury or death, use
> the product only as instructed and use only the accessories that have been
> supplied or recommended. Protection provided by the product may be impaired if
> used in a manner not specified by the manufacturer.
> 
> **WARNING** To prevent injury or death, do not use in wet or damp conditions,
> or near explosive gas or vapour.
> 
> **WARNING** paradar contains a rechargeable lithium-polymer battery. Do not use
> the device outside of the recommended operating conditions. Do not burn or
> crush, or otherwise damage or modify the outer case. Do not attempt to directly
> charge the battery; only use the USB-C port integrated into paradar.

### Operating environment

|   | Storage | Operating (including charging) |
| - | ------- | --------- |
| Temperature | 0°C to +55°C | 5°C to +50°C |
| Humidity | 5% to 95% RH (non-condensing) | 5% to 80% RH (non-condensing) |
| Magnetic field | - | -400 to 400 µT |

Keep paradar away from strong magnets and magnetic fields while in use. Keep
paradar well away from fuels (including fuel vapour), oils and solvents.

> ![Caution](https://raw.githubusercontent.com/blinken/paradar/master/doc/symbol-caution.png)
> 
> **CAUTION** To prevent damage, always use and store paradar in appropriate
> environments.

<div style="page-break-after: always;"></div>

### Care and cleaning

paradar contains user-servicable configuration switches on the top circuit
board, which can be accessed by removing the top cover using the four top
screws. Do not attempt to disassemble the device further; repair, servicing and
calibration require specialised test equipment.

To clean, ensure the top cover is firmly attached, and wipe only the outside of
the case with a damp, clean, soft cloth using a solution of mild soap or
detergent and water. Do not attempt to clean the circuit board or other
internal components.

Keep paradar well away from fuels (including fuel vapour), oils and solvents.

> ![Electric shock](https://raw.githubusercontent.com/blinken/paradar/master/doc/symbol-shock.png)
> 
> **WARNING** To prevent injury or death, do not touch any electronic or internal
> component except the user configuration switches as instructed in this manual.
> 
> **WARNING** To prevent injury or death, do not use the product if it appears to
> be damaged in any way, and stop using immediately if you are concerned by any
> abnormal operations.
> 
> **WARNING** When cleaning paradar, use a soft cloth and a solution of mild soap
> or detergent in water. To prevent electric shock, do not allow water to enter
> the casing as this will compromise the electronics or insulation inside.

<div style="page-break-after: always;"></div>

## Getting started

paradar is pretty easy to use!

1. Ensure the antenna is attached. The longer antenna is more sensitive, but also more bulky.
1. Turn paradar on using the power switch on the side. A small green LED in the
   center of the unit will light up.
1. Wait 30-40 seconds for the software to initialise.
1. The main display will start and show a spinning white dot. This indicates
   paradar is searching for a GPS signal. Make sure the top case is pointing
   upwards and it has an unobstructed view of the sky, and keep it in one place
   until it locates the GPS signal (30-120 seconds).
1. When paradar locks on to the GPS signal, the display will briefly change to
   a solid white ring.

You're up and running! paradar can show several things on the display via
coloured lights, all of which will move together as the device is rotated:

* White light: indicates compass north. Can be enabled/disabled (see below).
* Green light: guide-me-home indicator, showing that home is greater than 15
  meters away. Indicates the direction to the location the device was turned
  on. Can be enabled/disabled (see below).
* Teal light: guide-me-home indicator, showing that home is less than 15 meters
  away. When home is <15m away, the bearing is always shown as due south. Can
  be enabled/disabled (see below).
* Blue light: indicates an aircraft - far away (between 15km and 30km distant)
* Purple/red light: indicates an aircraft - nearby (less than 15km distant). The
  colour fades slowly from blue to red as the aircraft comes closer - a bright
  red light indicates that the aircraft is very close.
* Light orange light: altitude indicator in flight mode. See more on this below.

Note that aircraft distance indication (the colour of an aircraft indicator
light, from blue -> red) only considers the horizontal distance. That is, an
aircraft directly overhead but 30,000ft higher than paradar will be displayed
bright red.

The distance from which you can receive other aircraft depends on the antenna
and clearance from nearby obstacles (buildings, trees, terrain). Outdoors,
clear of obstructions, with a good line of sight in all directions, the
included 2dBi (10cm) antenna will receive large aircraft 20-30km away. A 5dBi
antenna (20cm) or a larger magnetic-mounted whip placed in a high location (eg,
a vehicle roof) will receive more distant aircraft.

paradar uses a female SMA antenna connector (the antenna must have a male SMA
connector). If you break the antenna, contact info@paradar.co.uk and we'll send
you a new one, if you cover postage.

> ![Caution](https://raw.githubusercontent.com/blinken/paradar/master/doc/symbol-caution.png)
> 
> **CAUTION** If attaching an antenna not supplied by the manufacturer, ensure it
> is tuned to 1090MHz (and optionally 978MHz in the USA). It must have 50 ohm impedance and a
> male SMA connector. Turn off paradar and disconnect the antenna if you receive
> reports of interference with other equipment.

To avoid display clutter, paradar will not display aircraft further than 30km
away, even if it can hear them. If connected to SkyDemon or another
GDL90-compatible app (see below), it will send all aircraft it can hear to the
app.

## What is ADS-B?

ADS-B (Automatic Dependent Surveillance Broadcast) is a system where aircraft
transmit their position, altitude, speed and heading (and plenty of other
information) every few seconds on a specific radio frequency. Transmit power
varies from 20W up to 500W, which means the transmissions can be heard by a
radio receiver a _very_ long way away.

The radio frequency used is 1090Mhz (most countries) or 978MHz ("UAT", largely
US-only).

There are a number of alternative standards, such as FLARM (which is popular
amongst ultralight aircraft in Europe) and the Open Glider Network (largely
UK/Europe). ADS-B however is rapidly becoming the global standard for fixed-wing
aircraft - which are the kind of aircraft paramotor and drone pilots want to
avoid at all costs!

References and further information:

* https://en.wikipedia.org/wiki/Automatic_dependent_surveillance_%E2%80%93_broadcast
* https://www.caa.co.uk/General-aviation/Aircraft-ownership-and-maintenance/Electronic-Conspicuity-devices/
* https://www.faa.gov/nextgen/programs/adsb/

### Can other aircraft see transmissions from paradar?

paradar is a receive-only device; it does not transmit. It's intended to give
you an indication of some of the traffic around you - to help you decide
whether to take off, and to help you identify other aircraft when in the air.

However, if you're flying near a location where fixed-wing aircraft operate,
it's a _really good idea_ to carry an ADS-B transmitter so you are visible to
other pilots and any air traffic control. A great option is the [uAvionix
SkyEcho 2](https://uavionix.com/products/skyecho/). This has been tested and
will work well alongside paradar.

Drone pilots should consider equipping with
a [uAvionix ping1090](https://uavionix.com/products/ping1090/), if possible.

<div style="page-break-after: always;"></div>

## Battery life, care and feeding

Paradar has a 2,000mAh internal battery. Battery life is approximately 2.5
hours (with display set to medium brightness and wifi turned off). The low
battery indicator (a small, red light in the center of the device) will come on
when you have approximately 30 minutes remaining.

Charge the battery by carefully connecting a USB-C cable to the port on the
side.

* An orange LED in the center of the device indicates the battery is
  charging
* A green LED indicates charging is complete.
* A red LED indicates low battery.
* If two lights (orange, green) are illuminated when the power is switched off,
  or you see three lights (green/orange/green) with the power switched on, the battery is
  too hot to charge. Disconnect the charger, turn paradar off and allow it
  to cool down.

paradar can be switched on or off while the battery is charging, though it will
charge slightly faster when switched off.

You can also run paradar continuously connected to an external USB battery pack
or 5V power source.  It can be run continuously off a USB-C power supply for
use on the ground or as part of a flight deck. **A good setup is a 10,000mAh
USB battery pack stored in a pocket of your flight deck, and permanently
attached to paradar via a short cable.  This can extend the run time by 5-10x,
depending on battery pack size.** Contact us if you need recommendations.

The case is made of PET plastic, which is resistant to most solvents and
somewhat resistant to fuels. paradar is not waterproof. Wipe the case clean
using a damp rag.

> ![Caution](https://raw.githubusercontent.com/blinken/paradar/master/doc/symbol-caution.png)
> 
> **CAUTION** For reliable operation and to prevent damage, follow the
> requirements below.
> 
> * paradar consumes 5W (1A) in operation, and up to 12W (2.5A) when charging. For
>   best results **use a good quality USB power supply rated to at least 3A, and a
>   good quality USB-C cable.** Weaker power supplies (eg, a laptop USB port) will
>   work, though the battery may still discharge if paradar is running and
>   charging at the same time (you'll still get a longer run time than battery alone).
> * Keep the device as level as possible to ensure the compass reading is accurate.
> * The compass used by paradar has a very high dynamic range, and will work well
>   in difficult magnetic environments. However, it is still susceptible to
>   interference. Keep paradar a few centimeters away from metal of any sort, and
>   well away from strong magnetic fields such as electric motors.
> * Don't leave paradar in hot environments or very strong sunlight (where it can
>   heat up). It will slow down processing and disable battery charging if the
>   external temperature exceeds approximately 50 degrees Celcius. Prolonged
>   exposure to higher temperatures (eg, the dashboard of a car on a hot day) may
>   damage the battery.

<div style="page-break-after: always;"></div>

## Features and configuration

paradar has six configurable feature switches just under the main lid.

To access them, remove the four screws on the top surface using a 2.5mm hex bit
or allen key, and carefully remove the lid. Be cautious not to yank on the main
circuit board just underneath as the lid comes off.

Orient the device so the USB-C connector is at the top-right. The six
configuration switches are very small and located on the center-right of the
main board. Each switch has a number printed below.

To turn a switch on, move it to the upper position (towards the ON marking). To
turn it off, move it down.

> ![Electric shock](https://raw.githubusercontent.com/blinken/paradar/master/doc/symbol-shock.png)
> 
> **WARNING** To prevent injury or death, do not touch (with fingers or tools)
> any electronic component except those described below. Ensure the power switch
> is turned off and the device is unplugged. Note that this reduces risk but does
> not de-energise the device, as it contains a battery.
> 
> **WARNING** Some parts of the device get very hot in normal operation. Be cautious.

> ![Caution](https://raw.githubusercontent.com/blinken/paradar/master/doc/symbol-caution.png)
> 
> **CAUTION** Ensure you work in a clean environment, to avoid damage to
> paradar's SD card or internal electronics.
> 
> **CAUTION** The main LEDs may be damaged if you touch them with your finger or
> a sharp tool.

### Switch function overview

| Switch # | Function | On | Off |
|----------|----------|----|-----|
| 1 | LED brightness control | High brightness | Medium brightness |
| 2 | Wifi control | Wifi hotspot enabled | Wifi hotspot disabled (saves power) |
| 3 | Guide-me-home (green/teal indicator) | Feature enabled | Feature disabled |
| 4 | Compass north (white indicator) | North shown | North not shown |
| 5 | Flight mode | Aircraft are only shown if within 3000ft of the current altitude, or less than 15km away | All aircraft closer than 30km are shown |
| 6 | Dual-mode 978Mhz operation | Device switches between 1090Mhz and 978Mhz reception periodically (for use in the USA) | Device listens continuously on 1090MHz (all other regions) |

It's fine to run paradar with the cover off for testing. You can change the
switch positions with the unit running, and they will have immediate effect. **Be
careful not to touch any electronic component, and be wary as some parts of the
board get very hot in normal operation.**

Don't run paradar with the cover off outdoors.

### LED brightness

The main display uses extremely bright LEDs, designed to be easily readable in
full sun. For use in shaded environments, or indoors, set the display to medium
brightness by setting switch #1 to OFF. This will save significant battery
power, particularly when there are a lot of aircraft nearby.

### Wifi and GDL90 (SkyDemon) support

paradar has an optional built-in wifi hotspot that allows you to provide
high-quality GPS and traffic information to a Garmin GDL90-compatible app on
your portable device or laptop. This lets you:

 * Record your flight using a better quality GPS than that available in your phone
 * See air traffic nearby displayed on a map
 * See air traffic further than 30km away (paradar will not display very
   distant aircraft, to avoid cluttering the display).

This feature has been tested with SkyDemon, but many apps support the Garmin
GDL90 protocol - ForeFlight, FlyQ, Naviator, WingX Pro, Droid EFB and more.

To enable the wifi hotspot, set switch #2 to ON. The wifi consumes the device's battery
faster. Turn it off when you're not planning on using it.

    SSID: paradar
    Password: radarapp

1. Connect your phone, tablet or laptop to the "paradar" hotspot using the
password above ("pparadar" backwards).
    * Internet access will not be available.
1. Open SkyDemon, and tap the Settings icon (the cog at the top-left of the display)
1. Select third-party devices, and tick the box next to "GDL90 compatible device".
1. Return to the main screen.
1. When you are ready, tap Go Flying at the top right of the display.
1. Select "Use GDL90 Compatible Device" when prompted.
1. SkyDemon will briefly show "Waiting for Device", which should disappear once
   it begins receiving data from paradar.

Altitude will be displayed under the "ALT" icon, and the current location will
be updated from paradar's GPS. Other aircraft will be visible as small, moving
icons against the map.

**paradar's wifi hotspot is very simple. Two paradars near each other will
interfere and good results are not guaranteed.**

### Guide-me-home

This feature allows you to record your takeoff point, and paradar will calculate
the bearing back home from your current location and display it with a green
light.

The saved home location is only held while paradar is running - it is deleted
when paradar is turned off (or the configuration switch is turned off). The
home location is recorded when paradar starts, or when the configuration switch
is turned on (if it is turned on when paradar is running).

When you are within 15 meters of the recorded home location (eg, before
takeoff) the bearing will always be shown as due south (180 degrees). This is
to avoid the display changing continuously due to GPS position error.

paradar will indicate you are close to home with a teal (blue-green) light when
you are within 15 meters.

When you are more than 15 meters from the recorded home location, paradar will
indicate the direction to home from the current position with a bright green
light.

To enable this feature, set switch #3 to ON.

### Compass north indicator

paradar can indicate compass north as a bright white LED. This is useful to
give you confidence that the compass is working without interference.

To indicate north, set switch #4 to ON.

### Flight mode

Flight mode is intended for use when flying, and has two features.

1. When activated, paradar will only show aircraft in a bubble of +/- 3000ft
   from the current altitude, and less than 15km distant. All other aircraft
   are hidden (but still sent via the WiFi link, if enabled). This is useful to
   avoid displaying large jets cruising at 35,000ft when you are flying low.

1. When paradar is turned on, the initial altitude is stored (this is reset
   when you turn it off again). Relative to the turn-on altitude, paradar will
   display an altimeter scale on the display between 20ft and 1000ft above the
   turn-on altitude. This is shown in light orange, as a "background" to other
   indicators (ie. North, Guide-me-home, and traffic all show on top of the
   altimeter).

   Note that long periods of flying at just below 1000ft will rapidly drain the
   battery, as all LEDs will be lit.

**The altimeter is based on barometric pressure using the IACO standard pressure
altitude model (on v1.5 hardware, white PCB) or GPS altitude (v1.4 hardware,
green PCB). It will be affected by changes in barometric pressure due to
weather conditions, or by interference with the GPS signal.**

**Do not rely on the altimeter function. It indicates pressure altitude, NOT
height-above-ground.**

To activate flight mode, set switch #5 to ON.

### Dual-band 978MHz+1090MHz operation

If you're operating in a region where 978Mhz (or "UAT") transmissions are used,
it is necessary to receive on both 978MHz and 1090Mhz to see all aircraft. This
usually means you're flying in the USA.

paradar can receive on 978Mhz in addition to 1090Mhz, but it only has one radio
receiver. It achieves dual-band operation by switching between 978MHz and
1090Mhz reception approximately every 10-20 seconds. Aircraft retransmit their
location very frequently, so this provides good coverage of both bands at the
expense of slightly delayed updates.

To enable dual-mode operation, set switch #6 to ON. This should be turned off
outside of the US.

Caveat - the antenna supplied with paradar is tuned to 1090Mhz. It will still
receive strong signals on 978Mhz, but reception will be weaker. However, even
in the US 1090MHz is the predominant frequency in use for air-to-air position
transmission.

<div style="page-break-after: always;"></div>

## Software updates

> ![Electric shock](https://raw.githubusercontent.com/blinken/paradar/master/doc/symbol-shock.png)
> 
> **WARNING** To prevent injury or death, do not touch (with fingers or tools)
> any electronic component except those described below. Ensure the power switch
> is turned off and the device is unplugged. Note that this reduces risk but does
> not de-energise the device, as it contains a battery.
> 
> **WARNING** Some parts of the device get very hot in normal operation. Be cautious.

> ![Caution](https://raw.githubusercontent.com/blinken/paradar/master/doc/symbol-caution.png)
> 
> **CAUTION** Ensure you work in a clean environment, to avoid damage to
> paradar's SD card or internal electronics.

To perform a software update, you'll need to remove the microSD card that holds
paradar's software. This is a bit of a delicate process - set yourself up on a
table with plenty of light.

1. Remove the four screws on the top surface using a 2.5mm hex bit or allen
   key, and carefully remove the lid. Be cautious not to yank on the main
   circuit board just under the lid.
1. Carefully loosen the nut that holds on the antenna connector. Be careful not
   to damage the antenna connector thread.
1. The SD card lives under the main circuit board on the left side - directly
   across from the USB-C connector.
1. Gripping the GPS antenna, cautiously lift the main circuit board by no more
   than 2-3cm (watch out for the tiny wires underneath).
1. Carefully remove the microSD card from the holder.

When a software update is released, it will come with instructions on what to
do next.

To re-install:

1. Insert the microSD card, contacts facing down, back where it came from -
   make sure it's fully seated in the silver card holder. It's normal that it
   sticks out slightly, and it's a friction fit only (there's no "click", it
   just slides in).
1. Make sure the main circuit board is gently seated in the center of the
   bottom case. The top of the circuit board should be level with the top of
   the case walls, and there should be an even gap around all sides.

   Sometimes, a connector under the top of the display blocks re-installation.
   Gently poke it with a small allen key or similar, so the main circuit board
   sits flat.
1. Re-attach the lid, being cautious that the tabs on the bottom of the lid fit
   in the gap between the main PCB and the side of the bottom case.
1. Reinstall all four lid screws and gently tighten. They do not need to be
   very tight. Retighten the antenna connector nut.

## Bug reports, feature requests and support

paradar is open hardware and open source software. This means that you can view
all the source code and hardware design files online, at https://github.com/blinken/paradar.
You can also contribute to development by raising a pull request.

Feature requests and bug reports are welcome. Please open an issue at
https://github.com/blinken/paradar/issues. For bug reports, please include as
much information as you possibly can about what you were doing.

For general queries (including bulk order discounts), you can contact Patrick
directly at patrick@paradar.co.uk.

<div style="page-break-after: always;"></div>

## Disclaimer and license

<img height="75px" style="margin: 5px;" src="https://raw.githubusercontent.com/blinken/paradar/master/doc/CE.png"> <img height="75px" style="margin: 5px;" src="https://raw.githubusercontent.com/blinken/paradar/master/doc/WEEE.png">

![Electric shock](https://raw.githubusercontent.com/blinken/paradar/master/doc/symbol-shock.png)

**paradar does not replace your responsibility to look for, see and avoid
other aircraft.** This device will not save your life, and you must ensure
you have appropriate flight-rated equipment to operate your aircraft.
paradar is intended only to provide additional situational awareness of
some traffic around you when flying VFR. It is not designed for and must
not be used for IFR flight, and you must not rely on it when flying in any
conditions.

paradar takes the place of a phone or tablet and app when flying, and aims
to provide useful information to a pilot. **The information provided by
paradar is not guaranteed to be correct and may fail without warning.
paradar is not suitable and must not be used to operate or control an
aircraft, and must not be relied upon for safety or the safe operation of
an aircraft.  It is not suitable and must not be used for the navigation of
an aircraft.**

**The pilot is responsible for the safe conduct of any flight, for ensuring
they have appropriate flight rated equipment alongside paradar and for
obeying all applicable laws.**

Copyright (C) 2021 Patrick Coleman

paradar is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

paradar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

