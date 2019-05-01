
import asyncio
import datetime
import time
import random
import websockets
from io import StringIO, BytesIO
import base64
import cv2
import numpy as np
from PIL import Image
import threading

from sklearn.externals import joblib
from src.system.interface import AnnotatorInterface

import json
from utils import string_to_image, image_to_string, preview_image

loop = 0
# cap = None
# open_websocket = None

def frameAsB64(frame):
    retval, buffer = cv2.imencode('.jpg', frame)
    encoded_image = base64.b64encode(buffer)
    return encoded_image.decode('utf-8')

async def sendFrame(cap, websocket):
    print('send frame')
    global loop

    ret, frame = cap.read()
    # if not ret:
    #     break

    frame = cv2.resize(frame, dsize=None, fx=0.5, fy=0.5)

    # preview_image(frame, 'video', 1)

    b64Image = frameAsB64(frame)

    data = { u'timestamp': time.time(), u"frame": b64Image } 

    text_data = json.dumps(data)
    await websocket.send(text_data)

    print('frame', loop)
    loop = loop + 1


server_address = '127.0.0.1'
server_port = ':5678'

async def updates():
    async with websockets.connect('ws://' + server_address + server_port) as websocket:

        print('Connected to server')
        
        # default_media = 0
        # default_media = './ressources/inputs/videos/nico_arms_side.mp4'

        default_media = './ressources/inputs/videos/okan_arms_up.min.mp4'
        cap = cv2.VideoCapture(default_media)
        
        while True:
            sleepTime = 0.2
            await asyncio.sleep(sleepTime)
            asyncio.ensure_future(sendFrame(cap, websocket))
    

def start():
    print('Streamer server websockets start')
    asyncio.get_event_loop().run_until_complete(updates())
    

if __name__ == "__main__":
    start()
