# Stage_UC

Stage réalisé a l'université de Canterbury, au sein du Wireless Center. Mon travail consistais en l'étude d'un module radar IWR6843ISK.

Le programme "vitesse_1courbe" permet de mesurer pendant 4 seconde les mouvement devant le radar et affiche les differents points avec leur vitesse. Ceci est utilisé afin de mesurer la trajectoire et la vitesse d'un objet en chute situé a environ 2m devant le radar.

Pour utiliser le programme: 
    1 - Flasher la carte avec le fichier .bin de "out of box demo"
    2 - Lancer le mmwave demo visualiser https://dev.ti.com/gallery/view/mmwave/mmWave_Demo_Visualizer/ver/3.6.0/
    3 - Choisir les paramètres voulu, puis cliquer sur "send config to mmwave device"
    4 - Deconnecter le radar en cliquant sur la deuxième icone en bas a gauche de l'écran, situé sur la bande noire. Il doit afficher "hardware not connected"
    5 - Aller sur pycharm et lancer le progamme, après avoir vérifié que les ports COM sont les bon (gestionnaire de periphérique pour vérifier)