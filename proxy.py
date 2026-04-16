import asyncio
import websockets
import os

DB_HOST = 'dpg-d7g9tb0sfn5c73a1354g-a.oregon-postgres.render.com'
DB_PORT = 5432

async def handle(websocket):
    try:
        reader, writer = await asyncio.open_connection(DB_HOST, DB_PORT)
        
        async def ws_to_db():
            try:
                async for message in websocket:
                    writer.write(message if isinstance(message, bytes) else message.encode())
                    await writer.drain()
            except:
                pass
            finally:
                writer.close()

        async def db_to_ws():
            try:
                while True:
                    data = await reader.read(4096)
                    if not data:
                        break
                    await websocket.send(data)
            except:
                pass

        await asyncio.gather(ws_to_db(), db_to_ws())
    except Exception as e:
        print(f"Error: {e}")

async def main():
    port = int(os.environ.get('PORT', 3000))
    print(f'WebSocket proxy starting on port {port}')
    async with websockets.serve(handle, '0.0.0.0', port):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
