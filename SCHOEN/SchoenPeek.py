import numpy as np
import torch
from PIL import ImageGrab, Image
import cv2
import time
import io
import base64
from aiohttp import web
import threading
import os

NODE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTURE_FILE = os.path.join(NODE_DIR, "schoen_peek_capture.png")

class SchoenPeek:
    def __init__(self):
        self.region = None
        self.preview_image = None

    @classmethod
    def INPUT_TYPES(cls):
        return { "required": { "mode": (["Manual", "Live"], {"default": "Manual"}), "refresh_interval": ("FLOAT", {"default": 1.0, "min": 0.2, "max": 10.0, "step": 0.1}), } }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Captured Image",)
    FUNCTION = "trigger"
    CATEGORY = "SCHOEN"  # GEÄNDERT

    def select_region(self):
        try:
            screenshot = ImageGrab.grab()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.namedWindow("Select Region", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Select Region", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty("Select Region", cv2.WND_PROP_TOPMOST, 1)
            r = cv2.selectROI("Select Region", frame, fromCenter=False, showCrosshair=True)
            cv2.destroyAllWindows()
            if r and all(r):
                x, y, w, h = r
                self.region = (int(x), int(y), int(x + w), int(y + h))
                print(f"[SCHOEN Peek] Region set: {self.region}") # GEÄNDERT
                self.capture_image()
                return {"result": f"Region set: {self.region}"}
            else:
                return {"result": "Cancelled"}
        except Exception as e:
            print(f"[SCHOEN Peek] Error during region selection: {e}") # GEÄNDERT
            return {"result": str(e)}

    def capture_image(self):
        if not self.region:
            return {"result": "Region not defined"}
        try:
            img = ImageGrab.grab(bbox=self.region)
            img.save(CAPTURE_FILE, "PNG")
            print(f"[SCHOEN Peek] Screenshot saved.") # GEÄNDERT
            self.preview_image = img
            return {"result": "ok", "preview": self._encode_preview(img)}
        except Exception as e:
            print(f"[SCHOEN Peek] Capture error: {e}") # GEÄNDERT
            return {"result": str(e)}

    def _encode_preview(self, img):
        buf = io.BytesIO()
        thumb = img.copy()
        thumb.thumbnail((180, 120))
        thumb.save(buf, format="JPEG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")

    def trigger(self, mode, refresh_interval):
        if os.path.exists(CAPTURE_FILE):
            try:
                img = Image.open(CAPTURE_FILE)
                img_rgb = img.convert("RGB")
                arr = np.array(img_rgb).astype(np.float32) / 255.0
                tensor = torch.from_numpy(arr).unsqueeze(0)
                return (tensor,)
            except Exception as e:
                print(f"[SCHOEN Peek] Error loading capture file: {e}") # GEÄNDERT
        return (torch.zeros((1, 64, 64, 3)),)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float(time.time())

schoen_peek_instance = SchoenPeek()

async def handle_select_region(request):
    loop = request.app.loop
    result = await loop.run_in_executor(None, schoen_peek_instance.select_region)
    return web.json_response(result)

async def handle_capture_image(request):
    result = schoen_peek_instance.capture_image()
    return web.json_response(result)

try:
    from server import PromptServer
    @PromptServer.instance.routes.post("/custom/SchoenPeek/select_region")
    async def _select_region_route(request): return await handle_select_region(request)

    @PromptServer.instance.routes.post("/custom/SchoenPeek/capture_image")
    async def _capture_image_route(request): return await handle_capture_image(request)
    
    print("[SCHOEN Peek] Webserver routes registered.") # GEÄNDERT
except Exception as e:
    print(f"[SCHOEN Peek] Error registering routes: {e}") # GEÄNDERT

NODE_CLASS_MAPPINGS = {"SchoenPeek": SchoenPeek}
NODE_DISPLAY_NAME_MAPPINGS = {"SchoenPeek": "SCHOEN Peek"} # GEÄNDERT
WEB_DIRECTORY = "./web"