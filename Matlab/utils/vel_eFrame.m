
%  Autor           : jrvalza
%  Función         : vel_eFrame
%  Descripción     : Obtención del vector de velocidad en el e-frame (dlat, dlon, dh) a partir del vector de velocidad en el n-frame. 
%  Datos de entrada: 
%                   *lat: latitud en radianes
%                   *h: altura elipsoidal
%                   *ellipsoid: elipsoide de referencia
%                   *vel_nFrame: vector de velocidad en el n-frame (vN, vE, vD) 
%  Datos de salida : vector de velocidad en el e-frame (3x1)
%  Ejemplo         : vector = vel_eFrame(lat, h, ellipsoid, vel_nFrame)


function vector=vel_eFrame(lat, h, ellipsoid, vel_nFrame)
    
    %componentes del vector velocidad en el n-frame 
    vN = vel_nFrame(1,1);
    vE = vel_nFrame(2,1);
    vD = vel_nFrame(3,1);

    %radio de curvatura de la elipse meridiana
    rm = ro(lat, ellipsoid);

    %radio de curvatura del primer vertical
    rv = nu(lat, ellipsoid);
    
    %vector de variación posicional
    dlat = vN / (rm + h);
    dlon = vE / ((rv + h) * cos(lat));
    dh = -vD;
    vector = [dlat; dlon; dh];
end