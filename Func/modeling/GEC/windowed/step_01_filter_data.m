% This script will read nifti-time series as carpet plot 
% Apply demean + detrend + filtering operation
% Input: 1 niftis carpet  
% Output: 1 niftis carpet  
clc
clear

pathname = 'E:\WB-MotionQuartet\derivatives\';

SUB_LIST = {'01', '03', '04', '05', '06', '07', '08', '09', '10'};
TASK = 'amb';     % // Run for ambiguous and physical
TRIALS = struct;
TRIALS_FILT = struct;

butterworth = true;
n_time = 616; % Number of time points (per run)
TR = 1;

% Construct the filter
if butterworth
    Tmax = n_time+19; % This is because when we filter the time series, some 
    % time points at the end points are deleted to avoid windowing artefacts

    % Bandpass butterworth filter settings
    fnq=1/(2*TR);                  % Nyquist frequency
    flp = 0.008;                   % lowpass frequency of filter (Hz) % // 0.008 Hz
    fhi = 0.08;                    % highpass                         % // 0.08 Hz
    Wn=[flp/fnq fhi/fnq];          % butterworth bandpass non-dimensional frequency
    k=2;                           % 2nd order butterworth filter
    [bfilt, afilt]=butter(k,Wn);   % construct the filter
end


for it_sub=1:size(SUB_LIST, 2)
    
    % Load carpet 
    sub_ID = SUB_LIST{it_sub};
    path_subj = fullfile(pathname, ['sub-' sub_ID, '\func\GEC']);
    
    disp(['Loading input data for sub-' sub_ID]);
    path_tc = fullfile(path_subj, ['sub-' sub_ID '_', TASK, '_VOICarpet.nii.gz']);
    info_tc = niftiinfo(path_tc);
    data_tc = niftiread(info_tc);

    % Extract relevant information
    n_runs = size(data_tc, 1) / n_time;
    n_vox = size(data_tc, 2);
    data_tc_reshape = reshape(data_tc, n_time, n_runs, n_vox);
    new_filt_data = zeros(size(data_tc_reshape));
    
    for it_run=1:n_runs

        % Filter the data
        ts=squeeze(data_tc_reshape(:, it_run, :));
        N=size(ts, 2); % spatial scale: number of nodes 
    
        for seed=1:N
            % demean and detrend:
            ts(:, seed) = detrend(ts(:, seed) - nanmean(ts(:, seed)));
            % Filtering
            if butterworth
                signal_filt(:, seed) = filtfilt(bfilt, afilt, double(ts(:, seed)));
            else
                signal_filt = ts;
            end
        end
       new_filt_data(:, it_run, :) = signal_filt;
    end
    new_filt_data = reshape(new_filt_data, size(data_tc));

    % Save structure data
    disp(['Saving data sub-' sub_ID]);
    outputname = fullfile(path_subj, ['sub-' sub_ID '_', TASK, '_VOICarpet_demeanDetr_filt_', num2str(butterworth), '.nii.gz']);
    niftiwrite(new_filt_data, outputname, info_tc)

    clear new_filt_data data_tc signal_filt data_tc_reshape;
end
