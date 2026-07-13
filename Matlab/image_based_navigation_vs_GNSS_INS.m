%TEMA        : Navegación por imagen vs GNSS/INS  
%SALIDA      : gráficos comparativos

%--------------------------------------------------------------------------------------------------------------------------------------------------------
%-------------------------------------------------------------INICIO DEL PROGRAMA------------------------------------------------------------------------
%--------------------------------------------------------------------------------------------------------------------------------------------------------

%Borrado de variables en memoria
clear;

%elipsoide de referencia
elip = 'GRS80';
ellipsoid=parelip(elip);

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

%[YY, MM, DD, HH, MM, SS, lat, lng, h, ro, nu, N, def_ro, def_nu, gN, gE, gD, declinacion, epoch]
auxFileINS_50hz = load("INS\INS-10-10-2024-50Hz-ses6.aux");

%-----------------------------------------------------------
%-------------------Datos receptores GNSS-------------------
%-----------------------------------------------------------

%[YY, MM, DD, HH, MM, SS, lat, lng, h, elat, elng, eh, elapsedTime, positions/receivers(0-4), solution_quality, epoch]
geoFileRTK_50hz = load("GNSS\50hz\RTK-10-10-2024-50Hz-ses6.geo");


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


%=====================================================================================================================================
%================================================Obtención de trayectoria con GNSS+INS================================================
%=====================================================================================================================================

%almacenará las trayectorias
trayectoriasCamaras_GNSS_RTK = [];

%==============================================================================
%==================1-) Transformación de s-frame to e-frame====================
%==============================================================================

%se empieza a realizar las transformaciones s-frame to e-frame para cada instante de tiempo
[f,~] = size(geoFileRTK_50hz);
for i=1:f
    
    % 1.1-) Transformación de s-frame to n-frame(Norte Magnético)
    % IMU raw data (roll, pitch, yaw) (radianes)
    roll_INS  = deg2rad(datFileINS_50hz(i,13));
    pitch_INS = deg2rad(datFileINS_50hz(i,14));
    yaw_INS   = deg2rad(datFileINS_50hz(i,15));

    % matriz de rotación
    matrix_sFrame_2_nFrameNM = euler2rotmat(-roll_INS, -pitch_INS, -yaw_INS);
    
    % 1.2-) Transformación de n-frame(Norte Magnético) to n-frame(Norte Geográfico)
    % declinación magnética IGRF24 (radianes)
    declinacion = deg2rad(auxFileINS_50hz(i,18));
    
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
    lat_RTK = deg2rad(geoFileRTK_50hz(i,7));
    lng_RTK = deg2rad(geoFileRTK_50hz(i,8));
    h_RTK = geoFileRTK_50hz(i,9);

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
    N = auxFileINS_50hz(i,12);
    H_ort = coordsGeodetic(:,4) - N;
    coordsTMz = [id, e, n, huso, H_ort];

    % 3.4-) Almacenando las coordenadas de los sensores de interes cada 0.5seg
    %Trayectorias de CAM1, CAM2 y CAM3
    hours = geoFileRTK_50hz(i,4);
    minutes = geoFileRTK_50hz(i,5);
    seconds = geoFileRTK_50hz(i,6);

    %comprobar que el tiempo es cada 0.5 segundos
    decimal_part = seconds - floor(seconds);
    is_zero_or_five = (abs(decimal_part - 0.00) < 1e-6) | (abs(decimal_part - 0.5) < 1e-6);
    if is_zero_or_five
  
        timeArray = repmat([hours, minutes, seconds], nCamaras, 1);
        ang_rot = repmat([roll_INS, pitch_INS, yaw_INS, declinacion], nCamaras, 1);

        %solo coordenadas de las cámaras
        filas_comunes = ismember(coordsTMz(:, 1), idCamaras);
        coordsCamaras = coordsTMz(filas_comunes, :);
        
        %resultado
        newRow= [timeArray, coordsCamaras, ang_rot];
        
        %HH, MM, SS, ID, e, n, huso, H, roll, pitch, yaw, declinacion
        trayectoriasCamaras_GNSS_RTK = [trayectoriasCamaras_GNSS_RTK; newRow];
    end
end


%=====================================================================================================================================
%==============================================================GRAFICOS===============================================================
%=====================================================================================================================================

%[e, n, huso, H, roll, pitch, yaw, declinacion]
trayectoria_GNSS_RTK = trayectoriasCamaras_GNSS_RTK(trayectoriasCamaras_GNSS_RTK(1:1163, 4) == idCamaras(3), [5,6,7,8,9,10,11,12]);

%[id, e, n, H, omega, phi, kappa]
trayectoriasCamaras_imagen = readtable('trayectoriasCamaras_imagen.csv');

%==========================================================================================================
%===================================Trayectoria de la cámara 3. GNSS+INS===================================
%==========================================================================================================

figure;
plot(trayectoria_GNSS_RTK(:,1), trayectoria_GNSS_RTK(:,2), 'b-', 'LineWidth', 1);
hold on;

%inicio y final de trayectoria
plot(trayectoria_GNSS_RTK(1,1), trayectoria_GNSS_RTK(1,2), 'go', 'MarkerFaceColor', 'k', 'MarkerSize', 4);
text(trayectoria_GNSS_RTK(1,1), trayectoria_GNSS_RTK(1,2), ' Inicio', 'FontSize', 9, 'Color', 'black');
plot(trayectoria_GNSS_RTK(end,1), trayectoria_GNSS_RTK(end,2), 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 4);
text(trayectoria_GNSS_RTK(end,1), trayectoria_GNSS_RTK(end,2), ' Final', 'FontSize', 9, 'Color', 'black');

%etiquetas y título
title({'Trayectoria de la cámara 3 calculada a 0.5 segundos', 'GNSS(RTK) + INS(roll, pitch, yaw)'});
xlabel('x UTM (m)');
ylabel('y UTM (m)');
legend('Trayectoria');
grid on;
hold off



%==========================================================================================================
%================================Trayectoria de la cámara 3. FOTOGRAMETRÍA=================================
%==========================================================================================================

figure;
plot(trayectoriasCamaras_imagen.xUTM, trayectoriasCamaras_imagen.yUTM, 'r-', 'LineWidth', 1);
hold on;

%inicio y final de trayectoria
plot(trayectoriasCamaras_imagen.xUTM(1), trayectoriasCamaras_imagen.yUTM(1), 'go', 'MarkerFaceColor', 'k', 'MarkerSize', 4);
text(trayectoriasCamaras_imagen.xUTM(1), trayectoriasCamaras_imagen.yUTM(1), ' Inicio', 'FontSize', 9, 'Color', 'black');
plot(trayectoriasCamaras_imagen.xUTM(end), trayectoriasCamaras_imagen.yUTM(end), 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 4);
text(trayectoriasCamaras_imagen.xUTM(end), trayectoriasCamaras_imagen.yUTM(end), ' Final', 'FontSize', 9, 'Color', 'black');

%etiquetas y título
title({'Trayectoria de la cámara 3 calculada por fotogrametría', 'una posición cada 0.5 segundos'});
xlabel('x UTM (m)');
ylabel('y UTM (m)');
legend('Trayectoria');
grid on;
hold off


%=====================================================================================================================================
%===================================gráfico: Trayectoria de la cámara 3. GNSS+INS vs Photogrametría===================================
%=====================================================================================================================================
figure;
%===========================================================
%=======================CAM3 GNSS+INS=======================
%===========================================================
plot(trayectoria_GNSS_RTK(:,1), trayectoria_GNSS_RTK(:,2), 'b.', 'MarkerSize', 4);
hold on;
%inicio y final de trayectoria GNSS+INS
text(trayectoria_GNSS_RTK(1,1), trayectoria_GNSS_RTK(1,2), ' Inicio(GNSS+INS)', 'FontSize', 9, 'Color', 'black');
text(trayectoria_GNSS_RTK(end,1), trayectoria_GNSS_RTK(end,2), ' Final(GNSS+INS)', 'FontSize', 9, 'Color', 'black');

%===========================================================
%========================CAM3 imagen========================
%===========================================================
plot(trayectoriasCamaras_imagen.xUTM(3:end),trayectoriasCamaras_imagen.yUTM(3:end), 'r.', 'MarkerSize', 4);
%inicio y final de trayectoria imagen
text(trayectoriasCamaras_imagen.xUTM(3),trayectoriasCamaras_imagen.yUTM(3), ' Inicio(imagen)', 'FontSize', 9, 'Color', 'black');
text(trayectoriasCamaras_imagen.xUTM(end),trayectoriasCamaras_imagen.yUTM(end), ' Final(imagen)', 'FontSize', 9, 'Color', 'black');

%etiquetas y título
title({'Comparación de trayectorias obtenidas de la cámara 3', 'GNSS(RTK) + INS(roll, pitch, yaw) vs Fotogrametría'});
xlabel('x UTM (m)');
ylabel('y UTM (m)');
legendHandle = legend('GNSS(RTK)+INS', 'Fotogrametría');
set(legendHandle, 'FontSize', 6);
legendHandle.Location = 'southeast';
grid on;
hold off

%=====================================================================================================================================
%==================================Transformación de (roll, pitch, yaw) a ángulos (omega, phi, kappa)=================================
%=====================================================================================================================================
%auxiliar
omega_phi_kappa_from_INS = [];
omega_phi_kappa_from_PHOTO = [];

[f,~] = size(trayectoriasCamaras_imagen);
for i = 3:f % Ajusta según tu rango
    % Posición de la cámara
    %xi = trayectoriasCamaras_imagen.xUTM(i);
    %yi = trayectoriasCamaras_imagen.yUTM(i);
    %zi = trayectoriasCamaras_imagen.H(i);
    
    % Ángulos de rotación (fotogrametría)
    omega = deg2rad(trayectoriasCamaras_imagen.omega(i));
    phi = deg2rad(trayectoriasCamaras_imagen.phi(i));
    kappa = deg2rad(trayectoriasCamaras_imagen.kappa(i));
    omega_phi_kappa_from_PHOTO = [omega_phi_kappa_from_PHOTO;[omega, phi, kappa]];

    j = i-2;
    % Ángulos de rotación (INS)
    roll = trayectoria_GNSS_RTK(j, 5);
    pitch = trayectoria_GNSS_RTK(j, 6);
    yaw = trayectoria_GNSS_RTK(j, 7);
    
    %conversión de coordenadas (utm -> geográficas)
    xp = trayectoria_GNSS_RTK(j, 1);
    yp = trayectoria_GNSS_RTK(j, 2);
    hp = trayectoria_GNSS_RTK(j,4);
    husop = trayectoria_GNSS_RTK(j, 3);
    [lat,lng] = utmgeo(xp, yp, husop, ellipsoid);

    %matriz de transformación s-frame(INS) -> n-frame
    matrix_b2n = euler2rotmat(-roll, -pitch, -yaw);
    
    %matriz de transformación n-frame -> n-frame(norte geográfico)
    p = euler2rotmat(0,0,trayectoria_GNSS_RTK(j,8));

    %matriz de cambio de base: NED -> ENU
    matrix_change_base = [0, 1, 0;
                          1, 0, 0;
                          0, 0, -1];
    %%matriz de transformación n-frame -> e-frame 
    matrix_n2B = rotNav2Earth(lat, lng);

    %transformación total
    total_matrix = matrix_n2B * p * matrix_b2n * matrix_change_base;

    %extracción de ángulos (omega, phi, kappa)
    [a1, a2, a3] = rotmat2euler(total_matrix);
    omega_phi_kappa_from_INS = [omega_phi_kappa_from_INS;[a1, a2, a3]];

end


%=====================================================================================================================================
%========================================gráfico: Comparaciónn de ángulos (omega, phi, kappa)=========================================
%=====================================================================================================================================

%----Datos para el gráfico----

%eje X
positions = 1:f-2;

%series de datos: eje Y
data = [
        omega_phi_kappa_from_INS';  %INS raw data (roll, pitch, yaw) to (omega, phi, kappa)
        omega_phi_kappa_from_PHOTO';    %Fotogrametric raw data (omega, phi, kappa)
       ];

%títulos de gráficos
titles = {
          {'Comparativa del ángulo OMEGA', 'GNSS(RTK)+INS vs Fotogrametría'};
          {'Comparativa del ángulo PHI', 'GNSS(RTK)+INS vs Fotogrametría'};
          {'Comparativa del ángulo KAPPA', 'GNSS(RTK)+INS vs Fotogrametría'}
         };

%etiquetas eje Y
yLabels = {'Omega (rad)', 'Phi (rad)', 'Kappa (rad)'};

%legenda de series de datos
leg = {'basado en INS', 'basado en fotogrametría'};

%número de gráficos a generar
numPlots = size(data, 1)/2;

%generación de gráfico
figure;

% Iterar sobre cada fila de datos
for i = 1:numPlots
    subplot(numPlots, 1, i);
    
    %Gráficos del eje izquierdo
    %serie de datos 1
    plot(positions, data(i,:), 'b-', 'LineWidth', 1);
    hold on;
    ylabel(yLabels{i});

    %serie de datos2
    plot(positions, data(i+numPlots,:), 'r--', 'LineWidth', 1);

    legendHandle = legend(leg{1}, leg{2});

    % Ajustar el tamaño de la fuente de la leyenda
    set(legendHandle, 'FontSize', 6);
    legendHandle.Location = 'southeast'; % Posición superior izquierda
    
    %Título, etiquetas y leyenda
    title(titles{i});
    xlabel('position');
    grid on;

end
hold off


%=====================================================================================================================================
%===============================================Estadisticas de diferencias de posición===============================================
%=====================================================================================================================================
% Calcular las distancias 2D y 3D
dx = trayectoria_GNSS_RTK(:,1) - trayectoriasCamaras_imagen.xUTM(3:end);
dy = trayectoria_GNSS_RTK(:,2) - trayectoriasCamaras_imagen.yUTM(3:end);
dz = trayectoria_GNSS_RTK(:,4) - trayectoriasCamaras_imagen.H(3:end);

distancias3D = sqrt(dx.^2 + dy.^2 + dz.^2);
distancias2D = sqrt(dx.^2 + dy.^2);

% Crear la figura para los histogramas
figure;

% Histograma para las distancias 2D
subplot(1, 2, 1);  % Subgráfico 1 (1 fila, 2 columnas, 1er gráfico)
histogram(distancias2D, 'BinLimits', [0, max(distancias2D)], 'FaceColor', 'b');
title({'Histograma de diferencias de posición 2D', 'GNSS(RTK)+INS vs Fotogrametría'});
xlabel('Distancia (m)');
ylabel('Frecuencia');
grid on;

% Histograma para las distancias 3D
subplot(1, 2, 2);  % Subgráfico 2 (1 fila, 2 columnas, 2do gráfico)
histogram(distancias3D, 'BinLimits', [0, max(distancias3D)], 'FaceColor', 'r');
title({'Histograma de diferencias de posición 3D', 'GNSS(RTK)+INS vs Fotogrametría'});
xlabel('Distancia (m)');
ylabel('Frecuencia');
grid on;

% Resumen de estadísticas
fprintf('Resumen de distancias 2D:\n');
fprintf('Media: %.4f\n', mean(distancias2D));
fprintf('Mediana: %.4f\n', median(distancias2D));
fprintf('Desviación estándar: %.4f\n', std(distancias2D));
fprintf('Mínimo: %.4f\n', min(distancias2D));
fprintf('Máximo: %.4f\n', max(distancias2D));

fprintf('\nResumen de distancias 3D:\n');
fprintf('Media: %.4f\n', mean(distancias3D));
fprintf('Mediana: %.4f\n', median(distancias3D));
fprintf('Desviación estándar: %.4f\n', std(distancias3D));
fprintf('Mínimo: %.4f\n', min(distancias3D));
fprintf('Máximo: %.4f\n', max(distancias3D));

%=====================================================================================================================================
%====================================================Gráfica 3D de las trayectorias===================================================
%=====================================================================================================================================
figure;

% Graficar la trayectoria GNSS (en azul)
h1 = plot3(trayectoria_GNSS_RTK(:,1), trayectoria_GNSS_RTK(:,2), trayectoria_GNSS_RTK(:,4), 'b-', 'LineWidth', 1, 'DisplayName', 'GNSS(RTK) + INS');
hold on;

% Graficar la trayectoria de las cámaras (en rojo)
h2 = plot3(trayectoriasCamaras_imagen.xUTM, trayectoriasCamaras_imagen.yUTM, trayectoriasCamaras_imagen.H, 'r-', 'LineWidth', 1, 'DisplayName', 'Fotogrametría');

% Puntos de inicio y final (sin leyenda)
plot3(trayectoria_GNSS_RTK(1,1), trayectoria_GNSS_RTK(1,2), trayectoria_GNSS_RTK(1,4), 'g.', 'MarkerSize', 10);
plot3(trayectoria_GNSS_RTK(end,1), trayectoria_GNSS_RTK(end,2), trayectoria_GNSS_RTK(end,4), 'k.', 'MarkerSize', 10);
text(trayectoria_GNSS_RTK(1,1), trayectoria_GNSS_RTK(1,2), trayectoria_GNSS_RTK(1,4), ' Inicio(GNSS+INS)', 'FontSize', 9, 'Color', 'black');
text(trayectoria_GNSS_RTK(end,1), trayectoria_GNSS_RTK(end,2), trayectoria_GNSS_RTK(end,4), ' Final(GNSS+INS)', 'FontSize', 9, 'Color', 'black');

plot3(trayectoriasCamaras_imagen.xUTM(3),trayectoriasCamaras_imagen.yUTM(3),trayectoriasCamaras_imagen.H(3), 'g.', 'MarkerSize', 10);
plot3(trayectoriasCamaras_imagen.xUTM(end),trayectoriasCamaras_imagen.yUTM(end),trayectoriasCamaras_imagen.H(end), 'k.', 'MarkerSize', 10);
text(trayectoriasCamaras_imagen.xUTM(3),trayectoriasCamaras_imagen.yUTM(3),trayectoriasCamaras_imagen.H(3), ' Inicio(imagen)', 'FontSize', 9, 'Color', 'black');
text(trayectoriasCamaras_imagen.xUTM(end),trayectoriasCamaras_imagen.yUTM(end), trayectoriasCamaras_imagen.H(end), ' Final(imagen)', 'FontSize', 9, 'Color', 'black');

% Etiquetas y título
xlabel('xUTM');
ylabel('yUTM');
zlabel('H');
title({'Comparación de trayectorias obtenidas de la cámara 3', 'GNSS(RTK) + INS(roll, pitch, yaw) vs Fotogrametría'});

% Añadir una leyenda solo para las trayectorias principales
legend([h1, h2]);

% Ajustar la vista 3D
axis equal; % Para que las escalas de los ejes X, Y y Z sean iguales
grid on;
view(3); % Vista 3D
hold off;
