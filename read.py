"""
Blynk is a platform with iOS and Android apps to control
Arduino, Raspberry Pi and the likes over the Internet.
You can easily build graphic interfaces for all your
projects by simply dragging and dropping widgets.

  Downloads, docs, tutorials: http://www.blynk.cc
  Sketch generator:           http://examples.blynk.cc
  Blynk community:            http://community.blynk.cc
  Social networks:            http://www.fb.com/blynkapp
                              http://twitter.com/blynk_app

This example shows how to display custom data on the widget.

In your Blynk App project:
  Add a Value Display widget,
  bind it to Virtual Pin V2,
  set the read frequency to 1 second.
  Run the App (green triangle in the upper right corner).

It will automagically call v2_read_handler.
Calling virtual_write updates widget value.
"""

import BlynkLib
import time

BLYNK_AUTH = '624362b2c01847f5adedaca933b93c9b'
BLYNK_AUTH = '624362b2c01847f5adedaca933b93c9b'

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Register virtual pin handler
@blynk.on("readV2")
def v2_read_handler():
    # This widget will show some time in seconds..
    blynk.virtual_write(1,1)

while True:
    blynk.run()
    blynk.notify( "ben dep trai " )
    blynk.virtual_write( 2, 1 ) 
