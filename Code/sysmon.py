#!/usr/bin/env python
#
# Copyright 2015 Matt Hawkins
#
# Update  : July 2016
# added CPU and disk monitoring to script
#      johnty.wang@mail.mcgill.ca
#
# additional requirement: psutil 
#
# --------------------------------------
#
# Code modified from above by
#          Scott Harvey
#       v8wookiee@gmail.com
# Added Uptime, Ram info and Wifi info
#
# --------------------------------------
from subprocess import PIPE, Popen
import smbus
import psutil
import os
import time

# Define some device parameters
I2C_ADDR = 0x27  # I2C device address
LCD_WIDTH = 16  # Maximum characters per line

# Define some device constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
# Uncomment the following two lines for a 1604 4x Line Display
# LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
# LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT = 0x08  # On
# LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100  # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Open I2C interface
# bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 and 3 Pi's use 1

def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(E_DELAY)

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = the data
    # mode = 1 for data
    #        0 for command

    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    # High bits
    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    # Low bits
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)


def lcd_toggle_enable(bits):
    # Toggle enable
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(E_DELAY)


def lcd_string(message, line):
    # Send string to display

    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

def main():
    # Main program block

    # Initialise display
    lcd_init()

    while True:

        #Network Info
        net = psutil.net_io_counters(pernic=True)
        sent = net['wlan0'].bytes_sent
        received = net['wlan0'].bytes_recv

        LINE1 = "Wifi IN =   " + str(received / 1024 / 1024) + "MB"
        LINE2 = "Wifi OUT=    " + str(sent / 1024 / 1024) + "MB"
        lcd_string(LINE1, LCD_LINE_1)
        lcd_string(LINE2, LCD_LINE_2)

        time.sleep(4)

        #CPU Info
        cpu_temp = get_cpu_temperature()
        cpu_usage = psutil.cpu_percent()

        LINE1 = "CPU TEMP=  " + str(cpu_temp) + "c"
        LINE2 = "CPU USED=   " + str(cpu_usage) + "%"
        lcd_string(LINE1, LCD_LINE_1)
        lcd_string(LINE2, LCD_LINE_2)

        time.sleep(4)

        #Disk Info
        st = os.statvfs("/")
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = total - free

        LINE1 = "DISK USED:  " + str(used / 1024 / 1024 / 1024) + "GB"
        LINE2 = "DISK FREE:  " + str(total / 1024 / 1024 / 1024) + "GB"
        lcd_string(LINE1, LCD_LINE_1)
        lcd_string(LINE2, LCD_LINE_2)

        time.sleep(4)

        # Ram Info
        usedram = psutil.virtual_memory().percent
        freeram = psutil.virtual_memory().free
        LINE1 = "MEM USED=  " + str(usedram) + "%"
        LINE2 = "MEM FREE=  " + str(freeram / 1024 / 1024) + "MB"
        lcd_string(LINE1, LCD_LINE_1)
        lcd_string(LINE2, LCD_LINE_2)

        time.sleep(4)

        #Uptime Info
        from datetime import timedelta
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds=uptime_seconds))

        LINE1 = "UPTIME:"
        LINE2 = str(uptime_string)
        lcd_string(LINE1, LCD_LINE_1)
        lcd_string(LINE2, LCD_LINE_2)

        time.sleep(4)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        LCD_BACKLIGHT = 0x00  # turn off backlight when exiting!
        lcd_byte(0x01, LCD_CMD)
