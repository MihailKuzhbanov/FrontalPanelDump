import asyncio
import websockets

cmdCon = 'USB CONNECTED'
cmdDis = 'USB DISCONNECTED'
cmdUnplug = 'unplug'
uriServer = "ws://localhost:8765"

async def main():
    async with websockets.connect(uriServer) as websocket:
        await websocket.send(cmdDis)


asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_forever()
