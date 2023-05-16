from flask import Flask, request, render_template,  redirect,url_for
from geopy.geocoders import Nominatim
from gmplot import gmplot
import socket



SERVER_IP = '192.168.1.123'
SERVER_PORT = 6666

app = Flask(__name__)

geolocator = Nominatim(user_agent="my_app")


@app.route('/', methods=['GET', 'POST'])
def parking():
    coordinates = ""

    if request.method == 'POST':
        # Get the value entered in the entry field
        street_name = request.form['entry']
        street_number = request.form['entry2']

        try:
            if street_number == "":
                location = geolocator.geocode(f"{street_name}, IL")
            else:
                location = geolocator.geocode(f"{street_name},{street_number}, IL")

            coordinates = (location.latitude, location.longitude)

        except AttributeError:
            print("The place doesn't exist.")
            return redirect(url_for('parking'))
        # Create a client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((SERVER_IP, SERVER_PORT))

        # Send the coordinates to the server
        client_socket.sendall(str(coordinates).encode())
        print(f"Coordinates sent to server: {coordinates}")

        num_parking_spots = int(client_socket.recv(1024).decode())

        parking_spots = []
        for i in range(num_parking_spots):
            spot_coords = client_socket.recv(1024).decode()
            client_socket.send("ok".encode())
            print(spot_coords)
            lat, lon = map(float, spot_coords.split(','))
            parking_spots.append((lat, lon))


        print(parking_spots)
        client_socket.close()

        # Create a Google Maps object centered at the user's location
        gmap = gmplot.GoogleMapPlotter(coordinates[0], coordinates[1], 18)

        # Add a marker for the user's location
        gmap.marker(coordinates[0], coordinates[1], color='red')

        # Add markers for each parking spot
        for spot in parking_spots:
            gmap.marker(spot[0], spot[1], color='green')

        # Save the map as an HTML file
        gmap.draw("templates/map.html")

        return redirect(url_for('show_map'))
    else:
        return render_template("parking.html")



@app.route("/show_map")
def show_map():
    return render_template("map.html")


if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0", debug=True)