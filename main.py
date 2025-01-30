from fastapi import FastAPI


app = FastAPI()


@app.get("/",)
async def test():
    user = {
        "username": "testuser",
        "password": "testpassword",
    }
    return user
