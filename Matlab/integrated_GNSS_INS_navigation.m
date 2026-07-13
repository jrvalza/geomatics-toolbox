%TEMA        : Navegación integrada GNSS/INS  
%SALIDA      : gráficos, fichero integrated-navigation.txt y  fichero coordenadas.csv

%--------------------------------------------------------------------------------------------------------------------------------------------------------
%-------------------------------------------------------------INICIO DEL PROGRAMA------------------------------------------------------------------------
%--------------------------------------------------------------------------------------------------------------------------------------------------------

%Borrado de variables en memoria
clear;

%sistema de referencia geodésico
sysrefGeodetic = 'ETRS89';

%elipsoide de referencia
elip = 'GRS80';
ellipsoid=parelip(elip);

%velocidad angular de la tierra (rad/s)
We = 7.29211510e-5;

%body frame: [id, x1, x2, x3, alpha, beta, gamma]
bFrame = [
           0  0.0000  0.0000   0.0000  0.000000  0.000000  0.000000 %PLA
           1  0.0000  0.0000   0.0000  0.000000  0.000000  0.000000 %INS
           2  0.4000 -0.4000   0.0000  0.000000  0.000000  0.000000 %REC2
           3  0.4000  0.4000   0.0000  0.000000  0.000000  0.000000 %REC3
           4 -0.4000 -0.4000   0.0000  0.000000  0.000000  0.000000 %REC4
           5 -0.4000  0.4000   0.0000  0.000000  0.000000  0.000000 %REC5
           6  0.7000 -0.1880  -0.0050  0.000000  0.000000  0.000000 %CAM1
           7  0.7000  0.1880  -0.0050  0.000000  0.000000  0.000000 %CAM2
           8  0.6750  0.0000  -0.6520  0.000000  0.000000  0.000000 %CAM3
         ];
bFrameNames = {'PLA'; 'INS'; 'REC2'; 'REC3'; 'REC4'; 'REC5'; 'CAM1'; 'CAM2'; 'CAM3'};

%body frame approximate offsets and misalignment of devices
% [id, x1, x2, x3, alpha, beta, gamma]
bFrameOffsets = [
                  1  0.0000  0.0000  -0.0250  0.000000  0.000000  0.000000 %INS
                  6  0.1250  0.0000  -0.0450  0.000000  0.000000  0.000000 %CAM1
                  7  0.1250  0.0000  -0.0450  0.000000  0.000000  0.000000 %CAM2
                  8  0.0200  0.0000  -0.0200  0.000000 15.000000  0.000000 %CAM3
                ];
bFrameOffsetsNames = {'INS'; 'CAM1'; 'CAM2'; 'CAM3'};


%-----------------------------------------------------------
%-----------------------Datos del INS-----------------------
%-----------------------------------------------------------

%[YY, MM, DD, HH, MM, SS, accX1, accX2, accX3, angX1, angX2, angX3, roll, pitch, yaw, lat, lng, h, vN, vE, vD, rumbo, elat, elng, eh, eroll, epitch, eyaw, epoch]
datFileINS_50hz = load("INS\INS-10-10-2024-50Hz-ses6.dat");

%[YY, MM, DD, HH, MM, SS, aN, aE, aD, vN, vE, vD, rumbo, acc, vel, epoch] 
kinFileINS_50hz = load("INS\INS-10-10-2024-50Hz-ses6.kin");

%[YY, MM, DD, HH, MM, SS, lat, lng, h, ro, nu, N, def_ro, def_nu, gN, gE, gD, declinacion, epoch]
auxFileINS_50hz = load("INS\INS-10-10-2024-50Hz-ses6.aux");


%-----------------------------------------------------------
%-------------------Datos receptores GNSS-------------------
%-----------------------------------------------------------

%[YY, MM, DD, HH, MM, SS, lat, lng, h, elat, elng, eh, elapsedTime, positions/receivers(0-4), solution_quality]
geoFileRTK_01hz = load("GNSS\1hz\RTK-10-10-2024-01hz-ses6.geo");

%[YY, MM, DD, HH, MM, SS, lat, lng, h, elat, elng, eh, elapsedTime, positions/receivers(0-4), solution_quality, epoch]
geoFileRTK_50hz = load("GNSS\50hz\RTK-10-10-2024-50Hz-ses6.geo");

%[YY, MM, DD, HH, MM, SS, roll(deg), pitch(deg), yaw(deg), positions/receivers(0-4), solution_quality, epoch]
attFileRTK_50hz = load("GNSS\50hz\RTK-10-10-2024-50Hz-ses6.att");

%[YY, MM, DD, HH, MM, SS, aN, aE, aD, vN, vE, vD, rumbo, acc, vel, positions/receivers(0-4), solution_quality, epoch] 
kinFileRTK_50hz = load("GNSS\50hz\RTK-10-10-2024-50Hz-ses6.kin");


%--------------------------------------------------------------------------------------------------------------------------------------------------------
%-------------------------------------------------------------Respuestas pregunta 1------------------------------------------------------------------------
%--------------------------------------------------------------------------------------------------------------------------------------------------------

%=====================================================================================================================================
%1.A
%   Comparar los ángulos de navegación (φ,θ,ψ) contenidos en los correspondientes ficheros de GNSS e INS (para facilitar esta tarea,
%   se proporcionan adicionalmente ficheros de GNSS a 50Hz, en concreto, el que tiene extensión .att). Analizar y extraer conclusiones
%   respecto a la consistencia de los datos y su precisión.
%=====================================================================================================================================

%----Datos para el gráfico----

%horas decimales: eje X
time = datFileINS_50hz(:,4) + datFileINS_50hz(:,5)/60 + datFileINS_50hz(:,6)/3600;

%series de datos: eje Y
data = [
        datFileINS_50hz(:,13:15)';  %IMU raw data (roll, pitch, yaw)
        attFileRTK_50hz(:,7:9)';    %GNSS(RTK)-based attitude of the platform (roll, pitch, yaw)
       ];

%número de receptores GPS: eje Y
numRTKrec = attFileRTK_50hz(:,10);

%títulos de gráficos
titles = {
          'Comparison between INS-based roll and GNSS-RTK-based roll';
          'Comparison between INS-based pitch and GNSS-RTK-based pitch';
          'Comparison between INS-based yaw and GNSS-RTK-based yaw'
         };

%etiquetas eje Y
yLabels = {'Roll (deg)', 'Pitch (deg)', 'Yaw (deg)'};

%legenda de series de datos
leg = {'INS-based', 'GNSS(RTK)-based', 'Number of RTK rec'};

%número de gráficos a generar
numPlots = size(data, 1)/2;

%gráfico
comparativeGraphs(time, data, numRTKrec, numPlots, titles, yLabels, leg, true, false);


%=====================================================================================================================================
%1.B
%   Comparar las aceleraciones proporcionadas por el INS con las aceleraciones calculadas a partir de los datos GNSS, empleando para 
%   ello las ecuaciones de navegación inercial (para facilitar esta tarea, se proporcionan adicionalmente ficheros de GNSS a 50Hz,
%   en concreto el que tiene extensión.kin). Analizar y extraer conclusiones respecto a la consistencia de los datos y su precisión.
%=====================================================================================================================================

%--------------------------------------------------------------------------------------------------------------------------------------
%----------------Corrección de aceleraciones lineales medidas por el INS mediante las ecuaciones de navegación inercial----------------
%--------------------------------------------------------------------------------------------------------------------------------------

%almacenará las acleraciones corregidas y expresadas en el n-Frame
accIMU_nFrame = [];

[f,~] = size(datFileINS_50hz);
for i=1:f
    %-----------------Transformación aceleraciones INS(s-frame to n-frame(Norte geográfico))-----------------
    
    %aceleraciones (m/s2) INS en s-frame
    accINS_sFrame = datFileINS_50hz(i, 7:9);
    
    %IMU raw data (roll, pitch, yaw) (radianes)
    roll_INS  = deg2rad(datFileINS_50hz(i,13));
    pitch_INS = deg2rad(datFileINS_50hz(i,14));
    yaw_INS   = deg2rad(datFileINS_50hz(i,15));

    %matriz de rotación s-frame to n_frame (norte magnético)
    matrix_sFrame_nFrameNM = euler2rotmat(-roll_INS, -pitch_INS, -yaw_INS);
    
    %------Corrección por declinación magnética (δ)------
    %declinación magnética IGRF24 (radianes)
    declinacion = deg2rad(auxFileINS_50hz(i,18));
    matrix_nFrameNM__nFrameNG = euler2rotmat(0, 0, declinacion);
    
    %aceleraciones (m/s2) INS en n-frame norte geográfico
    accINS_nFrame = matrix_nFrameNM__nFrameNG * matrix_sFrame_nFrameNM * accINS_sFrame';%vector (3*1)
    
    %-----------------Corrección de aceleraciones lineales medidas por el INS-----------------
    %vector de gravedad normal (GRS80) (m/s2)
    gNormal = auxFileINS_50hz(i,15:17)';%vector (3*1)

    %latitud y altura elipsoidal medidas por el GNSS interno del INS
    lat = deg2rad(auxFileINS_50hz(i,7));%radianes
    h = auxFileINS_50hz(i,9);%metros

    %vector de velocidad (m/s) n-frame (derivado del GNSS interno del INS)
    vel_nFrame = kinFileINS_50hz(i,10:12)';%vector (3*1)

    %velocidad en el e-frame (dlat, dlon, dh)
    v_eFrame = vel_eFrame(lat, h, ellipsoid, vel_nFrame); %vector (3*1)
    
    %aceleraciones (m/s2) INS en n-frame corregidas
    accIMU_nFrame(i,:) = acc_nFrame(lat, We, accINS_nFrame, gNormal, vel_nFrame, v_eFrame)'; %matriz (n*3)
end

%-------------------------------------------------------------------------------------
%--------------------gráfico comparativo INS vs internal GNSS(SPP)--------------------
%-------------------------------------------------------------------------------------

%horas decimales
time = datFileINS_50hz(:,4) + datFileINS_50hz(:,5)/60 + datFileINS_50hz(:,6)/3600;

%----selección de datos útiles----
%la aceleración GNSS derivada de la velocidad GNSS sólo está disponible para las épocas cuyos códigos de época son 1 ó 2
matriz = [time, accIMU_nFrame, kinFileINS_50hz(:, [7:9, end])]; %[horas decimales, accINS, accGNSS, época]

%selección registros válidos
mask = matriz(:, end) == 1 | matriz(:, end) == 2;
matrizFiltrada = matriz(mask, :);

%-----datos para el gráfico-----

%horas decimales: eje X
time2 = matrizFiltrada(:,1);

%series de datos: eje Y
data = [
        matrizFiltrada(:,2:4)';   %IMU raw data linear acceleration nFrame corregidas(aN, aE, aD)
        matrizFiltrada(:,5:7)';   %Internal GNSS-kinematics auxiliary data (aN; aE; aD)
       ];

%títulos de gráficos
titles = {
          {'NORTH component', 'INS-based vs internal GNSS(SPP)-based acceleration'};
          {'EAST component', 'INS-based vs internal GNSS(SPP)-based acceleration'};
          {'DOWN component', 'INS-based vs internal GNSS(SPP)-based acceleration'};
         };

%etiquetas eje Y
yLabels = {'aN (m/s²)', 'aE (m/s²)', 'aD (m/s²)'};

%legenda de series de datos
leg = {'INS-based', 'GNSS(SPP)-based'};

% Número de gráficos a generar
numPlots = size(data, 1)/2;
numRTKrec = [];

%gráfico
comparativeGraphs(time2, data, numRTKrec, numPlots, titles, yLabels, leg, false, true, -5, 5);


%----------------------------------------------------------------------------
%--------------------gráfico comparativo INS vs GNSS(RTK)--------------------
%----------------------------------------------------------------------------

%----Datos para el gráfico----

%series de datos: eje Y
data = [
        accIMU_nFrame';   %IMU raw data linear acceleration nFrame corregidas(aN, aE, aD)
        kinFileRTK_50hz(:, 7:9)';   %GNSS RTK-kinematics auxiliary data (aN; aE; aD)
       ];

%títulos de gráficos
titles = {
          {'NORTH component', 'INS-based vs GNSS(RTK)-based acceleration'};
          {'EAST component', 'INS-based vs GNSS(RTK)-based acceleration'};
          {'DOWN component', 'INS-based vs GNSS(RTK)-based acceleration'};
         };

%etiquetas eje Y
yLabels = {'aN (m/s²)', 'aE (m/s²)', 'aD (m/s²)'};

%legenda de series de datos
leg = {'INS-based', 'GNSS(RTK)-based'};

% Número de gráficos a generar
numPlots = size(data, 1)/2;
numRTKrec = [];

%gráfico
comparativeGraphs(time, data, numRTKrec, numPlots, titles, yLabels, leg, false, true, -5, 5);


%--------------------------------------------------------------------------------------------------------------------------------------------------------
%-------------------------------------------------------------Respuestas pregunta 2------------------------------------------------------------------------
%--------------------------------------------------------------------------------------------------------------------------------------------------------

%================================Datos de partida================================

%----bFrame + offsets----
%elementos comunes entre bFrameNames y bFrameOffsetsNames
[~, idx_bFrame, idx_bFrameOffsets] = intersect(bFrameNames, bFrameOffsetsNames, 'stable');

%incorporando información de offsets al bFrame
bFrameUpdated = bFrame;
bFrameUpdated(idx_bFrame, 2:end) = bFrameUpdated(idx_bFrame, 2:end) + bFrameOffsets(idx_bFrameOffsets, 2:end);

%incorporando información de desalineación (pitch) de la camara 3 al b-Frame
cam = 'CAM3';
id_cam3 = find(strcmp(bFrameNames, cam));
cam3 = bFrameUpdated(id_cam3,:);
bFrameUpdated(id_cam3,2:end) = [(euler2rotmat(deg2rad(cam3(:,5)), deg2rad(cam3(:,6)), deg2rad(cam3(:,7))) * cam3(:,2:4)')', [0,0,0]];

%identificador del punto definido como origen para las transformaciones
centerPointName = 'INS';
[~, sensorName, ~] = frameOrigin(centerPointName, bFrameNames, bFrameUpdated);
id_bFrame_origin = find(strcmp(bFrameNames, sensorName));

%nombre del punto origen de calibración de la plataforma
refSensorName = 'PLA';

%identificadores de camaras
camaras = {'CAM1'; 'CAM2'; 'CAM3'};
idCamaras = [];
[nCamaras,c] = size(camaras);
for i=1:nCamaras
    idCamaras(i,1)=find(strcmp(bFrameNames, camaras(i))) - 1;
end

%==============================================================================
%============1-) Transformación de incrementos b-frame to s-frame==============
%==============================================================================

%En los datos de calibración (apha, beta, gamma) para el sensor INS son igual a 0.
%En principio esta transformación no haría falta, pero se realiza para tenerla presente.

% ==Calculo de parametros de transformación==

% 1.1-) ángulos de euler (radianes) por calibración: (s-frame to b-frame) calibración sensor INS
alpha = deg2rad(bFrameUpdated(id_bFrame_origin,5));
beta = deg2rad(bFrameUpdated(id_bFrame_origin,6));
gamma = deg2rad(bFrameUpdated(id_bFrame_origin,7));

% 1.2-) matriz de rotación
matrix_bFrame_2_sFrame = euler2rotmat(-alpha, -beta, -gamma);

% 1.3) traslación: INS como origen del b-frame
increment_bFrame = traslation(id_bFrame_origin, bFrameUpdated, 1, 2, 4);

% 1.4-) aplicación de la transformación a los vectores (incrementos b-frame)
increment_sFrame = transpose(matrix_bFrame_2_sFrame * increment_bFrame(:,2:4)');
increment_sFrame = [increment_bFrame(:, 1) increment_sFrame];

%apertura del fichero de salida
sal=fopen('integrated-navigation.txt','w');
%cabecera para resultados
print(sal, 'Situación 3D de los centros mecánicos de cada sensor');
fprintf(sal,'\n  Id         x1(m)            x2(m)            x3(m)         alpha(deg)            beta(deg)            gamma(deg)            sensor\n');
fprintf(sal,'  --        ------           ------           ------         ----------            ---------            ----------            ------\n');

[f,~] = size(bFrame);
for i = 1:f
    %datos de calibración
    fprintf(sal,'%4d%14.4f   %14.4f   %14.4f    %15.8f   %18.8f   %19.8f   %15s\n',bFrame(i, 1), bFrame(i, 2), bFrame(i, 3), bFrame(i, 4), bFrame(i, 5), bFrame(i, 6), bFrame(i, 7), bFrameNames{i});
end

print(sal, 'Offsets y desalineaciones del centro de cada sensor');
[f,~] = size(bFrameOffsets);
for i = 1:f
    %datos de calibración
    fprintf(sal,'%4d%14.4f   %14.4f   %14.4f    %15.8f   %18.8f   %19.8f   %15s\n',bFrameOffsets(i, 1), bFrameOffsets(i, 2), bFrameOffsets(i, 3), bFrameOffsets(i, 4), bFrameOffsets(i, 5), bFrameOffsets(i, 6), bFrameOffsets(i, 7), bFrameOffsetsNames{i});
end

%cabecera para resultados
print(sal, 'Situación 3D de los centros de cada sensor');
fprintf(sal,'\n  Id         x1(m)            x2(m)            x3(m)         alpha(deg)            beta(deg)            gamma(deg)            sensor\n');
fprintf(sal,'  --        ------           ------           ------         ----------            ---------            ----------            ------\n');

[f,~] = size(bFrameUpdated);
for i = 1:f
    %datos de calibración + OFFSETS
    fprintf(sal,'%4d%14.4f   %14.4f   %14.4f    %15.8f   %18.8f   %19.8f   %15s\n',bFrameUpdated(i, 1), bFrameUpdated(i, 2), bFrameUpdated(i, 3), bFrameUpdated(i, 4), bFrameUpdated(i, 5), bFrameUpdated(i, 6), bFrameUpdated(i, 7), bFrameNames{i});
end
print(sal, ['Incrementos ', 's-frame', ' con origen: ', centerPointName], 'incrementos', {increment_sFrame; bFrameNames});


%=====================================================================================================================================
%2.A
%   Obtener, para cada segundo entero, las coordenadas del centro de proyección de las cámaras. Para ello se calculará la trayectoria
%   a 50Hz basada en una solución integrada GNSS/INS mediante el empleo de las ecuaciones de navegación inercial libre.
%=====================================================================================================================================

%Trayectorias INS libre y GNSS(RTK)
coordsUTM_INS = [];
coordsUTM_GNSS = [];
trayectoriasCamaras_GNSS_INS = [];

[f,~] = size(datFileINS_50hz);
for i=1:f
    %===============================================================================
    %==========2-) Transformación de s-frame to n-frame(Norte Geográfico)===========
    %===============================================================================
    
    % ==Calculo de parametros de transformación==

    % 2.1-) ángulos de euler: (s-frame to b-frame) proporcionados por el sensor INS
    %IMU raw data (roll, pitch, yaw) (radianes)
    roll_INS  = deg2rad(datFileINS_50hz(i,13));
    pitch_INS = deg2rad(datFileINS_50hz(i,14));
    yaw_INS   = deg2rad(datFileINS_50hz(i,15));

    % 2.2-) matriz de rotación s-frame to n_frame (norte magnético)
    matrix_sFrame_nFrameNM = euler2rotmat(-roll_INS, -pitch_INS, -yaw_INS);
    
    %------Corrección por declinación magnética (δ)------
    %declinación magnética IGRF24 (radianes)
    declinacion = deg2rad(auxFileINS_50hz(i,18));

    % 2.3-) matriz de rotación n_frame (norte magnético) to n_frame (norte geográfico)
    matrix_nFrameNM_nFrameNG = euler2rotmat(0, 0, declinacion);

    % 2.4-) Aplicación de la transformación a los incrementos
    increment_nFrame = transpose(matrix_nFrameNM_nFrameNG * matrix_sFrame_nFrameNM * increment_sFrame(:,2:4)');
    increment_nFrame = [increment_sFrame(:, 1) increment_nFrame];

    % 2.5-) Aplicación de la transformación a las aceleraciones
    %aceleraciones IMU raw data (m/s2) INS en s-frame
    accINS_sFrame = datFileINS_50hz(i, 7:9);
    
    %aceleraciones (m/s2) INS en n-frame norte geográfico
    accINS_nFrame = matrix_nFrameNM_nFrameNG * matrix_sFrame_nFrameNM * accINS_sFrame';%vector (3*1)

    %===============================================================================
    %=====3-) Posición relativa en n-frame(norte geográfico) de INS respectoPLA=====
    %===============================================================================

    %incrementos n-frame(Norte Geográfico) de PLA
    id_nFrame_refSensor = find(strcmp(bFrameNames, refSensorName));
    increment_nFrame_refSensor = increment_nFrame(id_nFrame_refSensor, 2:end);

    %incrementos n-frame(Norte Geográfico) de INS
    increment_nFrame_oriSensor = increment_nFrame(id_bFrame_origin, 2:end);
    
    %vector de posición PLA->INS en n-frame(Norte Geográfico)
    vector_posicion = increment_nFrame_oriSensor - increment_nFrame_refSensor;

    %===============================================================================
    %====================4-) Determinación del instante inicial=====================
    %===============================================================================

    %instante inicial
    if i==1
        %velocidad en el n-frame derivada del GNSS(RTK): [vN; vE; vD]
        vel_nFrame = kinFileRTK_50hz(i,10:12)'; %vector (3*1)
        
        %----calculo de coordenadas geográficas de INS con base en el centro de la plataforma PLA----

        %coordenadas geográficas (lat, lng, h) medidas por GNSS-RTK centro de la plataforma PLA (precisión centimétrica)
        lat_RTK = deg2rad(geoFileRTK_50hz(i,7));
        lng_RTK = deg2rad(geoFileRTK_50hz(i,8));
        h_RTK = geoFileRTK_50hz(i,9);

        %radio de curvatura de la elipse meridiana a partir de latitud de PLA
        Rm = ro(lat_RTK, ellipsoid);
        
        %radio de curvatura del primer vertical a partir de latitud de PLA
        Rn = nu(lng_RTK, ellipsoid);
    
        %incrementos de coordenadas geográficas
        dlat = vector_posicion(1) / Rm;
        dlon = vector_posicion(2) / Rn*cos(lat_RTK);
        dh = -vector_posicion(3);
        
        %coordenadas geográficas de INS
        lat_INS = lat_RTK + dlat;
        lng_INS = lng_RTK + dlon;
        h_INS = h_RTK + dh;
        v_pos = [lat_INS; lng_INS; h_INS];%vector (3*1)
        
        %velocidad en el e-frame (dlat, dlon, dh)
        v_eFrame = vel_eFrame(v_pos(1), v_pos(3), ellipsoid, vel_nFrame); %vector (3*1)
    end

    % 4.1-) Transformación de n-frame(Norte Geográfico) to e-frame
    %matriz de rotación a partir de coordenadas lat y lon del INS
    matrix_Nav2Earth = rotNav2Earth(v_pos(1), v_pos(2));

    %aplicación de la transformación a los vectores (incrementos n-frame(NG))
    increment_eFrame = transpose(matrix_Nav2Earth * increment_nFrame(:,2:4)');
    increment_eFrame = [increment_nFrame(:, 1) increment_eFrame];

    % 4.2-)Traslación de incrementos e-frame al geocentro
    %conversión de coordenadas geográficas de INS a cartesianas tridimensionales
    [X_INS, Y_INS, Z_INS] = geotri(v_pos(1), v_pos(2), v_pos(3), ellipsoid);

    %coordenadas ECEF de todos los sensores
    coordsECEF = [increment_eFrame(:,1) increment_eFrame(:,2)+X_INS increment_eFrame(:,3)+Y_INS increment_eFrame(:,4)+Z_INS];

    % 4.3-)Conversión entre sistemas de coordenadas
    %conversion a coordenadas geográficas de todos los sensores
    id = coordsECEF(:,1);
    X = coordsECEF(:, 2);
    Y = coordsECEF(:, 3);
    Z = coordsECEF(:, 4);
    [lat, lon, h] = arrayfun(@(x, y, z) trigeo(x, y, z, ellipsoid), X, Y, Z);
    coordsGeodetic = [id, lat, lon, h];
    

    %conversion a coordenadas TMZn
    lat_s = coordsGeodetic(:,2);
    lng_s = coordsGeodetic(:,3);
    [e, n, huso] = arrayfun(@(lat, lng) geoutm2(lat, lng, ellipsoid), lat_s, lng_s);
    
    %altura ortométrica
    N = auxFileINS_50hz(i,12);
    H_ort = coordsGeodetic(:,4) - N;
    coordsTMz = [id, e, n, huso, H_ort];

    % 4.4-) Almacenando las coordenadas de los sensores de interes
    %Trayectorias de CAM1, CAM2 y CAM3
    time = auxFileINS_50hz(i,4) + auxFileINS_50hz(i,5)/60 + auxFileINS_50hz(i,6)/3600;
    timeArray = repmat(time, nCamaras, 1);%vector(3*1)
    
    %solo coordenadas de las cámaras
    filas_comunes = ismember(coordsTMz(:, 1), idCamaras);
    coordsCamaras = coordsTMz(filas_comunes, :);
    
    %Trayectora de cámaras
    newRow= [timeArray(:,1), coordsCamaras];
    trayectoriasCamaras_GNSS_INS = [trayectoriasCamaras_GNSS_INS; newRow];

    %===============================================================================
    %=====5-) Determinación de la posición 0.02s despúes respecto a la anterior=====
    %===============================================================================
    
    %---------------------------------------------------------
    %----------------Navegación inercial libre----------------
    %---------------Solución integrada GNSS/INS---------------
    %-------------------integración orden 1-------------------
    %---------------------------------------------------------

    
    %aceleraciones (m/s2) INS en n-frame corregidas
    accIMU_nFrame = acc_nFrame(v_pos(1), We, accINS_nFrame, gNormal, vel_nFrame, v_eFrame); %vector (3*1)

    %vector de gravedad normal (GRS80) (m/s2)
    gNormal = auxFileINS_50hz(i,15:17)';%vector (3*1)
    
    %velocidad n-frame 0.02s despues
    vel_nFrame = vel_nFrame + ( accIMU_nFrame * 0.02 ); %vector (3*1)
    %vel_nFrame = kinFileRTK_50hz(i,10:12)'; %vector (3*1)
    
    %velocidad e-frame 0.02s despues
    v_eFrame = vel_eFrame(v_pos(1), v_pos(3), ellipsoid, vel_nFrame);


    %coordenadas geográficas 0.02s despues
    v_pos = v_pos + (  v_eFrame * 0.02 );


    %===============================================================================
    %=========6-) Almacenando la trayectoria del INS (GNSS/RTK y INS-libre==========
    %===============================================================================

    % 6.1-) información para gráfico (centro de plataforma)
    %INS
    [e, n, ~] = geoutm2(v_pos(1), v_pos(2), ellipsoid); 
    coordsUTM_INS = [coordsUTM_INS; [e, n]];

    %GNSS(RTK)
    [x, y, ~] = geoutm2(deg2rad(geoFileRTK_50hz(i,7)), deg2rad(geoFileRTK_50hz(i,8)), ellipsoid); 
    coordsUTM_GNSS = [coordsUTM_GNSS; [x, y]];
end

%=================Extracción de coordenadas de las cámaras cada segundo entero=================
%[time,e,n,H]
coordenadasCAM1 = trayectoriasCamaras_GNSS_INS(trayectoriasCamaras_GNSS_INS(:, 2) == idCamaras(1), [1,3,4,6]);
coordenadasCAM2 = trayectoriasCamaras_GNSS_INS(trayectoriasCamaras_GNSS_INS(:, 2) == idCamaras(2), [1,3,4,6]);
coordenadasCAM3 = trayectoriasCamaras_GNSS_INS(trayectoriasCamaras_GNSS_INS(:, 2) == idCamaras(3), [1,3,4,6]);

% Convertir horas decimales a horas, minutos y segundos
decimalHours = coordenadasCAM1(:, 1);
hours = floor(decimalHours);
minutes = floor((decimalHours - hours) * 60);
seconds = ((decimalHours - hours) * 60 - minutes) * 60;

%filtro de segundos enteros
mask = abs(seconds - round(seconds))<0.01;

%extracción
coordenadasCAM1_filtradas = coordenadasCAM1(mask, :);
coordenadasCAM2_filtradas = coordenadasCAM2(mask, :);
coordenadasCAM3_filtradas = coordenadasCAM3(mask, :);


%---------------------gráfico de la trayectoria del sensor INS. INS libre vs GNSS(RTK)---------------------
figure;

%INS
plot(coordsUTM_INS(:,1), coordsUTM_INS(:,2), 'r-', 'LineWidth', 0.5);
hold on;

%GNSS(RTK)
plot(coordsUTM_GNSS(:,1), coordsUTM_GNSS(:,2), 'b-', 'LineWidth', 0.5);

%inicio de trayectoria
plot(coordsUTM_INS(1,1), coordsUTM_INS(1,2), 'go', 'MarkerFaceColor', 'g', 'MarkerSize', 4);
text(coordsUTM_INS(1,1), coordsUTM_INS(1,2), ' Inicio', 'FontSize', 9, 'Color', 'black');

%final de trayectoria
plot(coordsUTM_INS(end,1), coordsUTM_INS(end,2), 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 4);
text(coordsUTM_INS(end,1), coordsUTM_INS(end,2), ' Final', 'FontSize', 9, 'Color', 'black');
plot(coordsUTM_GNSS(end,1), coordsUTM_GNSS(end,2), 'o', 'MarkerEdgeColor', 'b', 'MarkerFaceColor', 'b', 'MarkerSize', 4);
text(coordsUTM_GNSS(end,1), coordsUTM_GNSS(end,2), ' Final', 'FontSize', 9, 'Color', 'black');

%etiquetas y título
title('Trayectoria del sensor INS calculada a 50Hz: INS(Integración de orden 1) vs GNSS(RTK)');
xlabel('x UTM (m)');
ylabel('y UTM (m)');
legend('INS trayectoria', 'GNSS trayectoria');
grid on;

%---------------------gráfico de la trayectoria de las tres cámaras. INS libre---------------------
figure;

%CAM1
plot(coordenadasCAM1_filtradas(:,2), coordenadasCAM1_filtradas(:,3), 'r-', 'LineWidth', 0.5);
hold on;

%CAM2
plot(coordenadasCAM2_filtradas(:,2), coordenadasCAM2_filtradas(:,3), 'b-', 'LineWidth', 0.5);

%CAM3
plot(coordenadasCAM3_filtradas(:,2), coordenadasCAM3_filtradas(:,3), 'k-', 'LineWidth', 0.5);

%inicio de trayectoria
plot(coordenadasCAM3_filtradas(1,2), coordenadasCAM3_filtradas(1,3), 'go', 'MarkerFaceColor', 'g', 'MarkerSize', 4);
text(coordenadasCAM3_filtradas(1,2), coordenadasCAM3_filtradas(1,3), ' Inicio', 'FontSize', 9, 'Color', 'black');

%final de trayectoria
plot(coordenadasCAM3_filtradas(end,2), coordenadasCAM3_filtradas(end,3), 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 4);
text(coordenadasCAM3_filtradas(end,2), coordenadasCAM3_filtradas(end,3), ' Final', 'FontSize', 9, 'Color', 'black');

%etiquetas y título
title('Trayectorias calculadas a 50Hz de las cámaras: INS(Integración de orden 1)');
xlabel('x UTM (m)');
ylabel('y UTM (m)');
legendHandle = legend('CAM1 trayectoria', 'CAM2 trayectoria', 'CAM3 trayectoria');
set(legendHandle, 'FontSize', 6);
legendHandle.Location = 'southeast';
grid on;


%=====================================================================================================================================
%2.B
%   Obtener, para cada segundo entero, las coordenadas del centro de proyección de las cámaras. Para ello se calculará la trayectoria
%   a 1Hz basada en la solución GNSS-RTK y los ángulos de rotación proporcionados por el INS.
%=====================================================================================================================================

%almacenará las trayectorias
trayectoriasCamaras_GNSS_RTK = [];

%==============================================================================
%==================1-) Transformación de s-frame to e-frame====================
%==============================================================================

% encontrar tiempos comunes en los datos INS(50hz) y GNSS-RTK(1hz) 
[~, idx_RTK, idx_INS] = intersect(geoFileRTK_01hz(:,1:6), datFileINS_50hz(:,1:6), 'rows', 'stable');

% Extraer las filas correspondientes de los ficheros originales
geoFileRTK_01hz_aux = geoFileRTK_01hz(idx_RTK, :);
datFileINS_50hz_aux = datFileINS_50hz(idx_INS, :);
auxFileINS_50hz_aux = auxFileINS_50hz(idx_INS, :);

%se empieza a realizar las transformaciones s-frame to e-frame para cada instante de tiempo
[f,~] = size(geoFileRTK_01hz_aux);
for i=1:f
    
    % 1.1-) Transformación de s-frame to n-frame(Norte Magnético)
    % IMU raw data (roll, pitch, yaw) (radianes)
    roll_INS  = deg2rad(datFileINS_50hz_aux(i,13));
    pitch_INS = deg2rad(datFileINS_50hz_aux(i,14));
    yaw_INS   = deg2rad(datFileINS_50hz_aux(i,15));
    
    % matriz de rotación
    matrix_sFrame_2_nFrameNM = euler2rotmat(-roll_INS, -pitch_INS, -yaw_INS);
    
    % 1.2-) Transformación de n-frame(Norte Magnético) to n-frame(Norte Geográfico)
    % declinación magnética IGRF24 (radianes)
    declinacion = deg2rad(auxFileINS_50hz_aux(i,18));
    
    % matriz de rotación
    matrix_nFrameNM_2_nFrameNG = euler2rotmat(0, 0, declinacion);

    % 1.3-) Aplicación de transformación de s-frame to n-frame(Norte Geográfico)
    increment_nFrame = transpose(matrix_nFrameNM_2_nFrameNG * matrix_sFrame_2_nFrameNM * increment_sFrame(:,2:4)');
    increment_nFrame = [increment_sFrame(:, 1) increment_nFrame];

    %==============================================================================
    %=========2-) Transformación de n-frame(Norte Geográfico) to e-frame===========
    %==============================================================================
    
    % 2.1-) Determinación de coordenadas geográficas del INS respecto al centro de la plataforma PLA
    %coordenadas geográficas de PLA: centro de la plataforma
    lat_RTK = deg2rad(geoFileRTK_01hz_aux(i,7));
    lng_RTK = deg2rad(geoFileRTK_01hz_aux(i,8));
    h_RTK = geoFileRTK_01hz_aux(i,9);

    %incrementos n-frame(Norte Geográfico) de PLA
    id_nFrame_refSensor = find(strcmp(bFrameNames, refSensorName));
    increment_nFrame_refSensor = increment_nFrame(id_nFrame_refSensor, 2:end);

    %incrementos n-frame(Norte Geográfico) de INS
    increment_nFrame_oriSensor = increment_nFrame(id_bFrame_origin, 2:end);
    
    %vector de posición PLA->INS en n-frame(Norte Geográfico)
    vector_posicion = increment_nFrame_oriSensor - increment_nFrame_refSensor;
    
    %radio de curvatura de la elipse meridiana a partir de latitud de PLA
    Rm = ro(lat_RTK, ellipsoid);
    
    %radio de curvatura del primer vertical a partir de latitud de PLA
    Rn = nu(lng_RTK, ellipsoid);

    %incrementos de coordenadas geográficas
    dlat = vector_posicion(1) / Rm;
    dlon = vector_posicion(2) / Rn*cos(lat_RTK);
    dh = -vector_posicion(3);
    
    %coordenadas geográficas de INS
    lat_INS = lat_RTK + dlat;
    lng_INS = lng_RTK + dlon;
    h_INS = h_RTK + dh;

    % 2.2-) Matriz de rotación a partir de coordenadas lat y lon del INS
    matrix_Nav2Earth = rotNav2Earth(lat_INS, lng_INS);

    % 2.3-) Aplicación de la transformación a los vectores (incrementos n-frame(NG))
    increment_eFrame = transpose(matrix_Nav2Earth*increment_nFrame(:,2:4)');
    increment_eFrame = [increment_nFrame(:, 1) increment_eFrame];

    %==============================================================================
    %=============3-) Traslación de incrementos e-frame al geocentro===============
    %==============================================================================
    
    % 3.1-) Conversión de coordenadas geográficas de INS a cartesianas tridimensionales
    [X_INS, Y_INS, Z_INS] = geotri(lat_INS, lng_INS, h_INS, ellipsoid);

    % 3.2-) Coordenadas ECEF todos los sensores
    coordsECEF = [increment_eFrame(:,1) increment_eFrame(:,2)+X_INS increment_eFrame(:,3)+Y_INS increment_eFrame(:,4)+Z_INS];
    
    % 3.3-) Conversión entre sistemas de coordenadas
    %conversion a coordenadas geográficas
    id = coordsECEF(:,1);
    X = coordsECEF(:, 2);
    Y = coordsECEF(:, 3);
    Z = coordsECEF(:, 4);
    [lat, lon, h] = arrayfun(@(x, y, z) trigeo(x, y, z, ellipsoid), X, Y, Z);
    coordsGeodetic = [id, lat, lon, h];

    %conversion a coordenadas TMZn
    lat_s = coordsGeodetic(:,2);
    lng_s = coordsGeodetic(:,3);
    [e, n, huso] = arrayfun(@(lat, lng) geoutm2(lat, lng, ellipsoid), lat_s, lng_s);
    
    %altura ortométrica
    N = auxFileINS_50hz_aux(i,12);
    H_ort = coordsGeodetic(:,4) - N;
    coordsTMz = [id, e, n, huso, H_ort];

    % 3.4-) Almacenando las coordenadas de los sensores de interes
    %Trayectorias de CAM1, CAM2 y CAM3
    time = geoFileRTK_01hz_aux(i,4) + geoFileRTK_01hz_aux(i,5)/60 + geoFileRTK_01hz_aux(i,6)/3600;
    timeArray = repmat(time, nCamaras, 1);
    
    %solo coordenadas de las cámaras
    filas_comunes = ismember(coordsTMz(:, 1), idCamaras);
    coordsCamaras = coordsTMz(filas_comunes, :);
    
    %resultado
    newRow= [timeArray(:,1), coordsCamaras];
    trayectoriasCamaras_GNSS_RTK = [trayectoriasCamaras_GNSS_RTK; newRow];
end


%---------------------gráfico de la trayectoria de las tres cámaras. GNSS(RTK) + ángulos de rotación INS---------------------
%[e, n, H]
coordenadasCAM1 = trayectoriasCamaras_GNSS_RTK(trayectoriasCamaras_GNSS_RTK(:, 2) == idCamaras(1), [3,4,6]);
coordenadasCAM2 = trayectoriasCamaras_GNSS_RTK(trayectoriasCamaras_GNSS_RTK(:, 2) == idCamaras(2), [3,4,6]);
coordenadasCAM3 = trayectoriasCamaras_GNSS_RTK(trayectoriasCamaras_GNSS_RTK(:, 2) == idCamaras(3), [3,4,6]);

figure;

%CAM1
plot(coordenadasCAM1(:,1), coordenadasCAM1(:,2), 'r-', 'LineWidth', 0.5);
hold on;

%CAM2
plot(coordenadasCAM2(:,1), coordenadasCAM2(:,2), 'b-', 'LineWidth', 0.5);

%CAM3
plot(coordenadasCAM3(:,1), coordenadasCAM3(:,2), 'k-', 'LineWidth', 0.5);

%inicio de trayectoria
plot(coordenadasCAM3(1,1), coordenadasCAM3(1,2), 'go', 'MarkerFaceColor', 'g', 'MarkerSize', 4);
text(coordenadasCAM3(1,1), coordenadasCAM3(1,2), ' Inicio', 'FontSize', 9, 'Color', 'black');

%final de trayectoria
plot(coordenadasCAM3(end,1), coordenadasCAM3(end,2), 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 4);
text(coordenadasCAM3(end,1), coordenadasCAM3(end,2), ' Final', 'FontSize', 9, 'Color', 'black');

%etiquetas y título
title({'Trayectorias calculadas a 1Hz de las cámaras', 'GNSS(RTK) + INS(roll, pitch, yaw)'});
xlabel('x UTM (m)');
ylabel('y UTM (m)');
legendHandle = legend('CAM1 trayectoria', 'CAM2 trayectoria', 'CAM3 trayectoria');
set(legendHandle, 'FontSize', 6);
legendHandle.Location = 'southeast';
grid on;


%===========================================================================================
%===============Datos para comparar con la parte de imagen (PRACTICA 3)=====================
%===========================================================================================
%apertura del fichero de salida
sal=fopen('coordenadas.csv','w');
fprintf(sal,'hora;minuto;segundo;xUTM;yUTM;H;sensor\n');

[f,~] = size(trayectoriasCamaras_GNSS_RTK);
for i = 1:f
    %H:M:S
    decimalHours = trayectoriasCamaras_GNSS_RTK(i,1);
    hours = floor(decimalHours);
    minutes = floor((decimalHours - hours) * 60);
    seconds = ((decimalHours - hours) * 60 - minutes) * 60;

    xUTM = trayectoriasCamaras_GNSS_RTK(i,3);
    yUTM = trayectoriasCamaras_GNSS_RTK(i,4);
    H = trayectoriasCamaras_GNSS_RTK(i,6);
    name_sensor = trayectoriasCamaras_GNSS_RTK(i,2);
    if name_sensor == 6
        name = "CAM1";
    elseif name_sensor == 7
        name = "CAM2";
    elseif name_sensor == 8
        name = "CAM3";
    end
    fprintf(sal, '%d;%d;%.3f;%.3f;%.3f;%.3f;%s\n', hours, minutes, seconds, xUTM, yUTM, H, name);
end

fclose('all');