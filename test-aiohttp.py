import asyncio
import aiohttp
import json


async def sse_worker(endpoint):
    """
    Coroutine to handle the SSE connection.
    """
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                print("Connecting to SSE endpoint...")
                async with session.get(endpoint) as response:
                    if response.status == 200:
                        print("Connected to SSE")
                        async for data in response.content:
                            data = data.decode('utf-8').strip()
                            print("Received SSE data:", data)
                            try:
                                json_start_idx = data.find("{")
                                if json_start_idx != -1:
                                    json_str = data[json_start_idx:]
                                    data_json = json.loads(json_str)
                                    print("Parsed SSE JSON:", data_json)
                            except json.JSONDecodeError as e:
                                print("Error decoding JSON data:", e)
                    else:
                        print(f"Failed to connect: {response.status}")
        except aiohttp.ClientError as e:
            print(f"Connection error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            print("Retrying connection in 1 second...")
            await asyncio.sleep(1)  # Retry after 1 second


async def manage_task(endpoint):
    """
    Manages the lifecycle of the SSE worker task.
    """
    task = None
    try:
        while True:
            print("Starting SSE worker...")
            task = asyncio.create_task(sse_worker(endpoint))
            await asyncio.sleep(120)  # Run the task for 5 seconds
            print("Stopping SSE worker...")
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                print("SSE worker has been stopped.")
            print("Restarting in 1 second...")
            await asyncio.sleep(1)  # Wait before restarting
    except KeyboardInterrupt:
        print("Exiting...")
        if task:
            task.cancel()
            await task


if __name__ == "__main__":
    # Replace with your actual SSE endpoint URL
    SSE_ENDPOINT = "https://api.smartfarm.id/condition/getsetpoint/1?device_key=b20115e315475412c61ae695f518d791d0a9c92cc71425bcff62ce6132c4ab4879886736a742337bbacfb67727208b3d10e1f779ce8dff"  # Replace with your SSE endpoint
    asyncio.run(manage_task(SSE_ENDPOINT))
