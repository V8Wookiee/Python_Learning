# Uptime Info
        test = subprocess.check_output(['uptime', '-p'])
        print "test = '" + test + "'\n"

        match = re.search(r'up (.*)', test)
        var = match.group(1)

        match = re.search(r'^(.{0,16})', var)
        var = match.group(1)

        LINE1 = "UPTIME:"
        LINE2 = str(test)
        lcd_string(LINE1, LCD_LINE_1)
        lcd_string(LINE2, LCD_LINE_2)

        time.sleep(4)
