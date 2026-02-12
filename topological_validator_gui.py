import requests
# ... (imports stay same, adding requests)

# ... (Nexus, etc stay same)

class TelemetryTransmissionThread(threading.Thread):
    def __init__(self, validator, cam):
        super().__init__()
        self.validator = validator
        self.cam = cam
        self.daemon = True
        self.running = True
        self.server_url = "http://127.0.0.1:8000"

    def run(self):
        while self.running:
            res = self.validator.get_results()
            frame = self.cam.read()
            
            if frame is not None:
                try:
                    # 1. Enviar Estado
                    state_data = {
                        "user": res.get("user"),
                        "resonance": float(cns_inst.focus_score), # Proxy de ressonancia
                        "entropy": float(res.get("entropy", 0.0)),
                        "focus_score": float(cns_inst.focus_score),
                        "liveness": float(res.get("liveness", 0.0)),
                        "spectral_salt": f"0x{res.get('spectral_salt', 0):08X}",
                        "wallet": res.get("wallet", "LOCKED")
                    }
                    requests.post(f"{self.server_url}/update_state", json=state_data, timeout=0.1)
                    
                    # 2. Enviar Frame (Downsampled para performance)
                    small_frame = cv2.resize(frame, (320, 240))
                    _, buffer = cv2.imencode('.jpg', small_frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
                    requests.post(f"{self.server_url}/update_frame", data=buffer.tobytes(), timeout=0.1)
                except Exception:
                    pass
            
            time.sleep(0.06) # ~15 FPS para o dashboard é o ideal

def run_validation_gui():
    cam = CameraStream(0).start()
    validator = AsyncValidator().start()
    
    # Iniciar Ponte de Telemetria
    telemetry_bridge = TelemetryTransmissionThread(validator, cam)
    telemetry_bridge.start()
    
    sonic.architectural_alert("SINGULARITY", "Vocal Spectral Kernel Estabilizado. Transmissão iniciada.")
    
    mode = 's' 
    fullscreen = False
    prev_time = time.time()
    fps = 60.0
    
    while True:
        frame = cam.read(wait=True) 
        if frame is None: continue
        
        curr_time = time.time()
        dt = curr_time - prev_time
        prev_time = curr_time
        fps = 0.9 * fps + 0.1 * (1.0 / dt) if dt > 0 else fps
        
        display_frame = frame.copy()
        h_f, w_f, _ = frame.shape

        validator.submit_frame(frame)
        res = validator.get_results()
        
        # --- VOCAL-SONIC SYNC ---
        vocal.evolve_vocal_identity(cns_inst.focus_score)
        if int(time.time() * 10) % 8 == 0: 
            threading.Thread(target=sonic.generative_melody, args=(cns_inst.focus_score, 0.4)).start()

        # Overlays fluidas (Simplificadas para Minimalismo)
        for (x, y, w, h) in res["faces"]:
            color = (0, 255, 0) if res["user"] else (0, 0, 255)
            cv2.rectangle(display_frame, (x, y), (x+w, y+h), color, 1)
            cv2.putText(display_frame, f"{res['user'] or 'SCANNING'}", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

        # Barra Superior HUD (Minimalista)
        cv2.rectangle(display_frame, (0, 0), (w_f, 30), (5, 5, 5), -1)
        cv2.putText(display_frame, f"OMNI-VISION v3.1 | {res['user'] or 'READY'}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        cv2.imshow('OMNI-VISION v3.1', display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break
        elif key == ord('f'):
            fullscreen = not fullscreen
            cv2.setWindowProperty('OMNI-VISION v3.1', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN if fullscreen else cv2.WINDOW_NORMAL)

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_validation_gui()

if __name__ == "__main__":
    run_validation_gui()
