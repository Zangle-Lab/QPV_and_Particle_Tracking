%loads Step1Set_C_.mat file open in workspace before running and
%MTCompiledSet___C_org_.xlsx in same folder

%reads Manual Tracking (MT), rescales it from ImageJ coordinates to matlab coordinates
%outputs an image with both PTV and PIV tracks overlayed
load('Data/Step1SetSevenC1.mat')

close; %no plots open when run

%arrays to get scaled manual tracking data
MTX = [];
MTY = [];

%arrays to put PIV (XS, YS) data into
collectXS = [];
collectYS = [];

for a = 1:numOrg
    %reading excel file and getting the X and Y columns
    specificName = append('Data/', fileName(a));

    optsX = detectImportOptions(specificName);
    optsY = detectImportOptions(specificName);

    optsX.SelectedVariableNames = [3];
    optsY.SelectedVariableNames = [4];

    %get raw X and Y values without scaling (so at mercy of imageJ size)
    clearvars MTRawX
    clearvars MTRawY

    %collect MT data
    MTRawX = readmatrix(specificName,optsX);
    MTRawY = readmatrix(specificName,optsY);

    %rescale MT, first remove left hand border
    clearvars d

    for d = 1:stopFrame(a)
        MTX(a,d) = (MTRawX(d) - subX)  * realSize / scaleX ;
        MTY(a,d) = (MTRawY(d) - subY)  * realSize / scaleY;
    end;

    %get starting particle location for XS, YS from MT particle in question
    particleIX = round(MTX(a,1));
    particleIY = round(MTY(a,1));

    clearvars b;
    %get XS and YS into two arrays for particlar particle
    for b = 1:stopFrame(a)
        collectXS(a, b)= XS(particleIY,particleIX,b);
        collectYS(a, b)= YS(particleIY,particleIX,b);
    end;


end;

%BEGINNING OF PLOTTING SECTION

%gives black as MTX, white as PIX
imagesc(Abkg_stored2(:,:,1))
hold on;
grid off;

%colors for lines
colorM = ['k', 'k', 'k'];
colorC = ['w', 'w', 'w'];

%arrays to hold legend
Mname = strings;
Cname = strings;

%plot all organelles
for c  = 1:numOrg
    Mname(c) = "Manual Tracking Organelle " + string(c);
    Cname(c) = "PIV Tracking Organelle " + string(c);
    plot(MTX(c,1:stopFrame(c)), MTY(c,1:stopFrame(c)), colorM(c));
    hold on;
    plot(collectXS(c,1:stopFrame(c)), collectYS(c,1:stopFrame(c)), colorC(c));
    hold on;
end;

%plot settings

%cropping locations
xlow = 1;
xup = 512;
ylow = 1;
yup = 512;

%legend bar location
xbarLoc = xup - 15;
ybarLoc = yup - 10;
barsize = 1; %micron
pxlsize = 0.21 /1000; %mm

axis([xlow xup ylow yup]);
scalebar(xbarLoc, ybarLoc, barsize, pxlsize)

xlabel('x');
ylabel('y');

%legend to easily see all organelle data together
lgd = legend("PTV","PIV");
lgd.Color = '#B2BEB5';
hold off;
axis image
