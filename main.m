function [] = main(link_weight_csv, output_file, k)
% =============================================================
%   This is the main function that import the link weight csv 
%   file and generate a file that contains k paths for each 
%   pair of two nodes
% 
%   By Xuan Liu
%   Dec. 17, 2013
% =============================================================

weight_matrix = csvread(link_weight_csv);
all_paths_gen(weight_matrix, k, output_file)