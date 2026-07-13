
%  Autor           : jrvalza
%  Función         : acc_nFrame
%  Descripción     : Obtención del vector de aceleración en el n-frame (aN, aE, aD) 
%  Datos de entrada: 
%                    *lat: latitud en radianes
%                    *We: velocidad angular de la tierra
%                    *accINS: aceleración proporcionadas por el INS en el n-frame
%                    *gNormal: vector de gravedad normal
%                    *vel_nFrame: vector de velocidad en el n-frame
%                    *vel_eFrame: vector de velocidad en el e-frame
%  Datos de salida : vector de aceleración en el n-frame (3x1)
%  Ejemplo         : vector = acc_nFrame(lat, We, accINS, gNormal, vel_nFrame, vel_eFrame)


function vector = acc_nFrame(lat, We, accINS, gNormal, vel_nFrame, vel_eFrame)
    
    %componentes de la aceleración proporcionadas por el INS en el n-frame
    aN_ins = accINS(1,1);
    aE_ins = accINS(2,1);
    aD_ins = accINS(3,1);

    %componentes del vector de gravedad normal
    gN = gNormal(1,1);
    gE = gNormal(2,1);
    gD = gNormal(3,1);

    %componentes del vector de velocidad en el n-frame
    vN = vel_nFrame(1,1);
    vE = vel_nFrame(2,1);
    vD = vel_nFrame(3,1);

    %componentes del vector de velocidad en el e-frame
    dlat = vel_eFrame(1,1);
    dlon = vel_eFrame(2,1);
    %dh = vel_eFrame(3,1);

    %cálculo de las componentes del vector aceleración en el n-frame
    aN = aN_ins + gN - 2*We*vE*sin(lat) + dlat*vD - dlon*sin(lat)*vE;
    aE = aE_ins + gE - 2*We*vN*sin(lat) + 2*We*vD*cos(lat) + dlon*vN*sin(lat) + dlon*vD*cos(lat);
    aD = aD_ins + gD - 2*We*vE*cos(lat) - dlon*vE*cos(lat) - dlat*vN;

    vector = [aN; aE; aD];

end