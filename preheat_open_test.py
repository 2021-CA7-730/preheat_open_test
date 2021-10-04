import numpy as np
import preheat_open as ph
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import TimeKeeper
TK = TimeKeeper.TimeKeeper()
ph.logging.VERBOSE = False

upload_schedule = 1
do_plot = 1


b_id = 2245
b = ph.Building(b_id)


ventilation = b.qu(name="Ventilation")
DC01 = ventilation.qu(name="DC01:DAMPER_OUTSIDE_INTAKE")
DC02 = ventilation.qu(name="DC02:DAMPER_CROSS")
DC03 = ventilation.qu(name="DC03:DAMPER_LAB_INTAKE")

# loading data from a zone
start_date = TK.get_now_local_delay(-60*60*1)
end_date = TK.get_now_local()
res = "raw"


DC01.load_data(start_date, end_date, res)
DC02.load_data(start_date, end_date, res)
DC03.load_data(start_date, end_date, res)

if do_plot:
    plt.plot(pd.to_datetime(DC01.data.index),
             DC01.data.values, label=DC01.name)
    plt.plot(pd.to_datetime(DC02.data.index),
             DC02.data.values, label=DC02.name)
    plt.plot(pd.to_datetime(DC03.data.index),
             DC03.data.values, label=DC03.name)
    if res == "raw":
        formatter = mdates.DateFormatter("%H:%M")
    elif res == "minute":
        formatter = mdates.DateFormatter("%H:%M")
    else:
        formatter = mdates.DateFormatter("%Y-%m-%D")
    ax = plt.gca()
    ax.xaxis.set_major_formatter(formatter)
    ax.margins(x=0)
    plt.grid()
    plt.ylim(0, 10)
    plt.xlabel("Time")
    plt.ylabel(DC01.name)
    plt.legend()


schedule_start = TK.get_now_local()
schedule_end = TK.get_now_local_delay(60*60*1)

schedule = TK.create_schedule_dt(schedule_start, schedule_end, 30)

T = 30
values = [5+np.sin(2*np.pi*t/T) for t in range(len(schedule))]
values[-1] = 0

std_plan = TK.create_std_plan(schedule, values)

if upload_schedule:
    DC01.request_schedule(std_plan)

damper_schedule = DC01.get_schedule(schedule_start, schedule_end)
