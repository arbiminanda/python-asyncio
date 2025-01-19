import asyncio

async def periodic():
    while True:
        print('periodic')
        await asyncio.sleep(1)

async def manage_task():
    while True:
        print("Starting task...")
        task = asyncio.create_task(periodic())
        await asyncio.sleep(5)  # Let the task run for 5 seconds
        print("Stopping task...")
        task.cancel()  # Stop the current task
        try:
            await task  # Allow the task to handle cancellation
        except asyncio.CancelledError:
            print("Task canceled.")
        print("Restarting task after a short pause...")
        await asyncio.sleep(1)  # Optional pause before restarting

# Run the manager
asyncio.run(manage_task())
