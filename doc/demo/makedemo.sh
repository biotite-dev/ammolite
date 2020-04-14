convert images/demo_terminal_1.png images/demo_pymol_1.png -append /tmp/demo_combined_1.png
convert images/demo_terminal_2.png images/demo_pymol_2.png -append /tmp/demo_combined_2.png
convert images/demo_terminal_3.png images/demo_pymol_3.png -append /tmp/demo_combined_3.png
convert images/demo_terminal_4.png images/demo_pymol_4.png -append /tmp/demo_combined_4.png
convert images/demo_terminal_5.png images/demo_pymol_5.png -append /tmp/demo_combined_5.png
convert images/demo_terminal_6.png images/demo_pymol_6.png -append /tmp/demo_combined_6.png
convert images/demo_terminal_7.png images/demo_pymol_7.png -append /tmp/demo_combined_7.png
convert -delay 150 -loop 0 -dispose 2 /tmp/demo_combined_*.png demo.gif
