# Hand-Gesture-Recognition

This relatively simple algorithm is basically able to discern the number of open fingers of a hand present in the input image. The first step is to separate the skin pixels from the rest of the image.

## Skin-Pixel Detection

First, the image is converted from the RGB colorspace to the YCbCr colorspace since it is less sensitive to changes in lighting conditions. The next step is to apply the thresholds in order to segment the skin pixels from the non-skin pixels.
![image](https://user-images.githubusercontent.com/73758224/146670778-5922385e-f5b6-41ea-a40b-59ca7310ae07.png)

## Noise Removal

In order to remove noise from the image, we use morphological filetring. The Opening and Closing operations are performed on the image using an elliptical structural element.

## Finding the center of the Hand 

Next, we need to find the coordinates of the center of the hand. Then from the center coordinates, the longest distance to the hand contour is found. 

## Finger Count Calculation

We draw a circle centered on the hand, with a radius which is 0.7 times the longest distance found in the previous step. This would result in a circle which intersects all the open digits and thus we can find the number of intersecting segments which would give us the number of open digits present in the hand image.

![Result](https://user-images.githubusercontent.com/73758224/146671644-38f195e6-69bf-4e33-8a28-fa3fdd1958cd.jpg)

## Further Reading

Asanterabi Malima, Erol Uzgur and Mujdat Cetin, “A Fast Algorithm for Vision-Based Hand Gesture Recognition For Robot Control,” in 2006 IEEE 14th Signal Processing and Communications Applications.
