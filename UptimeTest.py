 # Uptime Info
        subprocess.check_output(['uptime', '-p'])

        LINE1 = "UPTIME:"
        LINE2 = str(uptime_string)
        lcd_string(LINE1, LCD_LINE_1)
        lcd_string(LINE2, LCD_LINE_2)

        time.sleep(4)
