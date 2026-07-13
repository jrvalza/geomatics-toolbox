
%  Autor           : jrvalza
%  Función         : rotmat2euler
%  Descripción     : Obtención de ángulos de euler a partir de una matriz de rotación
%  Datos de entrada: *matriz de rotación (3x3)
%
%  Datos de salida : angulos de euler (a1,a2,a3)
%  Ejemplo         : [a1, a2, a3]=rotmat2euler(matrix)


function [a1, a2, a3]=rotmat2euler(matrix)
    
    %cálculo de ángulos
    a1 = atan2(-matrix(3,2), matrix(3,3));
    a2 = asin(max(-1, min(1, matrix(3,1)))); % asegurando el rango [-1, 1]
    a3 = atan2(-matrix(2,1), matrix(1,1));

end