import asyncio
import websockets

cmdCon = 'USB CONNECTED'
cmdDis = 'USB DISCONNECTED'
cmdUnplug = 'unplug'
uriServer = "ws://localhost:8765"

async def main():
    async with websockets.connect(uriServer) as websocket:
        while True:
            try:
                await websocket.send(cmdCon)
                income = await websocket.recv()
                if income == cmdUnplug:
                    await websocket.send(cmdDis)
                    exit()
            except websockets.ConnectionClosed:
                print(f"Connection closed")
                break

asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_forever()