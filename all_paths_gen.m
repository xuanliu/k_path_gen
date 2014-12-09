function [] = all_paths_gen(weight_matrix, k, output_file)
% ==================================================================
%   This function is to generate paths for all pairs of N nodes in 
%   a network. The number of pairs is C(N,2)
%
%   By Xuan Liu
%   Dec.17, 2013
% ==================================================================

% ------Get the total number of nodes in the network ---------------
% The weight_matrix is n-by-n, where n is the number of nodes in the
% network
len = length(weight_matrix);
fileID = fopen(output_file,'wt');
fprintf(fileID,'%d nodes \n\n', len);
fclose(fileID);

node_pairs = combnk(1:len,2);

for index = 1: length(node_pairs)
    src = node_pairs(index, 1);
    dst = node_pairs(index, 2);
    gen_k_shortest_path(weight_matrix, src, dst, k, output_file, index);
end



