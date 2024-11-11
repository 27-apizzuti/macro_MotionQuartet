% This script will read nifti-time series + trials_labels + PRT_MotFlick 
% and prepare data structure per subject for computing NR
% Input: 3 niftis carpet + trials_labels + PRT_MotFlick 
% Output: struct file + nifti to check 
clc
clear

pathname = 'E:\WB-MotionQuartet\derivatives\';
SUB_LIST = {'01', '03', '04', '05', '06', '07', '09', '08', '10'};
TASK = 'phy';  % // Run for ambiguous and physical
butterworth = true;
TRIALS = struct;


for it_sub=1:size(SUB_LIST, 2)
    
    % Load carpet + trials_labels + PRT_MotFlick
    sub_ID = SUB_LIST{it_sub};
    path_subj = fullfile(pathname, ['sub-' sub_ID, '\func\GEC']);
    path_out = fullfile(pathname, ['sub-' sub_ID, '\func\GEC\blocks']);
    
    if ~exist(path_out, 'dir')
       mkdir(path_out)
    end

    disp(['Loading input data for sub-' sub_ID]);
    path_tc = fullfile(path_subj, ['sub-' sub_ID '_', TASK, '_VOICarpet_demeanDetr_filt_', num2str(butterworth), '.nii.gz']);
    % path_tc = fullfile(path_subj, ['sub-' sub_ID '_', TASK, '_VOICarpet', '.nii.gz']);

    info_tc = niftiinfo(path_tc);
    data_tc = niftiread(info_tc);
    
    % PRT Mot-Flicker
    path = fullfile(path_subj, ['sub-' sub_ID, '_', TASK, '_VOICarpet_PRT_MotFlick.nii.gz']);
    info_pro = niftiinfo(path);
    data_pro = niftiread(info_pro);
    data_pro = data_pro(:,1);
    
    % Trials label
    path = fullfile(path_subj, ['sub-' sub_ID, '_', TASK, '_VOICarpet_PRT_MotFlick_labels-trials.nii.gz']);
    info_lab = niftiinfo(path);
    data_lab = niftiread(info_lab);
    data_lab = data_lab(:,1);
   
    %%
    % -----------------------
    % Extract block
    for condition=1:2
        TRIALS_BLOCK = {};
        idx = data_pro == condition; % 1 motion condition; 2 flicker
        trials = data_lab(idx);
        trials_labels = unique(trials);
        nr_trials = length(trials_labels);
        disp(['   Number of trials for condition ' num2str(condition) ': ']);
        disp(nr_trials)
        
        for it_trial=1:nr_trials
            idx_trial = data_lab == trials_labels(it_trial);
            temp = data_tc(idx_trial, :);
            TRIALS_BLOCK{it_trial} = temp;
        end

        % Output structure
        if condition == 1
            TRIALS.motion = TRIALS_BLOCK;
        else
            TRIALS.flicker = TRIALS_BLOCK;
        end
    end
    % Save structure data
    disp(['Saving data sub-' sub_ID]);
    save(fullfile(path_out, ['sub-', sub_ID, '_trials_blocks_demeanDetr_filt_', num2str(butterworth), '_', TASK,  '.mat']), '-struct', 'TRIALS')
    % save(fullfile(path_out, ['sub-', sub_ID, '_trials_blocks_', TASK,  '.mat']), '-struct', 'TRIALS')
    clear TRIALS_BLOCK data_lab data_pro data_tc idx idx_trial;
end
