def get_cpu_freq():
    process = Popen(['vcgencmd', 'measure_clock arm'], stdout=PIPE)
    output, _error = process.communicate()

    match = re.search(r'=(\d+)', output)
    freq = match.group(1)
    # print("freq = '" + freq + "'\n")

# CPU Frequency
        cpu_freq = get_cpu_freq()
        freq = int(cpu_freq)
        LINE1 = "CPU =    " + str(freq / 1024 / 1024) + "Mhz"
        # LINE2 =
        lcd_string(LINE1, LCD_LINE_1)
        lcd_string(LINE2, LCD_LINE_2)
