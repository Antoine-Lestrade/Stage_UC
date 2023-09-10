# Stage_UC

Internship at the University of Canterbury, in the Wireless Center. My work consisted in studying an IWR6843ISK radar module.

The "speed_1curve" program measures movement in front of the radar for 4 seconds and displays the various points with their speed. This is used to measure the trajectory and speed of a falling object located about 2m in front of the radar.

To use the program: 
    1 - Flash the board with the .bin file of "out of box demo".
    2 - Run mmwave demo visualizer https://dev.ti.com/gallery/view/mmwave/mmWave_Demo_Visualizer/ver/3.6.0/
    3 - Select the desired parameters, then click on "send config to mmwave device".
    4 - Disconnect the radar by clicking on the second icon at the bottom left of the screen, located on the black band. It should display "hardware not connected".
    5 - Go to pycharm and run the program, after checking that the COM ports are correct (peripheral manager to verify).


Warning: The parser_one_mmw_demo_output_packet function of the parser_mmw_demo file was modified. The return was changed in order to only get the useful information.