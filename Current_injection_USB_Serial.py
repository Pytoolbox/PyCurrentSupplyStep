

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 11:35:34 2022

@author: Rahill Ismael 
"""
# Used to test AgNP sintering via current 


ser = serial.Serial('COM9', 9600)  # open serial port
print(ser.name)         # check which port was really used
ser.write(("V1 0.01 \r \n").encode())   # write a string
ser.write(("I1 0.001 \r \n").encode())   # write a string
ser.write(("OP1 1 \r \n").encode())   # write a string
time.sleep(0.01)
ser.write(("V1 1 \r \n").encode())   # write a string
ser.write(("V1 30 \r \n").encode())   # write a string




import ctypes
import threading
import time
import matplotlib.pyplot as plt
import serial.tools
import serial
def terminate_thread(thread):
    """Terminates a python thread from another thread.

    :param thread: a threading.Thread instance
    """
    if not thread.isAlive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


buff = -3
currr_div = 62
max_current_mA = 2000
time_s = []
curr_s = []
when_stop = []
when_start = []
steps = 4
time_ms_total = 4000
interval = 50
stop_interval = 200
when_interval = (time_ms_total-(stop_interval*steps))/steps
total_measure_t = (when_interval*steps)
current_res = (max_current_mA/total_measure_t)*interval

for stepz in range(1, steps+1, 1):
    when_start.append((when_interval*stepz)+(stop_interval*(stepz+buff)))
    when_stop.append((when_interval*stepz)+stop_interval*stepz)
print(when_start)
print(when_stop)
print(current_res)
print(when_interval)
count = 0
for i in range(0, time_ms_total+interval, interval):
    if i in range(int(when_start[0]), int(when_stop[0]), interval):

        time_s.append(i)
        curr_s.append(current_res*(int(when_start[0])/currr_div))
    elif i in range(int(when_start[1]), int(when_stop[1]), interval):
        time_s.append(i)
        curr_s.append(current_res*(int(when_start[1])/currr_div))
    elif i in range(int(when_start[2]), int(when_stop[2]), interval):
        time_s.append(i)
        curr_s.append(current_res*(int(when_start[2])/currr_div))
    elif i in range(int(when_start[3]), int(when_stop[3]), interval):
        time_s.append(i)
        curr_s.append(current_res*(int(when_start[3])/currr_div))
    else:
        time_s.append(i)
        curr_s.append(current_res*(i/currr_div))
print(curr_s)
print(time_s)
plt.plot(time_s, curr_s)
plt.show()


def timer(*args):
    print(str(args[0])+" It's "+str(time.ctime()))
    try:
        print(curr_s[(int(args[0]))])
        ser.write(("I1 "+str(curr_s[(int(args[0]))]/1000)+"\r \n").encode())
        ser.flush()
        next = int(args[0])+1
        threading.Timer(0.05, timer, [str(next)]).start()
    except:
        ser.write(("V1 0.01 \r \n").encode())   # write a string
        ser.write(("I1 0.001 \r \n").encode())   # write a string
        ser.write(("OP1 0 \r \n").encode())   # write a string
        ser.close()
        SystemExit()


timer("0")

# close port
