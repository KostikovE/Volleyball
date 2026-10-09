from fastapi import FastAPI

app = FastAPI(title="Volley Analytics")


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/videos")
def list_videos():
    return []


@app.get("/videos/{video_id}/rallies")
def get_rallies(video_id: int):
    return []