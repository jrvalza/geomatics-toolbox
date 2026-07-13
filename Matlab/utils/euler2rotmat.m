
%  Autor           : jrvalza
%  Función         : euler2rotmat
%  Descripción     : Obtención de la matriz de rotación a partir de los ángulos de euler 
%  Datos de entrada: ángulos de euler (alpha, beta, gamma)
%
%  Datos de salida : matriz de rotación (3x3)
%  Ejemplo         : matrix=euler2rotmat(alpha, beta, gamma)


function matrix=euler2rotmat(alpha, beta, gamma)
    
    %cálculo de cada elemento de la matriz
    c11 = cos(gamma) * cos(beta);
    c21 = -sin(gamma) * cos(beta);
    c31 = sin(beta);
    
    c12 = (cos(gamma) * sin(beta) * sin(alpha)) + (sin(gamma) * cos(alpha));
    c22 = (-sin(gamma) * sin(beta) * sin(alpha)) + (cos(gamma)*cos(alpha));
    c32 = -cos(beta)*sin(alpha);
    
    c13 = (-cos(gamma) * sin(beta) * cos(alpha)) + (sin(gamma) * sin(alpha));
    c23 = (sin(gamma) * sin(beta) * cos(alpha)) + (cos(gamma) * sin(alpha));
    c33 = cos(beta) * cos(alpha);
    
    %matriz de salida
    matrix = [c11 c12 c13
              c21 c22 c23
              c31 c32 c33];

end