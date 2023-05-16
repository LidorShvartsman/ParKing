import socket
import threading
import requests
import database

api_key = 'AIzaSyBkULWM5GxKKQtFLz1tlfnZXHDW_8hLVg0'
radius = 200
keyword = 'parking'



class ChatServer:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.IP, self.PORT))
        self.server.listen()
        print("SERVER is waiting for clients")
        self.list_of_obj_clients = []
        self.list_of_addr_clients = []

    def connection(self, conn_obj, conn_addr):

                data_receive = conn_obj.recv(1024).decode()
                print(data_receive)
                # print(f"Client {conn_addr}: {data_receive}")
                letters_to_remove = "(')"
                for letter in letters_to_remove:
                    data_receive = str(data_receive).replace(letter, "")
                print(data_receive)
                coordinates_list= data_receive.split(", ")
                latitude= coordinates_list[0]
                longitude=coordinates_list[1]
                url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={coordinates_list[0]},{coordinates_list[1]}&radius={radius}&keyword={keyword}&key={api_key}"
                response = requests.get(url)

                # Get the JSON data from the API response
                data = response.json()

                # Send the number of parking spots found to the client
                x = 0
                for spot in data['results']:
                    x = x + 1
                conn_obj.send(f"{x}".encode())

                # Send the coordinates of the parking spots found to the client
                for spot in data['results']:
                    lat = spot['geometry']['location']['lat']
                    lng = spot['geometry']['location']['lng']
                    database.add_new_parking_spot(lat,lng)
                    conn_obj.send(f"{lat},{lng}".encode())
                    conn_obj.recv(1024).decode()




    def get_clients(self):
        while True:
            try:
                conn_obj, conn_addr = self.server.accept()
                self.list_of_addr_clients.append(conn_addr)
                self.list_of_obj_clients.append(conn_obj)
                print(f"New client connected: {conn_addr}")
                conn_thread = threading.Thread(target=self.connection, args=(conn_obj, conn_addr))
                conn_thread.start()
            except Exception as e:
                print(f"Error: {e}")
                break

server1 = ChatServer("192.168.1.123", 6666)
server1.get_clients()


