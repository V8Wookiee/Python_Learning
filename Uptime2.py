 ./sysmoncpufreq.py
test = 'up 3 hours
'

Traceback (most recent call last):
  File "./sysmoncpufreq.py", line 215, in <module>
    main()
  File "./sysmoncpufreq.py", line 189, in main
    uptime_string = re.sub(r'\s*,*\s*$', '', uptime_string)
UnboundLocalError: local variable 'uptime_string' referenced before assignment
