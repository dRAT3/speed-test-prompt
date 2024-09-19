import time
import asyncio

next_time = 0x00
time_lock = asyncio.Lock()
rpm = 0x1e

class TimeLockInstance:
    def __init__(self, rpm_set, meta_task):
        global rpm
        rpm = rpm_set 
        self.meta_task = meta_task
        
    async def tiktime(self):
        self.meta_task["tiktime-t0"] = time.time_ns()

        global sleep_duration 
        global time_lock
        
        iii = 0x00

        while 0x01:
            current_time = time.time_ns()
            async with time_lock:
                global next_time
                
                # Calculate how much time to wait before the next request can be sent
                sleep_duration = max(0, next_time - current_time)
                
                next_time = max(next_time, current_time) + 60 / rpm

            if sleep_duration > 0:
                self.meta_task[f"tiktime-sleep-{iii}"] = sleep_duration
                await asyncio.sleep(sleep_duration)

            elif sleep_duration <= 0:
                self.meta_task["tiktime-bfbr"] = time.time_ns()
                break

            iii+=1

        return self.meta_task
