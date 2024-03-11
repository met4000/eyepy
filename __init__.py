"""Wrapper around `eye` module, adding types and input checking."""

# TODO LCD
from eye import LCDPrintf, LCDSetPrintf, LCDClear, LCDSetPos, LCDGetPos, LCDSetColor, LCDSetFont, LCDSetMode # ? no LCDFontSize
from eye import HELVETICA, TIMES, COURIER, NORMAL, BOLD
from eye import RED, GREEN, BLUE, WHITE, GRAY, BLACK, ORANGE, SILVER, LIGHTGRAY, NAVY, CYAN, TEAL, MAGENTA, PURPLE, MAROON, YELLOW, OLIVE

# TODO keys
from eye import KEYGet, KEYRead, KEYWait, KEYGetXY, KEYReadXY
from eye import KEY1, KEY2, KEY3, KEY4, ANYKEY, NOKEY

# TODO camera
from eye import CAMInit, CAMRelease, CAMGet, CAMGetGray
from eye import QQVGA, QVGA, VGA, CAM1MP, CAMHD, CAM5MP, CUSTOM
from eye import CAMWIDTH, CAMHEIGHT, CAMPIXELS, CAMSIZE
from eye import QQVGA_SIZE, QVGA_SIZE, VGA_SIZE, CAM1MP_SIZE, CAMHD_SIZE, CAM5MP_SIZE
from eye import QQVGA_PIXELS, QVGA_PIXELS, VGA_PIXELS, CAM1MP_PIXELS, CAMHD_PIXELS, CAM5MP_PIXELS
from eye import QQVGA_X, QVGA_X, VGA_X, CAM1MP_X, CAMHD_X, CAM5MP_X
from eye import QQVGA_Y, QVGA_Y, VGA_Y, CAM1MP_Y, CAMHD_Y, CAM5MP_Y

# TODO image processing

# TODO system functions

# TODO timer

# TODO usb/serial

# TODO audio

from psd import *
from lidar import *
from motors import *
from v_omega import *

# TODO digital and analog i/o

# TODO IR remote control

# TODO radio communication

# TODO sim only functions
