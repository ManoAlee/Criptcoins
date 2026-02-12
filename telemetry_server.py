from fastapi import FastAPI, WebSocket, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import asyncio
import random
import time
import sys
import cv2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class HUDState(BaseModel):
    user: str = None
    resonance: float = 0.0
    entropy: float = 0.0
    focus_score: float = 0.0
    liveness: float = 0.0
    spectral_salt: str = "0x00000000"
    wallet: str = "LOCKED"

class TelemetryBridge:
    def __init__(self):
        self.start_time = time.time()
        self.active_sessions = 0
        self.current_frame = None
        self.state = {
            "biometric": {"resonance": 0.0, "entropy": 0.0, "focus_score": 0.0, "liveness": "SCANNING"},
            "vocal_sync": {"kinetic_res": 0.0, "vocal_salt": "0x00000000", "status": "INITIALIZING"},
            "financial": {"balance_sig": 50.0, "blocks": 1, "last_hash": "N/A"},
            "terminal_status": "BRIDGE_LIVE"
        }

    def update(self, hud_data: HUDState):
        self.state["biometric"] = {
            "resonance": hud_data.resonance,
            "entropy": hud_data.entropy,
            "focus_score": hud_data.focus_score,
            "liveness": f"{hud_data.liveness*100:.1f}%" if hud_data.user else "SCANNING"
        }
        self.state["vocal_sync"] = {
            "kinetic_res": hud_data.focus_score,
            "vocal_salt": hud_data.spectral_salt,
            "status": "CONVERGED" if hud_data.focus_score > 0.8 else "SYNCING"
        }
        self.state["financial"]["last_hash"] = hud_data.spectral_salt
        self.state["user"] = hud_data.user
        self.state["wallet"] = hud_data.wallet

bridge = TelemetryBridge()

@app.post("/update_state")
async def update_state(data: HUDState):
    bridge.update(data)
    return {"status": "ok"}

@app.post("/update_frame")
async def update_frame(request: Request):
    # Receber frame JPEG via bytes
    body = await request.body()
    bridge.current_frame = body
    return {"status": "ok"}

async def frame_generator():
    while True:
        if bridge.current_frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + bridge.current_frame + b'\r\n')
        await asyncio.sleep(0.04) # ~25 FPS stream

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/telemetry")
async def get_telemetry():
    return bridge.state

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    bridge.active_sessions += 1
    try:
        while True:
            await websocket.send_json(bridge.state)
            await asyncio.sleep(0.1) # 10Hz é suficiente para o dashboard
    except Exception:
        pass
    finally:
        bridge.active_sessions -= 1

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
