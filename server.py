import asyncio
import os
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from starlette.responses import FileResponse

from audiochat.agents import AudioBot
from audiochat.voice_generator import Voice_generator

# Create a FastAPI instance
app = FastAPI()

audio_bot = AudioBot()
voice_gen = Voice_generator()
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
def chat(query: str, background_tasks: BackgroundTasks):
    # msg, voice_set = audio_bot.run(query)
    msg = audio_bot.run(query)
    voice_set = audio_bot.voice_set
    unique_id = str(uuid.uuid4())
    voice_gen.set_voice_set(voice_set)
    background_tasks.add_task(voice_gen.background_voice_systhesis, msg["output"], unique_id)
    return {"msg": msg, "id": unique_id}

@app.post("/download/{filename}")
async def download_file(filename: str):
    while True:
        if os.path.exists(filename):
            file = FileResponse(filename, filename=filename)
            break
        else:
            await asyncio.sleep(1)
    return file

@app.post("/remove/{filename}")
def remove_voice(filename: str):
    os.remove(filename)


@app.post("/add_images")

@app.post("/add_urls")
def add_urls():
    return {"response": "URLs added"}

@app.post("/add_pdfs")
def add_urls():
    return {"response": "PDFs added"}

@app.post("/add_texts")
def add_urls():
    return {"response": "Texts added"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Connection Closed")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
