import numpy as np
import preheat_open as ph
import matplotlib.pyplot as plt
import TimeKeeper
TK = TimeKeeper.TimeKeeper()


upload_schedule = 1
do_plot = 1


b_id = 2245
b = ph.Building(b_id)


damper = b.qu(name="DUMMY_VENTILATION")
damper_ctrl = damper.qu(name="DUMMY_VENTILATION_CONTROL")

# loading data from a zone
start_date = TK.get_now_local_delay(-60*60*1)
end_date = TK.get_now_local()
res = "raw"


damper_ctrl.load_data(start_date, end_date, res)
data = damper_ctrl.data

if do_plot:
    plt.plot(data, label=res)
    plt.grid()
    plt.legend()
    plt.ylabel("Damper postion")
    plt.xlabel("Time")
    plt.ylim(0, 10)

schedule_start = TK.get_now_local()
schedule_end = TK.get_now_local_delay(60*60*1)

schedule = TK.create_schedule_dt(schedule_start, schedule_end, 30)

T = 30
values = [5+np.sin(2*np.pi*t/T) for t in range(len(schedule))]
values[-1] = 0

std_plan = TK.create_std_plan(schedule, values)

if upload_schedule:
    damper_ctrl.request_schedule(std_plan)

damper_schedule = damper_ctrl.get_schedule(schedule_start, schedule_end)
