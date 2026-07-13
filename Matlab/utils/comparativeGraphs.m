
%  Autor           : jrvalza
%  Función         : comparativeGraphs
%  Descripción     : permite obtener gráficas comparativas de series de datos
%  Datos de entrada: *time: array de serie de tiempo (n*1)
%                    *data: array de matrices de series de datos (m*n). m: series de datos n:numero de registros
%                    *numRTKrec: array de serie de dato de número de receptores
%                    *numPlots: número de subgráficos a generar
%                    *titles: cell array de títulos de los subgráficos a generar
%                    *yLabels: cell array de etiquetas de series de datos
%                    *leg: cell array con la legenda de las series de datos
%                    *plotnumRTKrec: gráficar número de receptores GNSS. si=true, no:false
%                    *accPlot: gráficar aceleraciones. si=true, no:false
%                    *minY, maxY: rango de valores para el eje Y
%  Datos de salida : genera una figura con subplots comparativos para cada serie de datos
%  Ejemplo         : comparativeGraphs(time, data, numRTKrec, numPlots, titles, yLabels, leg, plotnumRTKrec, accPlot)
%                         p.e:
%                             data = [[1,2,3,4;5,6,7,8;9,10,11,12]; [12,11,10,9;8,7,6,5;4,3,2,1]]
%                             numPlots = size(data, 1)/2 = 3
%                             camparativa 1: [1,2,3,4]    vs [12,11,10,9]
%                             comparativa 2: [5,6,7,8]    vs [8,7,6,5]
%                             comparativa 3: [9,10,11,12] vs [4,3,2,1]

function comparativeGraphs(time, data, numRTKrec, numPlots, titles, yLabels, leg, plotnumRTKrec, accPlot, minY, maxY)

    %generación de gráfico
    figure;
    
    % Iterar sobre cada fila de datos
    for i = 1:numPlots
        subplot(numPlots, 1, i);
    
        %Gráficos del eje izquierdo
        %serie de datos 1
        plot(time, data(i,:), 'b-', 'LineWidth', 1);
        hold on;
        ylabel(yLabels{i});
        
        %serie de datos2
        if accPlot
            plot(time, data(i+numPlots,:), 'r--', 'LineWidth', 1);
            ylim([minY maxY]);
        else
            scatter(time, data(i+numPlots,:), 'filled', 'r', 'SizeData', 2);
        end
        
        %Gráfico del eje derecho
        %serie de datos 3
        if plotnumRTKrec
            yyaxis right;
            plot(time, numRTKrec, 'g', 'LineWidth', 1);
            ylabel('Rec');
            legendHandle = legend(leg{1}, leg{2}, leg{3});
        else
            legendHandle = legend(leg{1}, leg{2});
        end

        % Ajustar el tamaño de la fuente de la leyenda
        set(legendHandle, 'FontSize', 6);
        legendHandle.Location = 'northwest'; % Posición superior izquierda
        
        %Título, etiquetas y leyenda
        title(titles{i});
        xlabel('Time in hours');
        grid on;
    end
end
