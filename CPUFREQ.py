 # CPU Frequency
        cpu_freq = get_cpu_freq()
        freq = int(cpu_freq)
        LINE1 = "CPU Freq="
        LINE2 = str(freq) + "Mhz"
        lcd_string(LINE1, LCD_LINE_1)
        lcd_string(LINE2, LCD_LINE_2)
        time.sleep(4)
