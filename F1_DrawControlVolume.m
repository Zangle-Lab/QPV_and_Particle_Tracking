%plot tracks on cell images
clear

load('Data/Step1SetTwoC3.mat')
stopFrame(1) = 20; %just for ii = 27, to prevent this one from overwhelming the other tracks

scale = 0.21; %micrometers/pixel

close;
window = 15; %height and width of interegation window

%beginning of plotting section
figure(1)
imagesc(Abkg_stored2(:,:,1))
hold on;
grid on;

%colors for lines
colorM = ['k', 'k', 'k'];
colorC = ['w', 'w', 'w'];
colors = 'kbg';

%arrays to hold legend
Mname = strings;
Cname = strings;

%plot all organelles
for c  = 1:numOrg
    Mname(c) = "Manual Tracking Organelle " + string(c);
    Cname(c) = "PIV Tracking Organelle " + string(c);
    plot(MTX(c,1:stopFrame(c)), MTY(c,1:stopFrame(c)), colors(c));
    hold on;
    plot(collectXS(c,1:stopFrame(c)), collectYS(c,1:stopFrame(c)), [colors(c),'--']);
    hold on;

    xSC = collectXS(c,1) - window /2; %starting corner
    ySC = collectYS(c,1) - window /2;
    xEC = collectXS(c,stopFrame(c)) - window /2; %ending corner
    yEC = collectYS(c,stopFrame(c)) - window /2;
    rectangle('Position', [xSC ySC, window, window], 'EdgeColor', '#FF3333'); %x, y is bottom left corner of rectangle
    hold on;
    rectangle('Position', [xEC yEC, window, window]);
    hold on;
    disp(yEC - ySC);
end

axis image
scalebar(100,100,10,scale/1000);
text(100,90, '10 um')

%legend to easily see all organelle data together
lgd = legend("PTV", "PIV");

lgd.Color = '#B2BEB5';
hold off;


%%
%plot particle displacement:
colors = 'kbg';
figure(2)
for c = 1:numOrg
    MTD = ((MTX(c,1:stopFrame(c))-MTX(c,1)).^2 + (MTY(c,1:stopFrame(c))-MTY(c,1)).^2)*scale.^2;
    PTD = ((collectXS(c,1:stopFrame(c))-collectXS(c,1)).^2 + (collectYS(c,1:stopFrame(c))-collectYS(c,1)).^2)*scale.^2;

    plot(Time(1:stopFrame(c)),MTD, [colors(c),'o'])
    hold on
    plot(Time(1:stopFrame(c)),PTD, [colors(c),'*'])

end
hold off
ylabel('displacement (um)')
xlabel('time (min)')
legend('PTV','QPV',Location='NorthWest')

%%
%plot particle subimages
c = 1; %which particle to look at (1:3)
frames = [1, round(stopFrame(c)/2), stopFrame(c)]; %define the three frames to plot

%beginning of plotting section
figure(3)
for sub = 1:3 %display 3 subplots
    subplot(1, 3, sub)
    framenum = frames(sub);
    imagesc(Abkg_stored2(:,:,framenum))
    axis image
    hold on;

    xSC = MTX(c,framenum) - window /2; %starting corner
    ySC = MTY(c,framenum) - window /2;
    xEC = MTX(c,framenum) + window /2; %ending corner
    yEC = MTY(c,framenum) + window /2;
    axis([xSC xEC ySC yEC])
    axis square

    scalebar(xSC+5,ySC+5,1,scale/1000);
    text(xSC+5,ySC+3, '1 um')
end