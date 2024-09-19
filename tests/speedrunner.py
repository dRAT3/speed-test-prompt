async def _arun_tests(tests, runs, rpm):
    """
        TodO
    """
    print(30*"*")

    # Create a list of coroutine objects by calling each test function
    tasks = []
    meta_task ={}
    meta_task['completed'] = 'false' 
    meta_task['current_round'] = 0

    for i, test in enumerate(tests):
        meta_task['ray_id'] = uuid.uuid4() # Used for creating log stream
        # Access and call the function using globals()
        func = globals()[test](meta_task.copy(), runs)

        print(f"SUT: {test}")
        
        # Append to tasks list as an awaitable coroutine
        tasks.append((asyncio.create_task(func)))


    # Run all tasks concurrently
    results = await asyncio.gather(*tasks)
    
    for result in results:
        pass

    t1 = time.time_ns()
    
    elapsed = t1 - t0
    
    print(f"Time elapsed[All Runs]: {elapsed}")
