from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

clients = []

def store_data(data):
    fin = open("transfer_data.txt", 'w')
    fin.write(str(data) + ' ' + '2')
    print("Stored: " + str(data) + ' ' + '2')
    fin.close()

class SimpleChat(WebSocket):

    def handleMessage(self):
       for client in clients:
          if client != self:
             client.sendMessage(self.data)

    def handleConnected(self):
       print(self.address, 'connected')
    #    for client in clients:
    #       client.sendMessage(self.address[0] + u' - connected')
       clients.append(self)

    def handleClose(self):
       clients.remove(self)
       print(self.address, 'closed')
       for client in clients:
          client.sendMessage(self.address[0] + u' - disconnected')

server = SimpleWebSocketServer('', 8000, SimpleChat)
server.serveforever()

# import time
# from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

# # break_now = 0
# def breaknow():
#     global break_now
#     break_now = 1

# def store_data(data):
#     fin = open("transfer_data.txt", 'w')
#     fin.write(str(data) + ' ' + '2')
#     print("Stored: " + str(data) + ' ' + '2')
#     fin.close()

# def chatbot_response():
#     print("Waiting for chatbot response")
#     while True:
#         fin = open("transfer_data.txt", 'r')
#         x = fin.readline()
#         fin.close()
#         if x.split()[-1] == '1':
#             print(x)
#             return x
#         else:
#             print(x.split()[-1])
#             time.sleep(5)


# class SimpleEcho(WebSocket):
#     def handleMessage(self):
#         # echo message back to client
#         # self.sendMessage(self.data)
#         print("Revieved message..: ", self.data)
#         store_data(self.data)
#         time.sleep(5)
#         self.sendMessage(chatbot_response())
#         # breaknow()

#     def handleConnected(self):
#         print(self.address, 'connected')

#     def handleClose(self):
#         print(self.address, 'closed')

# break_now = 0
# server = SimpleWebSocketServer('', 8000, SimpleEcho)
# while True:
#     server.serveonce()
# # server.serveforever()
# print("test")

# # import asyncio
# # import websockets
# # import time

# # async def hello(websocket, path):
# #     name = await websocket.recv()
# #     print(f"< {name}")

# #     greeting = f"Hello {name}!"

# #     await websocket.send(greeting)
# #     print(f"> {greeting}")
# #     asyncio.get_event_loop().stop()
# #     # asyncio.get_event_loop().close()
    

# # async def response(websocket, path):
# #     await websocket.send("Hey fellas")
# #     # print(f"> {greeting}")
# #     asyncio.get_event_loop().stop()

# # start_server = websockets.serve(hello, "localhost", 8000)

# # asyncio.get_event_loop().run_until_complete(start_server)
# # asyncio.get_event_loop().run_forever()
# # # asyncio.get_event_loop().stop()
# # # asyncio.get_event_loop().stop()
# # time.sleep(5)
# # print("Attempt 2")
# # start_server = websockets.serve(response, "localhost", 8000)
# # asyncio.get_event_loop().run_until_complete(start_server)
# # asyncio.get_event_loop().run_forever()

# # while True:
# #     websockets.serve(hello, "localhost", 8000)