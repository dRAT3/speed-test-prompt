import time

async def tiktime():
    async def acquire_time_lock_and_update():
        async with time_lock:
            # Calculate how much time to wait before the next request can be sent
            global NEXT_TIME
            current_time = time.time_ns()
            sleep_duration = max(0, NEXT_TIME - current_time)
            NEXT_TIME = max(NEXT_TIME, current_time) + RPS

    if sleep_duration > 0:
        await asyncio.sleep(sleep_duration)
        await acquire_time_lock_and_update()
