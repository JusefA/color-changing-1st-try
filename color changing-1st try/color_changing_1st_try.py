import ctypes
from ctypes import wintypes
import os
import sys
import time

class COORD(ctypes.Structure):
  _fields_ = (('X', wintypes.SHORT), ('Y', wintypes.SHORT))

class CONSOLE_SCREEN_BUFFER_INFOEX(ctypes.Structure):
  _fields_ = (
    ('cbSize', wintypes.ULONG),
    ('dwSize', COORD),
    ('dwCursorPosition', COORD),
    ('wAttributes', wintypes.WORD),
    ('srWindow', wintypes.SMALL_RECT),
    ('dwMaximumWindowSize', COORD),
    ('wPopupAttributes', wintypes.WORD),
    ('bFullscreenSupported', wintypes.BOOL),
    ('ColorTable', wintypes.DWORD * 16))
  def __init__(self, *args, **kwds):
    super(CONSOLE_SCREEN_BUFFER_INFOEX, self).__init__(*args, **kwds)
    self.cbSize = ctypes.sizeof(self)

def rgb_values_to_integer_color(red, green, blue):
  integer_color = red + (green * 256) + (blue * 256 * 256)
  return integer_color

STD_OUTPUT_HANDLE = -11
console_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
console_screen_information = CONSOLE_SCREEN_BUFFER_INFOEX()

# get the original color to later set it back
ctypes.windll.kernel32.GetConsoleScreenBufferInfoEx(console_handle, ctypes.byref(console_screen_information))
original_color = console_screen_information.ColorTable[0]

# prevent the console screen's height from shrinking
console_screen_information.srWindow.Bottom += 1

# set the new rgb color
console_screen_information.ColorTable[0] = rgb_values_to_integer_color(red=84, green=170, blue=255)
ctypes.windll.kernel32.SetConsoleScreenBufferInfoEx(console_handle, ctypes.byref(console_screen_information))

# wait 3 seconds
time.sleep(3)

# change back to the original color
console_screen_information.ColorTable[0] = original_color
ctypes.windll.kernel32.SetConsoleScreenBufferInfoEx(console_handle, ctypes.byref(console_screen_information))