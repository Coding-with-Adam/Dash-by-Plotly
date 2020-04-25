# Solution to update your web app every 5 seconds, and stop updating after 3 intervals
# changes made to line 8,9

dcc.Interval(
            id='my_interval',
            disabled=False,     #if True the counter will no longer update
            n_intervals=0,      #number of times the interval has passed
            interval=5*1000,    #increment the counter n_intervals every 5 seconds
            max_intervals=3,    #number of times the interval will be fired.
                                #if -1, then the interval has no limit (the default)
                                #and if 0 then the interval stops running.
),
