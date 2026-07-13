
%  Autor           : jrvalza
%  Función         : rotNav2Earth
%  Descripción     : Calculo de matriz de rotación para pasar del sistema
%                    de coordenadas de navegación (local: n-frame) al sistema terrestre (e-frame)
%  Datos de entrada: *latitud y longitud del origen del sistema local (n-frame) en radianes:
%
%  Datos de salida : matriz de rotación para pasar del n-frame al e-frame 
%  Ejemplo         : matrix=rotNav2Earth(lat, lon)


function matrix=rotNav2Earth(lat,lon)
    
    %cálculo de los elementos de la matriz
    m11 = -sin(lat)*cos(lon);
    m12 = -sin(lon);
    m13 = -cos(lat)*cos(lon);
    
    m21 = -sin(lat)*sin(lon);
    m22 = cos(lon);
    m23 = -cos(lat)*sin(lon);
    
    m31 = cos(lat);
    m32 = 0;
    m33 = -sin(lat);
    
    %matriz de rotación
    matrix = [m11 m12 m13
              m21 m22 m23
              m31 m32 m33
              ];
end