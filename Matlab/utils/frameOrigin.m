
%  Autor           : jrvalza
%  Función         : frameOrigin
%  Descripción     : permite obtener las coordenadas del punto definido como origen en un determinado frame.
%
%  Datos de entrada: *name: nombre del sensor.
%                    *frameNames: array con los nombres de sensores
%                    *frame: matriz de coordenadas
%
%  Datos de salida : *idCenterPoint: identificador del punto en la matriz frameNames de entrada
%                    *sensorName: nombre del sensor o punto origen
%                    *centerPoint: coordenadas del punto origen
%
%  Ejemplo         : [idCenterPoint, sensorName, centerPoint] = frameOrigin(name, frameNames, frame)


function [idCenterPoint, sensorName, centerPoint] = frameOrigin(name, frameNames, frame)

    if ismember(name, frameNames)
        idCenterPoint = find(strcmp(frameNames, name));

        %extracción de coordenadas
        x1 = frame(idCenterPoint,2);
        x2 = frame(idCenterPoint,3);
        x3 = frame(idCenterPoint,4);
        centerPoint = [x1 x2 x3];
        sensorName = name;

    else
        %extracción de coordenadas
        idCenterPoint = 1+max(frame(:,1));
        x1 = mean(frame(:,2));
        x2 = mean(frame(:,3));
        x3 = mean(frame(:,4));
        centerPoint = [x1, x2, x3];
        sensorName = 'Centroide';

    end

end