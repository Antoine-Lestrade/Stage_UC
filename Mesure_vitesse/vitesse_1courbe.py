###### AFFICHAGE AVEC 1 COURBE
import serial
import time
import matplotlib.pyplot as plt

from parser_mmw_demo import parser_one_mmw_demo_output_packet

# Temps initial
start_time = time.time()
# Liste pour stocker les temps à chaque boucle
timestamps = []

# Paramètres de communication UART
port = "COM7"  # Port COM à utiliser (veuillez vérifier le port approprié sur votre système)
baud_rate = 921600  # Vitesse en bauds (ajustez en fonction des paramètres de votre périphérique UART)
max_number_of_objects = 15
t = 0
# Initialisation de la communication UART
ser = serial.Serial(port, baud_rate)
longueur_totale = 0
X_list = []
Y_list = []
Z_list = []

# Lecture et regroupement des données UART
data = b""
while time.time() - start_time < 4:
    if ser.in_waiting > 0:
        data += ser.read(ser.in_waiting)  # Lecture des octets bruts depuis le port UART et ajout à la variable data
        while b"\x02\x01\x04\x03\x06\x05\x08\x07" in data:
            start_index = data.index(b"\x02\x01\x04\x03\x06\x05\x08\x07")
            if b"\x02\x01\x04\x03\x06\x05\x08\x07" in data[start_index + 1:]:
                end_index = data.index(b"\x02\x01\x04\x03\x06\x05\x08\x07", start_index + 1)
                frame = data[start_index:end_index]
                X, Y, Z, V, M = parser_one_mmw_demo_output_packet(frame, len(frame))
                X_list += X
                Y_list += Y
                Z_list += Z
                current_time = time.time()
                timestamps.append(current_time)
                t = t + 1
                data = data[end_index:]  # Mise à jour de la variable data en supprimant la trame traitée
            else:
                break

print("le numero t = %d \n" % t)
print("les x sont :\n")
print(X_list)
print("les y sont :\n")
print(Y_list)


def distance_to_radar(x, y, z):
    radar_position = (0, 0, 0)  # Coordonnées du radar (ici, supposées être à l'origine)
    distances = []

    for i in range(len(x)):
        # Calcul de la distance entre le point (x[i], y[i], z[i]) et le radar
        distance = ((x[i] - radar_position[0]) ** 2 + (y[i] - radar_position[1]) ** 2 + (
                    z[i] - radar_position[2]) ** 2) ** 0.5
        distances.append(distance)

    return distances


def afficher_points_dans_intervalles(x, y, z):
    distances = distance_to_radar(x, y, z)
    filtered_x = []
    filtered_z = []

    for i in range(len(distances)):
        if 1 <= distances[i] <= 1.7:
            if -0.17<= x[i] <= -0.06:
                filtered_x.append(x[i])
                filtered_z.append(z[i])

    # Affichage du graphique
    plt.figure()
    plt.scatter(filtered_x, filtered_z, color='b', label='Points entre 0.8m et 1.5m')
    plt.xlabel('X')
    plt.ylabel('Z')
    plt.axhline(0, color='gray', linestyle='--')
    plt.axvline(0, color='gray', linestyle='--')
    plt.legend()
    plt.show()


afficher_points_dans_intervalles(X_list, Y_list, Z_list)
