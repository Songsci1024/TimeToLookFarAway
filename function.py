import time
from pynput import mouse
from pynput import keyboard
from win10toast import ToastNotifier
from pycaw.pycaw import AudioUtilities
import pyaudiowpatch as pyaudio
import numpy as np
import threading
from datetime import datetime

def print_time(timestamp):
    t = datetime.fromtimestamp(timestamp)
    formatted_date = t.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date

class monitor_mouse:
    def __init__(self):
        super(monitor_mouse, self).__init__()
        self.used = False
    def on_move(self, x, y):
        self.used = True
        # print('move')
    def on_click(self, x, y, button, b):
        self.used = True
    def create_listen(self):
        listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click
        )
        return listener
    

class monitor_keyborad:
    def __init__(self):
        super(monitor_keyborad, self).__init__()
        self.used = False
    def on_press(self, key):
        self.used = True
    def create_listen(self):
        listener = keyboard.Listener(
            on_press=self.on_press
        )
        return listener
    

class monitor_audio:
    def __init__(self, interval):
        super(monitor_audio, self).__init__()
        self.used = False
        self.inteval = interval
    def task(self):
        """
        audio detection
        """
        p = pyaudio.PyAudio()
        for speakers_loopback in p.get_loopback_device_info_generator():    #for loop one or more audio devices
            stream = p.open(format=pyaudio.paInt16,
                            channels=speakers_loopback['maxInputChannels'],
                            rate=int(speakers_loopback['defaultSampleRate']),
                            input=True,
                            input_device_index = speakers_loopback['index'],
                            frames_per_buffer=1024)
            # print("开始监测是否有声音播放")
            for i in range(0, 5):  # it takes 5 seconds
                data = stream.read(1024)
                audio_data = np.frombuffer(data, dtype=np.short)
                temp = np.max(audio_data)
                time.sleep(1)
                if i >= 3 and temp >= 400:
                    # print(temp)
                    return True
            stream.stop_stream()
            stream.close()
            p.terminate()
        return False
    def threading_task(self, interval):
        while True:
            self.used = self.task() or self.used
            time.sleep(interval)
    def create_listen(self):
        listener = threading.Thread(target=self.threading_task, args=(self.inteval, ))
        return listener

stop_signal = False
start_signal = True
def stop():
    global stop_signal
    stop_signal = True
def start(worktime, cleartime, unit_checktime = 1, check_interval_seconds = 10):
    ### initialization
    WORKTIME = worktime * 60
    CLEARTIME = cleartime * 60                    # save the accumulated working hours 
    UNIT_CHECKTIME = unit_checktime * 60        # At checktime intervals, check whether the computer is in use
    CHECK_INTERVAL = check_interval_seconds     # unit is seconds, the sleep time of the check audio threading

    # file = open('./log.txt', 'a', encoding='UTF-8')
    toast = ToastNotifier() # windows notice
    last_time = time.time()

    mm = monitor_mouse()
    mouse_listener = mm.create_listen()

    mk = monitor_keyborad()
    keyboard_listener = mk.create_listen()

    ma = monitor_audio(interval=CHECK_INTERVAL)
    audio_listener = ma.create_listen()

    mouse_listener.start()
    keyboard_listener.start()
    audio_listener.start()
    no_operation_time = 0
    print(f'time_begin:{print_time(last_time)}')
    # file.write(f'{time.time()}\n')
    global start_signal, stop_signal
    while start_signal:
        
        # for i in range(UNIT_CHECKTIME):
        #     time.sleep(1)
        #     if stop_signal:
        #         start_signal = False
        #         break
                
        time.sleep(UNIT_CHECKTIME)
        nowtime = time.time()


        if mm.used == False and mk.used == False and ma.used == False:  # no work time
            no_operation_time += UNIT_CHECKTIME
            print(f'no operation time: {no_operation_time / 60},add unit_checktime')
        else:
            last_time += no_operation_time
            print(f'new time_begin:{print_time(last_time)}')
            no_operation_time = 0
        mm.used = mk.used = ma.used = False    

        if no_operation_time == CLEARTIME:       # Any longer than this save time will clear the previous working time
            last_time = time.time()
            no_operation_time = 0
        if nowtime - last_time > WORKTIME:      #  time to look far away
            last_time = time.time()
            print(f'time_end:{print_time(nowtime)}')
            # file.write(f'{nowtime}\n')
            # file.close()
            toast.show_toast(title='time to look far away', msg='让眼睛休息一下吧')
        