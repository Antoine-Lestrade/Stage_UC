### AFFICHAGE AVEC PLUSIEUR COURBES

import serial
import time
import matplotlib.pyplot as plt
from math import*

from parser_mmw_demo import checkMagicPattern, parser_one_mmw_demo_output_packet

# Temps initial
start_time = time.time()

# Paramètres de communication UART
port = "COM7"  # Port COM à utiliser (veuillez vérifier le port approprié sur votre système)
baud_rate = 921600  # Vitesse en bauds (ajustez en fonction des paramètres de votre périphérique UART)
max_number_of_objects = 20
tab_objet = [[] for _ in range(max_number_of_objects)]  # Vous pouvez remplacer max_number_of_objects par le nombre maximal d'objets que vous pourriez détecter à un instant donné.
t = 0
distance = 0
# Initialisation de la communication UART
ser = serial.Serial(port, baud_rate)

# Lecture et regroupement des données UART
data = b""
while time.time() - start_time < 5:
    if ser.in_waiting > 0:
        data += ser.read(ser.in_waiting)  # Lecture des octets bruts depuis le port UART et ajout à la variable data
        while b"\x02\x01\x04\x03\x06\x05\x08\x07" in data:
            start_index = data.index(b"\x02\x01\x04\x03\x06\x05\x08\x07")
            if b"\x02\x01\x04\x03\x06\x05\x08\x07" in data[start_index + 1:]:
                end_index = data.index(b"\x02\x01\x04\x03\x06\x05\x08\x07", start_index + 1)
                frame = data[start_index:end_index]
                X, Y, Z, V, M = parser_one_mmw_demo_output_packet(frame, len(frame))

                for j in range(len(X)):
                    # Vérifier si la liste tab_objet[j] est assez grande pour contenir l'instant t
                    while len(tab_objet[j]) <= t:
                        tab_objet[j].append([])  # Ajouter des sous-listes vides jusqu'à ce que l'instant t soit atteint.

                        # Création de la liste C pour chaque objet à l'instant t
                    C = [X[j], Y[j], Z[j]]
                    # Ajouter la liste C à l'emplacement tab_objet[j][t]
                    tab_objet[j][t].append(C)
                    print("TAB OBJET EST:\n")
                    print(tab_objet)

                t = t + 1
                data = data[end_index:]  # Mise à jour de la variable data en supprimant la trame traitée
            else:
                break

print("le numero t = %d \n" % t)
print("le nombre d'objet est = %d \n" % (len(tab_objet)))


def distance(x, y, z):
    return ((x ** 2) + (y ** 2) + (z ** 2)) ** 0.5

def afficher_courbe_coordonnees(tab_data):
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    plt.figure()
    for j in range(len(tab_data)):
        # Extraction des coordonnées x, y et z de toutes les instants
        x_values = [coord[0] if coord[0] else 0 for coord_instant in tab_data[j] for coord in coord_instant]
        y_values = [coord[1] if coord[1] else 0 for coord_instant in tab_data[j] for coord in coord_instant]
        z_values = [coord[2] if coord[2] else 0 for coord_instant in tab_data[j] for coord in coord_instant]

        # Calcul des distances pour chaque instant
        distances = [distance(x, y, z) for x, y, z in zip(x_values, y_values, z_values)]

        # Création du graphique
        plt.axhline(0, color='gray', linestyle='--')  # Configuration du graphique pour avoir le zéro au centre
        plt.axvline(0, color='gray', linestyle='--')

        color = colors[j % len(colors)]  # Choix d'une couleur

        # Filtrer les points dont la distance est entre 1m et 1.5m
        filtered_x_values = [x if 1 <= d <= 1.7 else None for x, d in zip(x_values, distances)]
        filtered_z_values = [z if 1 <= d <= 1.7 else None for z, d in zip(z_values, distances)]
        # filtered_x_values = [x if 0.2 <= d <= 10 else None for x, d in zip(x_values, distances)]
        # filtered_z_values = [z if 0.2 <= d <= 10 else None for z, d in zip(z_values, distances)]

        # Vérifier si distances est vide avant d'essayer d'accéder à distances[-1]    + distance_label
        distance_label = f' - Distance: {distances[-1]:.2f} m' if distances else ''

        # Affichage de la courbe (ligne)
        plt.plot(filtered_x_values, filtered_z_values, color=color, label=f'Objet {j + 1}')

        # Affichage des points de chaque courbe
        plt.scatter(filtered_x_values, filtered_z_values, color=color, s=5)  # s définit la taille des points

        # Ajout des étiquettes d'axes
        plt.xlabel('X')
        plt.ylabel('Z')

    # Ajout de la légende pour les différentes courbes
    plt.legend()

    # Affichage du graphique
    plt.show()
afficher_courbe_coordonnees(tab_objet)
