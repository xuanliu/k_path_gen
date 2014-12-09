function [shortestPaths, totalCosts] =  ...
            gen_k_shortest_path(weight_matrix, src, dst, k, ...
            output_file, demand_id)
%=================================================================
%  This function is to generate k shortest paths from source node
%  to destinatin node, given the weight_matrix of the links
%  The matlab code for k-shortest path algoritem is by by Meral Sh.
%  It can be download from 
%  
%  http://www.mathworks.com/matlabcentral/
%  fileexchange/32513-k-shortest-path-yens-algorithm
%
%  By Xuan Liu 
%  Dec. 16, 2013
%=================================================================
fileID = fopen(output_file,'at');

%------Show case selected:------:
%disp(weight_matrix);
%fprintf(fileID,'The path request is from source node %d to destination node %d, with K = %d \n',src,dst, k);

%------Call kShortestPath------:
[shortestPaths, totalCosts] = kShortestPath(weight_matrix, src, dst, k);

%------Display results------:
if isempty(shortestPaths)
    fprintf(fileID,'No path available between these nodes\n\n');
else
    for i = 1: length(shortestPaths)
        fprintf(fileID,'Path # %d: %d %d : ',i, src, dst);
        %disp(shortestPaths{i});
        len = length(shortestPaths{i});
        for j = 1: len - 1
            fprintf(fileID, '%d_', shortestPaths{i}(j));
        end
        fprintf(fileID,'%d : ', shortestPaths{i}(len));
        fprintf(fileID,'x_%d_%d \n', demand_id, i);
        %fprintf(fileID,'Cost of path %d is %5.2f\n\n',i,totalCosts(i));
    end
end
fclose(fileID);


