function H = scalebar(xbase, ybase, barsize, pxlsize)
%function H = scalebar(xbase, ybase, barsize, pxlsize)
%function to plot a scalebar on the current image
%xbase, ybase: pixel location of the middle of the scalebar
%barsize: size of desired scalebar, in micron
%pxlsize: size of pixels in the image, in mm
bar_2 = barsize./pxlsize./1000./2; %half-width of scalebar, in pixels

hold on
H = plot([xbase-bar_2 xbase+bar_2], ybase+[0 0], '-w', 'LineWidth', 2);
hold off