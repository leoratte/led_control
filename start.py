import asyncio
import websockets
import json
import logging

from control import Controller


async def send_web_config(websocket):
    await websocket.send(json.dumps(web_config))


async def consumer_handler(websocket, path):
    logger.info("Client connected")
    await send_web_config(websocket)
    async for message in websocket:
        logger.info("Message received: {}".format(message))
        try:
            data = json.loads(message)
            controller.parse(data)
        except ValueError:
            logger.warning("Message could not be parsed")
        except Exception as e:
            logger.warning(e.args)


__name__ = "start"
# logging
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='app.log', filemode='a', format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Application started")

# configuration
CONFIG_PATH = "config.json"
controller = Controller(CONFIG_PATH)
web_config = controller.get_webconfig()

# websocket
start_server = websockets.serve(consumer_handler, "0.0.0.0", 6789)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
