clear
% basefolder = 'E:\Marco\Documenti\Dropbox (too large)\Photospace\Datasets_small';
basefolder = pwd;

inpath = fullfile(basefolder, 'Raw_Dataset', 'StandardRGBD_3d');
outpath = fullfile(basefolder, 'training');
mkdir(outpath)


rgb_outpath = fullfile(outpath, 'rgb');
depth_outpath = fullfile(outpath, 'image_2');

mkdir(rgb_outpath)
mkdir(depth_outpath)

addpath('kdtree');
addpath('utils');
addpath('matlab');

addpath(genpath('vlfeat-0.9.21'));
%% KITTI RAW Dataset

% Load file name mapping (might come in handy...)
load(fullfile(inpath, ['file_mapping_kir' ]));

filelist = dir(fullfile(inpath, '*.mat'));

display('Kitti_Dataset');

counter = 0;
for i = counter+1:numel(filelist)
    
    counter = counter+1;
    cam = 2;
    
    % I/O names
    [~, filename_in, ~] = fileparts(filelist(i).name);
    %filename_out = sprintf('%06s.mat', counter);
    
    % Load depth and rgb
    load(fullfile(inpath, filelist(i).name));
    
    velo_points = depth;
    P = P_velo_to_img;
    
    % load velodyne points
    % remove every 5th point for display speed
    velo_points = velo_points(1:5:end,:);
    
    
    % remove all points behind image plane (approximation
    idx = velo_points(:,1)<5;
    velo_points(idx,:) = [];
    
    %velo_points_2D = project(velo(:,1:3), P_velo_to_img);
    velo_points_2D = projectToImage(velo_points(:, 1:3)',  P)';
    % project to image plane (exclude luminance)
    to_keep = velo_points_2D(:,1)>=1 & ...
        velo_points_2D(:,1)<=size(rgb,2) & velo_points_2D(:,2)>=1 & ...
        velo_points_2D(:,2)<=size(rgb,1);
    velo_points_2D = round(velo_points_2D(to_keep,:));
    velo_points = round(velo_points(to_keep,:));
    
    % Create model
    kdtree = vl_kdtreebuild(velo_points_2D');
    % Appiattish
    [y, x] = find(true(size(rgb(:,:,1))));
    [index, distance] = vl_kdtreequery(kdtree, velo_points_2D', [x y]') ;
    depth = velo_points(index,1);
    depth = reshape(depth, size(rgb,1),size(rgb,2));
    depth = uint8(depth);
    
    % "x,y and y are stored in metric (m) Velodyne coordinates."
    
    % Save rgb-d
    imwrite(rgb, fullfile(rgb_outpath, [filename_in '.png'] ))
    imwrite(depth, fullfile(depth_outpath,[filename_in '.png']))
    
    
end

