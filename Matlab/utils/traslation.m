
%  Autor           : jrvalza
%  Función         : traslation
%  Descripción     : permite realizar la traslación de un conjunto de puntos a un determinado origen de coordenadas.
%  Datos de entrada: *id: numero de fila del punto origen. 
%                         Si id='none' el origen será el centroide de todos los puntos en la matriz de entrada.
%                    *matrix: matriz de coordenadas
%                    *idColumn: columna de identificadores
%                    *firstColumn y lastColumns: inicio y fin de las columnas de coordenadas
%  Datos de salida : *incrementos de coordenadas
%  Ejemplo         : [increments] = traslation(id, matrix, idColumn, firstColumn, lastColumn)


function [increments]=traslation(id, matrix, idColumn, firstColumn, lastColumn)
    
    %traslación al punto (id) especificado
    if isscalar(id) && id > 0 && id <= size(matrix, 1)
        centerPoint = matrix(id, firstColumn:lastColumn);
        increments = [matrix(:, idColumn) matrix(:, firstColumn:lastColumn) - centerPoint];

    %Traslación al baricentro
    else
        centerPoint = mean(matrix(:, firstColumn:lastColumn));
        increments = [matrix(:, idColumn) matrix(:, firstColumn:lastColumn) - centerPoint];
    end

end