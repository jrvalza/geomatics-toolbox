
%  Autor           : jrvalza
%  Función         : print
%  Descripción     : permite imprimir datos con un formato predefinido
%
%  Datos de entrada: *matrices (3*3)
%                    *incrementos de coordenadas (en 1 o en 2 sistemas)
%                    *ángulos de euler
%
%  Datos de salida : imprime en el fichero de salida los datos de entrada
%  Ejemplo         : imprimir(fichero, *args)
%                    *text: titulo o subtitulo
%                    *type: matriz, incrementos, ó, euler
%                    *frx : nombre del sistema de origen
%                    *tox : nombre del sistemo destino
%                    *data: matriz, ó, array de celdas según type.
%                           p.e:    type=matriz, data=matriz(3*3)
%                                   type=euler, data={a1, a2, a3}
%                                   type=incrementos, data={incrementos, names} -> para un solo sistema
%                                   type=incrementos, data={incrementos1, incrementos2, names} -> para dos sistemas



function imprimir(sal, text, type, data, frx, tox)
    
    % Verificar si se ha pasado el argumento 'type'
    % Si no se proporcionó 'type' solo se imprime la cabecera
    if nargin == 2 
        type = 'none';  % Valor por defecto
        
        %ancho total del encabezado
        n=136;
        text_long = length(text);
        
        % Número de guiones a imprimir a ambos lados del texto central
        left_guiones = floor((n-text_long)/2);
        right_guiones = n - text_long - left_guiones;
        
        % Imprimir la línea con el texto centrado
        fprintf(sal,'\n\n%s\n', repmat('-', 1, n));
        fprintf(sal, '%s%s%s', repmat('-', 1, left_guiones), text, repmat('-', 1, right_guiones));
        fprintf(sal,'\n%s\n', repmat('-', 1, n));
    end

    %matriz de rotación en el fichero de salida
    if nargin == 4 && strcmp(type, 'matriz')
        fprintf(sal,'\n\n  %s\n\n', text);
        [f,c] = size(data);
        
        for i = 1:f
            for j = 1:c
                fprintf(sal, '%18.10f ', data(i,j));  % Imprimir cada valor de la matriz
            end
            fprintf(sal, '\n');  % Salto de línea después de cada fila para que quede en formato de matriz
        end
    


    %ángulos de euler en el fichero de salida
    elseif nargin == 4 && strcmp(type, 'euler')
        %datos
        a1 = data{1};
        a2 = data{2};
        a3 = data{3};
        fprintf(sal,'\n\n  %s\n\n', text);
        fprintf(sal, '      a1=  %15.10f (deg)    %18.10f (gon)    %18.10f (rad)', rad2deg(a1),  rad_cent(a1), a1);
        fprintf(sal, '\n');
        fprintf(sal, '      a2=  %15.10f (deg)    %18.10f (gon)    %18.10f (rad)', rad2deg(a2),  rad_cent(a2), a2);
        fprintf(sal, '\n');
        fprintf(sal, '      a3=  %15.10f (deg)    %18.10f (gon)    %18.10f (rad)', rad2deg(a3),  rad_cent(a3), a3);
        fprintf(sal, '\n');


    %incrementos en el fichero de salida (un solo sistema) 
    elseif nargin ==4 && strcmp(type, 'incrementos')
        %datos
        increments = data{1};
        names = data{2};

        fprintf(sal,'\n  %s\n\n', text);
        
        %salida a fichero
        fprintf(sal,'  Id         x1(m)            x2(m)            x3(m)         sensor\n');
        fprintf(sal,'  --        ------           ------           ------         ------\n');
        [f,~] = size(increments);
        for i=1:f
            id = increments(i,1);
            x1 = increments(i,2);
            x2 = increments(i,3);
            x3 = increments(i,4);
            sensor = names{i};
        
            %datos de incrementos n-Frame en fichero de salida
            fprintf(sal,'%4d   %12.4f   %13.4f   %14.4f   %11s\n', id, x1, x2, x3, sensor);
        end


    %incrementos en el fichero de salida (dos sistemas)
    elseif nargin ==6 && strcmp(type, 'incrementos')
        %datos
        points_from = data{1};
        points_to = data{2};
        names = data{3};

        %salida a fichero
        fprintf(sal,'\n\n  %s\n\n', text);
        fprintf(sal,'\n           -----------Incrementos en %s----------              -----------Incrementos en %s----------\n',frx, tox);
        fprintf(sal,'            x1(m)            x2(m)            x3(m)                  x1(m)            x2(m)            x3(m)         sensor\n');
        fprintf(sal,'            ------           ------           ------                 ------           ------           ------         ------\n');
        
        [f,~] = size(points_from);
        for i=1:f

            %datos de incrementos n-Frame en fichero de salida
            x1 = points_from(i,2);
            x2 = points_from(i,3);
            x3 = points_from(i,4);
        
            %datos de incrementos b-Frame en fichero de salida
            x4 = points_to(i,2);
            x5 = points_to(i,3);
            x6 = points_to(i,4);
        
            sensor=names{i};
            fprintf(sal,'%18.4f   %13.4f   %14.4f           %12.4f    %13.4f   %14.4f   %11s\n', x1, x2, x3, x4, x5, x6, sensor);
        end


    %si type es none
    else
        % No hacer nada si type es 'none'
    end

end