import time

async def tiktime():
    async def acquire_time_lock_and_update():
        current_time = time.time_ns()
        
        while 0x01:
            async with TIME_LOCK:
                # Calculate how much time to wait before the next request can be sent
                global NEXT_TIME
                sleep_duration = max(0, NEXT_TIME - current_time)
                NEXT_TIME = max(NEXT_TIME, current_time) + RPS

            if sleep_duration > 0:
                await asyncio.sleep(sleep_duration)
