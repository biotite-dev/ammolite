convert images/demo_1.png -gravity center -crop +67+27 +repage images/demo_crop_1.png
convert images/demo_2.png -gravity center -crop +67+27 +repage images/demo_crop_2.png
convert images/demo_3.png -gravity center -crop +67+27 +repage images/demo_crop_3.png
convert images/demo_4.png -gravity center -crop +67+27 +repage images/demo_crop_4.png
convert images/demo_5.png -gravity center -crop +67+27 +repage images/demo_crop_5.png
convert images/demo_6.png -gravity center -crop +67+27 +repage images/demo_crop_6.png
convert images/demo_7.png -gravity center -crop +67+27 +repage images/demo_crop_7.png
convert images/demo_8.png -gravity center -crop +67+27 +repage images/demo_crop_8.png
convert images/demo_9.png -gravity center -crop +67+27 +repage images/demo_crop_9.png
convert -delay 100 -loop 0 -dispose 2 images/demo_crop_*.png demo.gif