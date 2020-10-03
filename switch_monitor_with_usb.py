#!/usr/bin/env python3
import usb.core
import usb.util

import argparse
from subprocess import run
import sys

INPUT_VCP = '0x60'

def auto_int(x):
  return int(x, 0)

def hex_int(x):
  return int(x, 16)

def xhex_int(x):
  return f'x{auto_int(x):x}'

parser = argparse.ArgumentParser(description = 'Set input VCP on monitor when USB device is present')
parser.add_argument('vendor', type = hex_int, help = 'Vendor ID of the USB device (hex)')
parser.add_argument('product', type = hex_int, help = 'Product ID of the USB device (hex)')
parser.add_argument('serial', help = 'Monitor serial number')
parser.add_argument('input', type = xhex_int, help = 'Desired monitor input')

parser.add_argument('--ddcutil', '-d', help = 'ddcutil executable', default = '/usr/bin/ddcutil')

args = parser.parse_args()

# Check if the USB device is connected
dev = usb.core.find(idVendor = args.vendor, idProduct = args.product)
if dev is None:
  print(f'USB device {args.vendor:0>4X}:{args.product:0>4X} not connected', file = sys.stderr)
  sys.exit(1)

# Retrieve the current VCP value
getvcp = run([ args.ddcutil, '-n', args.serial, '--nousb', '-t', 'getvcp', '0x60' ], capture_output = True, text = True)
if getvcp.returncode != 0:
  print(f'Failed to retrieve VCP {INPUT_VCP} for monitor with serial number {args.serial}', file = sys.stderr)
  print(args.ddcutil + ': ' + getvcp.stderr, file = sys.stderr)
  sys.exit(1)

# Set the VCP value if it is different to the current value
if getvcp.stdout.split()[3] != args.input:
  setvcp = run([ args.ddcutil, '-n', args.serial, '--nousb', 'setvcp', INPUT_VCP, args.input ], capture_output = True, text = True)
  if setvcp.returncode != 0:
    print(f'Failed to set VCP {INPUT_VCP} to {args.input} for monitor with serial number {args.serial}', file = sys.stderr)
    print(args.ddcutil + ': ' + setvcp.stderr, file = sys.stderr)
    sys.exit(1)