clear

basefolder = pwd;

inpath = fullfile(basefolder, 'Raw_Dataset', 'training');
outpath = fullfile(basefolder, 'Raw_Dataset', 'StandardRGBD_3d');
mkdir(outpath)

rgbpath = fullfile(inpath, 'image_2');
depthpath = fullfile(inpath, 'velodyne');
calibpath = fullfile(inpath, 'calib');
cam = 2;

addpath('utils');


%% KITTI RAW Dataset

file_mapping = containers.Map();

dirlist1 = dir(fullfile(inpath, '*'));
dirlist1 = dirlist1([dirlist1.isdir]);

display('EXTRACTING - PHASE 1');
counter = 0;

superfolder = strsplit(rgbpath,'/');
superfolder = superfolder{end-2};

filelist = dir(fullfile(rgbpath, '*.png'));

for n_frame = 1:numel(filelist)
    
    % I/O names
    [~, filename_in, ~] = fileparts(filelist(n_frame).name);
    filename_out = sprintf('%s.mat', filename_in);
    
    % Read and process rgb
    rgb = imread(fullfile(rgbpath, [filename_in '.png']));
    
    % Read and process depth (Velodyne points)
    
    fid = fopen(fullfile(depthpath, [filename_in '.bin']),'rb');
    if (fid ~= -1)
        % Save name mapping info
        file_mapping = [file_mapping; ...
            containers.Map(filename_out, [superfolder '/' filename_in])];
        
        
        depth = fread(fid,[4 inf],'single')';
        fclose(fid);
        
        % compute projection matrix velodyne->image plane
        R_cam_to_rect = eye(4);
        [P, Tr_velo_to_cam, R] = readCalibration(calibpath, n_frame, ...
            cam);
        R_cam_to_rect(1:3,1:3) = R;
        P_velo_to_img = P * R_cam_to_rect * Tr_velo_to_cam;
        
        % Save rgb-d
        save(fullfile(outpath, filename_out),  'rgb', 'depth', ...
            'P_velo_to_img', 'filename_in');
        
    end
    
end

save(fullfile(outpath, ['file_mapping_kir']), 'file_mapping');
