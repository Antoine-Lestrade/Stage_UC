###### AFFICHAGE AVEC 1 COURBE
import serial
import time
import matplotlib.pyplot as plt

from parser_mmw_demo import parser_one_mmw_demo_output_packet

# Initial time
start_time = time.time()

# UART communication parameters
port = "COM7"  # COM port to use (please check the appropriate port on your system)
baud_rate = 921600  # Baud rate (adjust according to your UART device settings)
max_number_of_objects = 15
t = 0  #Variable for checking the number of iterations in the loop

# UART communication initialization

ser = serial.Serial(port, baud_rate)
longueur_totale = 0

# List of radar measurements
X_list = []
Y_list = []
Z_list = []
V_list = []

# Reading and grouping UART data
data = b""
while time.time() - start_time < 4:
    if ser.in_waiting > 0:
        data += ser.read(ser.in_waiting)  # Read raw bytes from the UART port and add to the data variable
        while b"\x02\x01\x04\x03\x06\x05\x08\x07" in data:
            start_index = data.index(b"\x02\x01\x04\x03\x06\x05\x08\x07")
            if b"\x02\x01\x04\x03\x06\x05\x08\x07" in data[start_index + 1:]:
                end_index = data.index(b"\x02\x01\x04\x03\x06\x05\x08\x07", start_index + 1)
                frame = data[start_index:end_index]
                X, Y, Z, V, M = parser_one_mmw_demo_output_packet(frame, len(frame))
                X_list += X
                Y_list += Y
                Z_list += Z
                V_list += V
                t = t + 1
                data = data[end_index:]  # Update the data variable by deleting the processed frame
            else:
                break

def distance_to_radar(x, y, z):
    radar_position = (0, 0, 0)  # Radar coordinates (here, assumed to be at origin)
    distances = []

    for i in range(len(x)):
        # Calculate the distance between the point (x[i], y[i], z[i]) and the radar
        distance = ((x[i] - radar_position[0]) ** 2 + (y[i] - radar_position[1]) ** 2 + (
                z[i] - radar_position[2]) ** 2) ** 0.5
        distances.append(distance)

    return distances


def afficher_points_dans_intervalles(x, y, z, V_list):
    distances = distance_to_radar(x, y, z)
    filtered_x = []
    filtered_z = []
    filtered_v = []

    for i in range(len(distances)):
        if 0.8 <= y[i] <= 2.5 and -0.5 <= x[i] <= 0.5:
            filtered_x.append(x[i])
            filtered_z.append(z[i])
            filtered_v.append(V_list[i])  # Add associated speed

    # Graph display with color scale
    plt.figure()
    plt.scatter(filtered_x, filtered_z, c=filtered_v, cmap='viridis', label='Points entre 1.6m et 2m')
    plt.xlabel('X')
    plt.ylabel('Z')
    plt.axhline(0, color='gray', linestyle='--')
    plt.axvline(0, color='gray', linestyle='--')
    plt.colorbar(label='Vitesse')
    plt.legend()
    plt.show()


afficher_points_dans_intervalles(X_list, Y_list, Z_list, V_list)
