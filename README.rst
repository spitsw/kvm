KVM
===
Script to switch active monitor using DDC/CI control

Installation
------------
Run as a udev rule
::
  ACTION=="add", SUBSYSTEM=="usb", ENV{ID_VENDOR_ID}=="1234", ENV{ID_MODEL_ID}=="5678", RUN+="/usr/local/bin/switch_monitor_with_usb.py 0x1234 0x5678 H8B6023 0x11"
