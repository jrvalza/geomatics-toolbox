%TEMA        : Transformaciones
%SALIDA      : Fichero 'solutions.txt'
                
%--------------------------------------------------------------------------------------------------------------------------------------------------------
%-------------------------------------------------------------INICIO DEL PROGRAMA------------------------------------------------------------------------
%--------------------------------------------------------------------------------------------------------------------------------------------------------

%Borrado de variables en memoria
clear;

%apertura del fichero de salida
sal=fopen('solutions.txt','w');

%==============================================================================
%===============================Datos de partida===============================
%==============================================================================

%body frame
bFrame = [
           0  0.0000  0.0000  0.0000  0.000000  0.000000  0.000000 %PLA
           1  0.0000  0.0000 -0.0250  0.263568 -0.437974  2.869214 %INS
           2  0.4000 -0.4000 -0.0150  0.000000  0.000000  0.000000 %REC2
           3  0.4000  0.4000 -0.0150  0.000000  0.000000  0.000000 %REC3
           4 -0.4000 -0.4000 -0.0150  0.000000  0.000000  0.000000 %REC4
           5 -0.4000  0.4000 -0.0150  0.000000  0.000000  0.000000 %REC5
           6  0.7000 -0.1500 -0.0800  0.196543  0.541674 -1.355847 %CAM1
           7  0.7000  0.1500 -0.0800 -0.287495  0.426588  1.128792 %CAM2
           ];
bFrameNames = {'PLA'; 'INS'; 'REC2'; 'REC3'; 'REC4'; 'REC5'; 'CAM1'; 'CAM2'};

%earth frame
eFrame = [
          2  39.2853133637  -0.2007650964  55.867 %REC2
          3  39.2853109885  -0.2007663129  55.829 %REC3
          4  39.2853143535  -0.2007680928  55.883 %REC4
          5  39.2853119474  -0.2007693816  55.866 %REC5
         ];
eFrameNames = {'REC2'; 'REC3'; 'REC4'; 'REC5'};

%sistema de referencia geodésico
sysrefGeodetic = 'ETRS89';

%elipsoide de referencia
elip = 'GRS80';
ellipsoid=parelip(elip);

%declinación magnética (deg -> rad)
delta = deg2rad(-0.700);

%ondulación del geoide (m)
N = 50.0166;

%orientación de la plataforma proporcionada por el sistema inercial-INS (deg -> rad)
roll_INS = deg2rad(1.195278);
pitch_INS = deg2rad(-1.189671);
yaw_INS = deg2rad(111.269874);

%==salida de datos en fichero==

%cabecera para resultados
print(sal, 'Información de calibración (Body-frame)');
fprintf(sal,'\n  Id         x1(m)            x2(m)            x3(m)         alpha(deg)            beta(deg)            gamma(deg)            sensor\n');
fprintf(sal,'  --        ------           ------           ------         ----------            ---------            ----------            ------\n');

[f,~] = size(bFrame);
for i = 1:f
    %datos de calibración
    fprintf(sal,'%4d%14.4f   %14.4f   %14.4f    %15.8f   %18.8f   %19.8f   %15s\n',bFrame(i, 1), bFrame(i, 2), bFrame(i, 3), bFrame(i, 4), bFrame(i, 5), bFrame(i, 6), bFrame(i, 7), bFrameNames{i});
end



%--------------------------------------------------------------------------------------------------------------------------------------------------------
%-----------------------------------------------------------------------Pregunta 1-----------------------------------------------------------------------
%--------------------------------------------------------------------------------------------------------------------------------------------------------

%1) Determinar las coordenadas geodésicas del centro de la plataforma y la orientación de la misma (roll, pitch, yaw)
% a partir de las coordenadas de los cuatro receptores de GNSS


%==============================================================================
%===1-)===========Conversión de coordenadas geodésicas a ECEF y TMzn===========
%==============================================================================

print(sal, 'Informacion del sistema terrestre (Earth-frame)');
fprintf(sal,'\n  Ondulación del geoide  : %1.4f (m)\n', N);
fprintf(sal,'\n  Sistema geodésico de referencia: %s \t\tElipsoide de referencia: %s\n\n', sysrefGeodetic, elip);
fprintf(sal,'         ----------Coordenadas geodésicas----------         ---------------Coordenadas ECEF---------------        ---------------Coordenadas TMzn---------------\n');
fprintf(sal,'  Id           ϕ                 λ             h                  X               Y              Z                   E               N           zn      H.ort\n');
fprintf(sal,'              (º)               (º)           (m)                (m)             (m)            (m)                 (m)             (m)                   (m)         sensor\n\n');

%variables que almacenan cada tipo de coordenadas obtenidas
gnssgeo = [];
gnsscart = [];
gnssTMzn = [];
[f,~] = size(eFrame);
for i=1:f
    %conversión de ángulos de pseudo decimal sexagesimal a radianes
    lat = psdo_rad(eFrame(i,2));
    lon = psdo_rad(eFrame(i,3));
    
    %otros datos, id, altura elip y nombre del sensor
    id = eFrame(i,1);
    h = eFrame(i,4);
    sensor = eFrameNames{i};
    
    %de geodésicas a cartesianas tridimensionales
    [X, Y, Z] = geotri(lat, lon, h, ellipsoid);

    %de geodésicas a coordenadas proyectadas TMzn
    [e, n, huso] = geoutm2(lat, lon, ellipsoid);
    H_ort = h-N;
    
    %almacenando el nuevo formato de coordenadas, tanto geodésicas como tridimensionales y proyectadas TMzn
    gnsscart(i, :) = [id X Y Z];
    gnssgeo(i, :) = [id lat lon h];
    gnssTMzn(i, :) = [id e n huso H_ort];

    %datos en fichero de salida
    fprintf(sal,'%4d    %s  %s    %6.4f   %18.4f   %13.4f   %14.4f   %16.4f   %13.4f   %4d  %9.4f   %9s\n',id, rad_sex(lat), rad_sex(lon), h, X, Y, Z, e, n, huso, H_ort, sensor);
end

%Se hacen en total 2 iteraciones
%En la primer iteración, se considera como origen de los sistemas de referencia, el centroide de los receptores GPS.
%En la segunda iteración se usa como origen el punto 'PLA' de coordenadas ya conocidas tras la primera iteración.
for i=1:2
    %==============================================================================
    %========2-)Obtención de coordenadas del punto origen {centerPointName}========
    %==============================================================================

    %centerPointName: identificador que define el origen de coordenadas a emplear
    if i==1
        print(sal,['Iteración: ', num2str(i)]);
        %'': centroide de receptores GPS
        centerPointName = '';
    else
        print(sal,['Iteración: ', num2str(i)]);
        %'PLA': centro de la plataforma
        centerPointName = 'PLA';
    end
    
    %añadiendo en e-frame el punto origen
    [idCenterPoint, sensorName, centerPoint] = frameOrigin(centerPointName, eFrameNames, eFrame);
    
    if ~ismember(sensorName, eFrameNames)
        eFrame(end+1, :) = [idCenterPoint centerPoint];
        eFrameNames{end+1} = sensorName;
    
        %coordenadas del origen
        lat = psdo_rad(centerPoint(1));
        lon = psdo_rad(centerPoint(2));
        h = centerPoint(3);
    
        %geodésicas
        gnssgeo(end+1, :) = [idCenterPoint lat lon h];
        
        %ECEF
        [X, Y, Z] = geotri(lat, lon, h, ellipsoid);
        gnsscart(end+1,:) = [idCenterPoint X Y Z];
        
        %TMzn
        [e, n, huso] = geoutm2(lat, lon, ellipsoid);
        H_ort = h-N;
        gnssTMzn(end+1, :) = [idCenterPoint e n huso H_ort];
    end
    %posición del origen dentro de la matriz de e-frame
    id_eFrame_origin = find(strcmp(eFrameNames, sensorName));
    

    %añadiendo en b-frame el punto origen
    [idCenterPoint, sensorName, ~] = frameOrigin(centerPointName, bFrameNames, bFrame);
    
    if ~ismember(sensorName, bFrameNames)
        if strcmp(sensorName, 'Centroide')
            bFrame(end+1, :) = [idCenterPoint [mean(bFrame(3:6,2:4)) 0 0 0]];
            bFrameNames{end+1} = sensorName;
        end
    end
    %posición del origen dentro de la matriz
    id_bFrame_origin = find(strcmp(bFrameNames, sensorName));
   
    
    %==============================================================================
    %===3-)===============Transformación de e-frame to n-frame=====================
    %==============================================================================
    origen = 'e-frame';
    destino = 'n-frame';
    
    %Nota:
    % Pasar de incrementos ECEF a incrementos locales END
    % Rotar del sistema terrestre al sistema de navegacion
    % Se necesita conocer lat y lon del origen de los incrementos de coordenadas ECEF, en este caso se define en centerPointName
    
    % El origen de coordenadas ECEF es el geocentro. 
    % El centroide de las coordenadas ECEF de los cuatro receptores GPS es aproximadamente el centro de la plataforma en coordenadas ECEF.
    
    % Traslación del geocentro al centerPointName
    incrementECEF = traslation(id_eFrame_origin, gnsscart, 1, 2, 4);
    
    %salida en fichero
    print(sal,['Transformación ', origen, ' to ', destino]);
    print(sal, ['Incrementos ', origen, '(ECEF) con origen: ', sensorName], 'incrementos', {incrementECEF; eFrameNames});
    fprintf(sal,'\n\n Coordenadas de %s:\n\n', sensorName);
    fprintf(sal, '           X0= %14.4fm    Lat0= %s\n', gnsscart(id_eFrame_origin,2), rad_sex(gnssgeo(id_eFrame_origin,2)));
    fprintf(sal, '           Y0= %14.4fm    Lon0= %s\n', gnsscart(id_eFrame_origin,3), rad_sex(gnssgeo(id_eFrame_origin,3)));
    fprintf(sal, '           Z0= %14.4fm    h0  = %1.4fm\n', gnsscart(id_eFrame_origin,4), gnssgeo(id_eFrame_origin,4));
    
    
    % ==Cálculo de parámetros de transformación==
    
    % 1-) matriz de rotación empleando lat y lon del centerPointName
    matrix_Earth2Nav = transpose(rotNav2Earth(gnssgeo(id_eFrame_origin,2), gnssgeo(id_eFrame_origin,3)));
    
    % 2-) ángulos de euler (radianes)
    [a1, a2, a3] = rotmat2euler(matrix_Earth2Nav);

    % 3-) aplicación de la transformación a los vectores (incrementos ECEF)
    incrementNav = matrix_Earth2Nav * transpose(incrementECEF(:, 2:end));
    incrementNav = [incrementECEF(:,1) incrementNav'];
    
    %salida en fichero
    print(sal, 'Matriz de rotación:', 'matriz', matrix_Earth2Nav);
    print(sal, 'Ángulos de Euler:', 'euler', {a1; a2; a3});
    print(sal, ['Incrementos en el ', destino, ':'], 'incrementos', {incrementNav; eFrameNames});
    
    
    %==============================================================================
    %==4-)================Transformación de b-frame to n-frame=====================
    %==============================================================================
    origen ='b-frame';
    destino = 'n-frame';
    print(sal,['Transformación ', origen, ' to ', destino]);
    
    % ==Obtención de puntos comunes en ambos sistemas de referencia==
    
    % obtener filas comunes
    [comunes, idx_b, idx_n] = intersect(bFrameNames, eFrameNames, 'stable');
    common_points_bframe = bFrame(idx_b, :);
    common_points_nframe = incrementNav(idx_n, :);
    
    %salida en fichero
    print(sal, 'Puntos comunes en ambos sistemas:', 'incrementos', {common_points_bframe; common_points_nframe; comunes}, origen, destino);
    

    % ==Traslación de puntos al centerPointName en ambos sitemas de referencia==
    % en sistema destino
    increment_nFrame = common_points_nframe;
    
    % en sistema origen
    increment_bFrame = traslation(id_bFrame_origin, common_points_bframe, 1, 2, 4);
    
    %salida en fichero
    print(sal, ['Incrementos de coordenadas respecto a: ', sensorName], 'incrementos', {increment_bFrame; increment_nFrame; comunes}, origen, destino);
    
    
    % ==Cálculo de parametros de transformación==
    % empleando descomposición en valores singulares de la matriz de correlación entre ambos sistemas de referencia

    % 1-) puntos comunes en ambos sistemas
    frx = increment_bFrame(:,2:end);
    tox = increment_nFrame(:,2:4);
    
    % 2-) cálculo de matriz de correlación entre sistemas
    H = tox'*frx; %proyección de puntos frx a tox
    
    % 3-) descomposición de la matriz de correlación en valores singulares
    [U,S,V] = svd(H);
    
    % 4-) cálculo de matriz de rotación
    matrix_bFrame2NavFrame = U*V';
    
    % 5-) cálculo de ángulos de euler (radianes)
    [roll_GPS, pitch_GPS, yaw_GPS] = rotmat2euler(matrix_bFrame2NavFrame);
    
    %salida en fichero
    fprintf(sal, "\n  Descomposición en valores singulares de la matriz de correlación (%s' * %s)", destino, origen);
    fprintf(sal, "\n\n\t\tA=USV'");
    print(sal, "Matriz de rotación U*V':", 'matriz', matrix_bFrame2NavFrame);
    print(sal, 'Ángulos de Euler:', 'euler', {roll_GPS; pitch_GPS; yaw_GPS});
    
    
    %==============================================================================
    %==5-)================Transformación de b-frame to e-frame=====================
    %==============================================================================
    origen ='b-frame';
    destino = 'e-frame';
    print(sal,['Transformación ', origen, ' to ', destino]);
    
    % 1-) traslación de puntos (b-frame) al centerPointName
    increment_bFrame = traslation(id_bFrame_origin, bFrame, 1, 2, 4);

    % 2-) matriz de rotación
    matrix_bFrame2eFrame = matrix_Earth2Nav'*matrix_bFrame2NavFrame;

    % 3-) ángulos de euler
    [alfa,beta,gamma] = rotmat2euler(matrix_bFrame2eFrame);

    % 4-) aplicación de la transformación a los vectores (incrementos b-frame)
    eFrame_increments = matrix_bFrame2eFrame*increment_bFrame(:, 2:4)';
    eFrame_increments = [increment_bFrame(:, 1) eFrame_increments'];

    %salida en fichero
    print(sal, ['Incrementos ', origen, ' con origen: ', sensorName], 'incrementos', {increment_bFrame; bFrameNames});
    print(sal, 'Matriz de rotación: ', 'matriz', matrix_bFrame2eFrame);
    print(sal, 'Ángulos de Euler:', 'euler', {alfa; beta; gamma});
    print(sal, ['Incrementos ', destino, ' :'], 'incrementos', {eFrame_increments; bFrameNames});
    
    
    %==============================================================================
    %=============================Solución pregunta 1==============================
    %==============================================================================
    print(sal,['Solución de la iteración: ', num2str(i)]);
    
    %orientación
    print(sal, ['Orientación de la plataforma con origen: ', sensorName], 'euler', {roll_GPS; pitch_GPS; yaw_GPS});
    
    %coordenadas e-frame de todos los sensores
    fprintf(sal,'\n\n  Coordenadas de todos los sensores:');
    fprintf(sal,'\n\n  \tOndulación del geoide  : %1.4f (m)\n', N);
    fprintf(sal,'\n  \tSistema geodésico de referencia: %s \t\tElipsoide de referencia: %s\n\n', sysrefGeodetic, elip);
    fprintf(sal,'         ----------Coordenadas geodésicas----------         ---------------Coordenadas ECEF---------------        ---------------Coordenadas TMzn---------------\n');
    fprintf(sal,'  Id           ϕ                 λ             h                  X               Y              Z                   E               N           zn      H.ort\n');
    fprintf(sal,'              (º)               (º)           (m)                (m)             (m)            (m)                 (m)             (m)                   (m)         sensor\n\n');
    
    [f,~] = size(eFrame_increments);
    for i=1:f
        %otros datos id, nombre del sensor
        id = eFrame_increments(i,1);
        sensor = bFrameNames{i};
        
        %==============================================================================
        %==============6-)Traslación de incrementos e-frame al geocentro===============
        %==============================================================================
        
        %Coordenadas ECEF
        X = eFrame_increments(i,2) + gnsscart(id_eFrame_origin,2);
        Y = eFrame_increments(i,3) + gnsscart(id_eFrame_origin,3);
        Z = eFrame_increments(i,4) + gnsscart(id_eFrame_origin,4);
    
        %de ECEF a geodésicas
        [lat, lon, h] = trigeo(X, Y, Z, ellipsoid);
        
        %de geodésicas a coordenadas proyectadas TMzn
        [e, n, huso] = geoutm2(lat, lon, ellipsoid);
        H_ort = h-N;
    
        %datos en fichero de salida
        fprintf(sal,'%4d    %s  %s    %6.4f   %18.4f   %13.4f   %14.4f   %16.4f   %13.4f   %4d   %10.4f   %8s\n',id, rad_sex(lat), rad_sex(lon), h, X, Y, Z, e, n, huso, H_ort, sensor);
        
        %Añadiendo el punto PLA al eFrame
        if strcmp(sensor, 'PLA') & ~ismember(sensor, eFrameNames)
            eFrame(end+1,:) = [1+max(eFrame(:,1)), rad_psdo(lat), rad_psdo(lon), h];
            eFrameNames{end+1} = sensor;
            gnsscart(end+1, :) = [id X Y Z];
            gnssgeo(end+1, :) = [id lat lon h];
            gnssTMzn(end+1, :) = [id e n huso H_ort];
        end
    end
end


%Determinar las coordenadas en el sistema terrestre (e-frame) de todos los dispositivos, incluyendo el origen de la plataforma en los dos casos siguientes:
%a) Empleando la orientación (roll, pitch y yaw) obtenidos en el punto 1 a partir de los datos GNSS
fprintf(sal, '\n\n');
print(sal, 'Pregunta 2a');


%b-frame
fprintf(sal, '\n  Body-frame\n');
fprintf(sal,'\n  Id         x1(m)            x2(m)            x3(m)         alpha(deg)            beta(deg)            gamma(deg)            sensor\n');
fprintf(sal,'  --        ------           ------           ------         ----------            ---------            ----------            ------\n');

[f,~] = size(bFrame);
for i = 1:f
    %datos de calibración en fichero de salida
    fprintf(sal,'%4d%14.4f   %14.4f   %14.4f    %15.8f   %18.8f   %19.8f   %15s\n',bFrame(i, 1), bFrame(i, 2), bFrame(i, 3), bFrame(i, 4), bFrame(i, 5), bFrame(i, 6), bFrame(i, 7), bFrameNames{i});
end

% ==Obtención del identificador del punto definido como origen==

%centerPointName: identificador que define el origen de coordenadas a emplear
%'PLA': centro de la plataforma
centerPointName = 'PLA';

%en b-frame
[~, sensorName, ~] = frameOrigin(centerPointName, bFrameNames, bFrame);
id_bFrame_origin = find(strcmp(bFrameNames, sensorName));

%en e-frame
[~, sensorName, ~] = frameOrigin(centerPointName, eFrameNames, eFrame);
id_eFrame_origin = find(strcmp(eFrameNames, sensorName));


%==============================================================================
%=================1-)Transformación de b-frame to n-frame======================
%==============================================================================
origen = 'b-frame';
destino = 'n-frame';
print(sal,['Transformación ', origen, ' to ', destino]);


% ==Cálculo de parametros de transformación==

% 1-) traslación
increment_bFrame = traslation(id_bFrame_origin, bFrame, 1, 2, 4);

% 2-) matriz de rotación
      %ángulos de euler (radianes) de b-frame to n-frame con GPS
      %roll_GPS, pitch_GPS, yaw_GPS obtenidos en el punto 1
matrix_bFrame2nFrame = euler2rotmat(roll_GPS,pitch_GPS,yaw_GPS);

% 3-) aplicación de la transformación a los vectores (incrementos b-frame)
increment_nFrame = transpose(matrix_bFrame2nFrame*increment_bFrame(:,2:end)');
increment_nFrame = [bFrame(:, 1) increment_nFrame];

%salida en fichero
print(sal, ['Incrementos ', origen, ' con origen: ', sensorName], 'incrementos', {increment_bFrame; bFrameNames});
print(sal, 'Ángulos de Euler from GPS:', 'euler', {roll_GPS; pitch_GPS; yaw_GPS});
print(sal, 'Matriz de rotación: ', 'matriz', matrix_bFrame2nFrame);
print(sal, ['Incrementos ', destino, ' :'], 'incrementos', {increment_nFrame; bFrameNames});

%==============================================================================
%==================2-)Transformación de n-frame to e-frame=====================
%==============================================================================
origen = 'n-frame';
destino = 'e-frame';
print(sal,['Transformación ', origen, ' to ', destino]);

% ==Calculo de parametros de transformación==

% 1-) traslación de puntos a un punto de coordenadas e-frame conocidas, en este caso se define como centerPointName
increment_nFrame = traslation(id_bFrame_origin, increment_nFrame, 1, 2, 4);

print(sal, ['Incrementos ', origen, ' con origen: ', sensorName], 'incrementos', {increment_nFrame; bFrameNames});
fprintf(sal,'\n\n Punto conocido en el e-frame: %s\n\n', sensorName);
fprintf(sal, '                   X0= %14.4fm    Lat0= %s\n', gnsscart(id_eFrame_origin,2), rad_sex(gnssgeo(id_eFrame_origin,2)));
fprintf(sal, '                   Y0= %14.4fm    Lon0= %s\n', gnsscart(id_eFrame_origin,3), rad_sex(gnssgeo(id_eFrame_origin,3)));
fprintf(sal, '                   Z0= %14.4fm    h0  = %1.4fm\n', gnsscart(id_eFrame_origin,4), gnssgeo(id_eFrame_origin,4));


% 2-) matriz de rotación empleando lat y lon del centerPointName
matrix_Nav2Earth = rotNav2Earth(gnssgeo(id_eFrame_origin,2), gnssgeo(id_eFrame_origin,3));

% 3-) ángulos de euler (radianes)
[a1, a2, a3] = rotmat2euler(matrix_Nav2Earth);

% 4-) aplicación de la transformación a los vectores (incrementos n-frame)
increment_eFrame = transpose(matrix_Nav2Earth*increment_nFrame(:,2:end)');
increment_eFrame = [bFrame(:, 1) increment_eFrame];

%salida en fichero
print(sal, 'Matriz de rotación: ', 'matriz', matrix_Nav2Earth);
print(sal, 'Ángulos de Euler: ', 'euler', {a1, a2,a3});
print(sal, ['Incrementos ', destino, ':'], 'incrementos', {increment_eFrame; bFrameNames});


%==============================================================================
%==============3-)Traslación de incrementos e-frame al geocentro===============
%==============================================================================
coordsECEF = [increment_eFrame(:,1) increment_eFrame(:,2)+gnsscart(id_eFrame_origin,2) increment_eFrame(:,3)+gnsscart(id_eFrame_origin,3) increment_eFrame(:,4)+gnsscart(id_eFrame_origin,4)];

%Solución pregunta 2a
print(sal,"Solución 2a");

fprintf(sal, '\n  Coordenadas de todos los sensores\n');
fprintf(sal,'\n  \tOndulación del geoide  : %1.4f (m)\n', N);
fprintf(sal,'\n  \tSistema geodésico de referencia: %s \t\tElipsoide de referencia: %s\n\n', sysrefGeodetic, elip);
fprintf(sal,'         ----------Coordenadas geodésicas----------         ---------------Coordenadas ECEF---------------        ---------------Coordenadas TMzn---------------\n');
fprintf(sal,'  Id           ϕ                 λ             h                  X               Y              Z                   E               N           zn      H.ort\n');
fprintf(sal,'              (º)               (º)           (m)                (m)             (m)            (m)                 (m)             (m)                   (m)         sensor\n\n');

[f,~] = size(coordsECEF);
for i=1:f
    
    %coordenadas ECEF
    X = coordsECEF(i,2);
    Y = coordsECEF(i,3);
    Z = coordsECEF(i,4);
    
    %otros datos id, nombre del sensor
    id = coordsECEF(i,1);
    sensor = bFrameNames{i};
    
    %de cartesianas tridimensionales a geodésicas
    [lat, lon, h] = trigeo(X, Y, Z, ellipsoid);

    %de geodésicas a coordenadas proyectadas TMzn
    [e, n, huso] = geoutm2(lat, lon, ellipsoid);
    H_ort = h-N;
    
    %datos en fichero de salida
    fprintf(sal,'%4d    %s  %s    %6.4f   %18.4f   %13.4f   %14.4f   %16.4f   %13.4f   %4d   %10.4f   %8s\n',id, rad_sex(lat), rad_sex(lon), h, X, Y, Z, e, n, huso, H_ort, sensor);
end


%Determinar las coordenadas en el sistema terrestre (e-frame) de todos los dispositivos, incluyendo el origen de la plataforma en los dos casos siguientes:
%b) Empleando la orientación (roll, pitch y yaw) proporcionados por el INS.

fprintf(sal, '\n\n');
print(sal, 'Pregunta 2b');

%==============================================================================
%===============================Datos de partida===============================
%==============================================================================

%identificador del punto definido como origen
centerPointName = 'INS';

%en b-frame
[~, sensorName, ~] = frameOrigin(centerPointName, bFrameNames, bFrame);
id_bFrame_origin = find(strcmp(bFrameNames, sensorName));

%nombre del punto origen de calibración de la plataforma
refSensorName = 'PLA';

%b-frame
fprintf(sal, '\n  Body-frame\n');
fprintf(sal,'\n  Id         x1(m)            x2(m)            x3(m)         alpha(deg)            beta(deg)            gamma(deg)            sensor\n');
fprintf(sal,'  --        ------           ------           ------         ----------            ---------            ----------            ------\n');
[f,~] = size(bFrame);
for i = 1:f
    %datos de calibración en fichero de salida
    fprintf(sal,'%4d%14.4f   %14.4f   %14.4f    %15.8f   %18.8f   %19.8f   %15s\n',bFrame(i, 1), bFrame(i, 2), bFrame(i, 3), bFrame(i, 4), bFrame(i, 5), bFrame(i, 6), bFrame(i, 7), bFrameNames{i});
end

%ángulos de euler (radianes) n-frame(NM) to s-frame, dados por INS (radianes)
%roll_INS, pitch_INS, yaw_INS: datos proporcionados al inicio de todo el código
print(sal, ['Roll, Pitch y Yaw proporcionados por el INS (n-frame(NM) to s-frame) - origen (', centerPointName, '):'], 'euler', {roll_INS; pitch_INS; yaw_INS});

%ángulos de euler (radianes) (s-frame to b-frame) calibración sensor INS
alpha = deg2rad(bFrame(id_bFrame_origin,5));
beta = deg2rad(bFrame(id_bFrame_origin,6));
gamma = deg2rad(bFrame(id_bFrame_origin,7));
print(sal, ['Alpha, Beta y Gamma proporcionados por calibración (s-frame to b-frame) - origen (', refSensorName,'):'], 'euler', {alpha; beta; gamma});


%==============================================================================
%==================1-) Transformación de b-frame to s-frame====================
%==============================================================================
origen = 'b-frame';
destino = 's-frame';
print(sal, ['Matriz de rotación: ', origen, ' to ', destino]);

% ==Calculo de parametros de transformación==

% 1-) ángulos de euler (radianes) por calibración
print(sal, 'Alpha, Beta y Gamma proporcionados por calibración:', 'euler', {-alpha; -beta; -gamma});

% 2-) matriz de rotación
matrix_bFrame_2_sFrame = euler2rotmat(-alpha, -beta, -gamma);
print(sal, 'Matriz de rotación:', 'matriz', matrix_bFrame_2_sFrame);


%==============================================================================
%==========2-) Transformación de s-frame to n-frame(Norte Magnético)===========
%==============================================================================
origen = 's-frame';
destino = 'n-frame(NM)';
print(sal, ['Matriz de rotación: ', origen, ' to ', destino]);

% ==Calculo de parametros de transformación==

% 1-) ángulos de euler (radianes)
print(sal, 'Alpha, Beta y Gamma proporcionados por el INS:', 'euler', {-roll_INS; -pitch_INS; -yaw_INS});

% 2-) matriz de rotación
matrix_sFrame_2_nFrameNM = euler2rotmat(-roll_INS, -pitch_INS, -yaw_INS);
print(sal, 'Matriz de rotación:', 'matriz', matrix_sFrame_2_nFrameNM);

%==============================================================================
%==3-) Transformación de n-frame(Norte Magnético) to n-frame(Norte Geográfico)=
%==============================================================================
origen = 'n-frame(NM)';
destino = 'n-frame(NG)';
print(sal, ['Matriz de rotación: ', origen, ' to ', destino]);
fprintf(sal,'\n  Declinación mágnetica (δ):\t%2.10f deg', rad2deg(delta));

% ==Calculo de parametros de transformación==

% 1-) ángulos de euler (radianes)
alpha = 0;
beta = 0;
gamma = delta;
print(sal, 'Alpha, Beta y Gamma. Corrección por declinación magnética (δ):', 'euler', {alpha; beta; gamma});

% 2-) matriz de rotación
matrix_nFrameNM_2_nFrameNG = euler2rotmat(alpha, beta, gamma);
print(sal, 'Matriz de rotación:', 'matriz', matrix_nFrameNM_2_nFrameNG);

%==============================================================================
%=======4-) Transformación total de b-frame to n-frame(Norte Geográfico)=======
%==============================================================================
%Nota:
%Para pasar del b-frame al n-frame de norte geográfico hay que pasar de
%b-frame to s-frame, s-frame to n-frame(NM) y n-frame(NM) to n-frame(NG)
origen = 'b-frame';
destino = 'n-frame(NG)';
print(sal, ['Transformación ', origen, ' to ', destino]);

% ==Calculo de parametros de transformación==

% 1-) traslación: INS como origen del b-frame
%centerPointName = 'INS';
increment_bFrame = traslation(id_bFrame_origin, bFrame, 1, 2, 4);

% 2-) matriz de rotación
matrix_bFrame_2_nFrameNG = matrix_nFrameNM_2_nFrameNG * matrix_sFrame_2_nFrameNM * matrix_bFrame_2_sFrame;

% 3-) ángulos de euler (radianes)
[alpha, beta, gamma] = rotmat2euler(matrix_bFrame_2_nFrameNG);

% 4-) aplicación de la transformación a los vectores (incrementos b-frame)
increment_nFrame = transpose(matrix_bFrame_2_nFrameNG * increment_bFrame(:,2:4)');
increment_nFrame = [increment_bFrame(:, 1) increment_nFrame];

%salida en fichero
print(sal, ['Incrementos ', origen, ' con origen : ', centerPointName], 'incrementos', {increment_bFrame; bFrameNames});
print(sal, 'Matriz de rotación:', 'matriz', matrix_bFrame_2_nFrameNG);
print(sal, 'Ángulos de euler:', 'euler', {alpha; beta; gamma});
print(sal, ['Incrementos ', destino, ':'], 'incrementos', {increment_nFrame; bFrameNames});

%==============================================================================
%==========5-) Transformación de n-frame(Norte Geográfico) to e-frame==========
%==============================================================================
origen = 'n-frame(NG)';
destino = 'e-frame';
print(sal, ['Transformación de incrementos ', origen, ' to ', destino]);

% ==Coordenadas geográficas de INS con base en el centro de la plataforma==

%refSensorName = 'PLA';
id_eFrame_refSensor = find(strcmp(eFrameNames, refSensorName));
id_nFrame_refSensor = find(strcmp(bFrameNames, refSensorName));
increment_nFrame_refSensor = increment_nFrame(id_nFrame_refSensor, 2:end);

%INS
increment_nFrame_oriSensor = increment_nFrame(id_bFrame_origin, 2:end);

%vector de posición PLA->INS
vector_posicion = increment_nFrame_oriSensor - increment_nFrame_refSensor;

%conversión de incrementos del vector de posición PLA->INS a incrementos en coordenadas geográficas

%radio de curvatura de la elipse meridiana a partir de latitud de PLA
Rm = ro(gnssgeo(id_eFrame_refSensor,2), ellipsoid);

%radio de curvatura del primer vertical a partir de latitud de PLA
Rn = nu(gnssgeo(id_eFrame_refSensor,2), ellipsoid);

%incrementos del vector de posición en sistema geodésico de coordenadas
dlat = vector_posicion(1) / Rm;
dlon = vector_posicion(2) / Rn*cos(gnssgeo(id_eFrame_refSensor,2));
dh = -vector_posicion(3);

fprintf(sal,'\n  Vector posicion %s -> %s en %s:\n', refSensorName, centerPointName, origen);
fprintf(sal,'\n                   in %10.4fm    \tdLat= %s', vector_posicion(1), rad_sex(dlat));
fprintf(sal,'\n                   ie %10.4fm    \tdLon=  %s', vector_posicion(2), rad_sex(dlon));
fprintf(sal,'\n                   id %10.4fm    \tdh  = %8.4fm', vector_posicion(3), dh);

%coordenadas geodésicas de PLA
fprintf(sal,'\n\n Coordenadas %s de: %s\n\n', destino, refSensorName);
fprintf(sal, '                   X0= %14.4fm    Lat0= %s\n', gnsscart(id_eFrame_refSensor,2), rad_sex(gnssgeo(id_eFrame_refSensor,2)));
fprintf(sal, '                   Y0= %14.4fm    Lon0= %s\n', gnsscart(id_eFrame_refSensor,3), rad_sex(gnssgeo(id_eFrame_refSensor,3)));
fprintf(sal, '                   Z0= %14.4fm    h0  = %1.4fm\n', gnsscart(id_eFrame_refSensor,4), gnssgeo(id_eFrame_refSensor,4));

%coordenadas geodésicas de INS
lat = gnssgeo(id_eFrame_refSensor,2) + dlat;
lon = gnssgeo(id_eFrame_refSensor,3) + dlon;
h = gnssgeo(id_eFrame_refSensor,4) + dh;

%ECEF
[X, Y, Z] = geotri(lat, lon, h, ellipsoid);

%TMzn
[e, n, huso] = geoutm2(lat, lon, ellipsoid);
H_ort = h-N;

%almacenando las coordenadas de INS en el eFrame
if ~ismember(centerPointName, eFrameNames)
    eFrame(end+1,:) = [1+max(eFrame(:,1)), rad_psdo(lat), rad_psdo(lon), h];
    eFrameNames{end+1} = centerPointName;
end

id_eFrame_oriSensor = find(strcmp(eFrameNames, centerPointName));
gnsscart(id_eFrame_oriSensor, :) = [id_eFrame_oriSensor X Y Z];
gnssgeo(id_eFrame_oriSensor, :) = [id_eFrame_oriSensor lat lon h];
gnssTMzn(id_eFrame_oriSensor, :) = [id_eFrame_oriSensor e n huso H_ort];

fprintf(sal,'\n\n Coordenadas %s de: %s\n\n', destino, centerPointName);
fprintf(sal, '                   X0= %14.4fm    Lat0= %s\n', gnsscart(id_eFrame_oriSensor,2), rad_sex(gnssgeo(id_eFrame_oriSensor,2)));
fprintf(sal, '                   Y0= %14.4fm    Lon0= %s\n', gnsscart(id_eFrame_oriSensor,3), rad_sex(gnssgeo(id_eFrame_oriSensor,3)));
fprintf(sal, '                   Z0= %14.4fm    h0  = %1.4fm\n', gnsscart(id_eFrame_oriSensor,4), gnssgeo(id_eFrame_oriSensor,4));


% ==Calculo de parametros de transformación==

% 1-) traslacion de incrementos (n-frame(NG
increment_nFrame = traslation(id_bFrame_origin, increment_nFrame, 1, 2, 4);

% 2-) matriz de rotación a partir de coordenadas lat y lon del INS
matrix_Nav2Earth = rotNav2Earth(gnssgeo(id_eFrame_oriSensor, 2), gnssgeo(id_eFrame_oriSensor, 3));

% 3-) ángulos de euler (radianes)
[a1, a2, a3] = rotmat2euler(matrix_Nav2Earth);

% 4-) aplicación de la transformación a los vectores (incrementos n-frame(NG))
increment_eFrame = transpose(matrix_Nav2Earth*increment_nFrame(:,2:4)');
increment_eFrame = [increment_nFrame(:, 1) increment_eFrame];

%salida en fichero
print(sal, ['Incrementos en ', origen, ' con origen: ', sensorName], 'incrementos', {increment_nFrame; bFrameNames});
print(sal, 'Matriz de rotación:', 'matriz', matrix_Nav2Earth);
print(sal, 'Ángulos de Euler:', 'euler', {a1; a2; a3});
print(sal, ['Incrementos en ', destino, ':'], 'incrementos', {increment_eFrame; bFrameNames});


%Solución
%==============================================================================
%==============6-)Traslación de incrementos e-frame al geocentro===============
%==============================================================================
coordsECEF = [increment_eFrame(:,1) increment_eFrame(:,2)+gnsscart(id_eFrame_oriSensor, 2) increment_eFrame(:,3)+gnsscart(id_eFrame_oriSensor, 3) increment_eFrame(:,4)+gnsscart(id_eFrame_oriSensor, 4)];

print(sal,"Solución 2b");
fprintf(sal, '\n  Coordenadas %s de todos los sensores\n', destino);
fprintf(sal,'\n  Ondulación del geoide  : %1.4f (m)\n', N);
fprintf(sal,'\n  Sistema geodésico de referencia: %s \t\tElipsoide de referencia: %s\n\n', sysrefGeodetic, elip);
fprintf(sal,'         ----------Coordenadas geodésicas----------         ---------------Coordenadas ECEF---------------        ---------------Coordenadas TMzn---------------\n');
fprintf(sal,'  Id           ϕ                 λ             h                  X               Y              Z                   E               N           zn      H.ort\n');
fprintf(sal,'              (º)               (º)           (m)                (m)             (m)            (m)                 (m)             (m)                   (m)         sensor\n\n');

[f,~] = size(coordsECEF);
for i=1:f
    
    %coordenadas ECEF
    X = coordsECEF(i,2);
    Y = coordsECEF(i,3);
    Z = coordsECEF(i,4);
    
    %otros datos id, nombre del sensor
    id = coordsECEF(i,1);
    sensor = bFrameNames{i};
    
    %coordenadas geodésicas
    [lat, lon, h] = trigeo(X, Y, Z, ellipsoid);

    %coordenadas TMzn
    [e, n, huso] = geoutm2(lat, lon, ellipsoid);
    H_ort = h-N;

    %datos del en fichero de salida
    fprintf(sal,'%4d    %s  %s    %6.4f   %18.4f   %13.4f   %14.4f   %16.4f   %13.4f   %4d   %10.4f   %8s\n',id, rad_sex(lat), rad_sex(lon), h, X, Y, Z, e, n, huso, H_ort, sensor);
end

fclose('all');

