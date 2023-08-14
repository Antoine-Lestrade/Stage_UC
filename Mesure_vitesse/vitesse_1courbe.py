###### AFFICHAGE AVEC 1 COURBE
import serial
import time
import matplotlib.pyplot as plt

from parser_mmw_demo import parser_one_mmw_demo_output_packet

# Temps initial
start_time = time.time()

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
V_list = []

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
                V_list += V
                t = t + 1
                data = data[end_index:]  # Mise à jour de la variable data en supprimant la trame traitée
            else:
                break

def distance_to_radar(x, y, z):
    radar_position = (0, 0, 0)  # Coordonnées du radar (ici, supposées être à l'origine)
    distances = []

    for i in range(len(x)):
        # Calcul de la distance entre le point (x[i], y[i], z[i]) et le radar
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
        if 0.8 <= y[i] <= 2.5:
            filtered_x.append(x[i])
            filtered_z.append(z[i])
            filtered_v.append(V_list[i])  # Ajout de la vitesse associée

    # Affichage du graphique avec graduation de couleur
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
