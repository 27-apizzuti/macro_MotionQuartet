% Tenet empírico
% Compute NR per ROI per subject 

clear all;
clc;

pathname = 'E:\WB-MotionQuartet\derivatives';
SUB_LIST = {'01', '03', '04', '05', '06', '07', '08', '09', '10'};
TASK = 'rest';
Tmax = 600;            % Max number of time points to use
% ------------------------------------
% Parameters
N_nodes = 360; 
Tau = 2; 
TR = 1;
NSUB = size(SUB_LIST, 2);

butterworth = true; 

if butterworth
    Tmax_filter = Tmax-19; % This is because when we filter the time series, some 
    % time points at the end points are deleted to avoid windowing artefacts

    % Bandpass butterworth filter settings
    fnq=1/(2*TR);                  % Nyquist frequency
    flp = 0.008;                   % lowpass frequency of filter (Hz)
    fhi = 0.08;                    % highpass
    Wn=[flp/fnq fhi/fnq];          % butterworth bandpass non-dimensional frequency
    k=2;                           % 2nd order butterworth filter
    [bfilt, afilt]=butter(k,Wn);   % construct the filter
end


% output inizialization
NonRev = zeros(NSUB, 1);
NonRev_matrix = {};

path_out = fullfile(pathname, 'res_tc_masked');
    
if ~exist(path_out, 'dir')
   mkdir(path_out)
end

for sub=1:NSUB
    sub_ID = SUB_LIST{sub};
    RES = struct;
    
    path_sbj = fullfile(pathname, ['sub-' sub_ID, '\func\VTC_MNI']);
    
    % Load time course (all runs together)
    path_tc = fullfile(path_sbj, ['sub-' sub_ID '_' TASK '_VOICarpet_masked.nii.gz']);
    info_tc = niftiinfo(path_tc);
    data_tc = niftiread(info_tc);
    n_runs = size(data_tc, 1) / Tmax;
    data_tc_runs = reshape(data_tc, [Tmax, n_runs, N_nodes]);
    data_tc_runs(isnan(data_tc_runs)) = 0;


    % Prepare output
    NR_runs = zeros(n_runs,1);
    FowRev_matrix = {};
    temp_matrix = zeros(N_nodes);    
    temp_sig_filt = zeros(size(data_tc_runs));
    temp_shifted_FC = zeros(N_nodes);

    for it=1:n_runs

        % // Extract run-time course and compute NR
        ts = squeeze(data_tc_runs(:, it, :))';
   
        for seed=1:N_nodes
            % demean and detrend:
            ts(seed, :) = detrend(ts(seed, :) - nanmean(ts(seed,:)));
            if butterworth
               signal_filt(seed, :) = filtfilt(bfilt, afilt, double(ts(seed,:)));
            end
        end
    
        if butterworth
            clear ts;
            ts = signal_filt(:,10:end-10);
        end

        temp_sig_filt(10:end-10, it, :) = ts';

        new_filt_data = signal_filt';

        % // Compute non-reversability
        Tm = size(ts, 2);
        FCtf = corr(ts(:, 1:Tm-Tau)', ts(:,1+Tau:Tm)');
        disp(sum(isnan(FCtf(86, :))))
        FCtr = corr(ts(:,Tm:-1:Tau+1)', ts(:,Tm-Tau:-1:1)');
        Itauf=-0.5*log(1- FCtf.*FCtf);
        Itaur=-0.5*log(1- FCtr.*FCtr);
        Reference=((Itauf(:)-Itaur(:)).^2)';

        % // Reshape reference (non-reversability) to matrix
        Reference_reshape = reshape(Reference, size(Itauf));
        FowRev_matrix{it} = Reference_reshape;
        temp_matrix = temp_matrix + Reference_reshape;

        % // Summarize results per subject
        index=find(Reference>quantile(Reference, 0.0));      % can vary quantile, for now we are keeping all the ROIS 
        NR_runs(it) = nanmean(Reference(index));

        % // Storing the shifted FC matrix
        temp_shifted_FC = temp_shifted_FC + FCtf;

    end

    % Save time course as .mat file
    save(fullfile(path_sbj, ['sub-' sub_ID '_' TASK '_VOICarpet_demeanDetr_filt_', num2str(butterworth), '.mat']), 'temp_sig_filt');

    % Save as carpet fMRI data after filtering
    temp_sig_filt = reshape(temp_sig_filt, size(data_tc));
    outputname = fullfile(path_sbj, ['sub-' sub_ID '_' TASK '_VOICarpet_demeanDetr_filt_', num2str(butterworth), '.nii.gz']);
    niftiwrite(temp_sig_filt, outputname, info_tc)
    
    % Save single subject results
    save(fullfile(path_sbj, ['sub-', sub_ID, '_' TASK ' _runs_demeanDetr_filt_', num2str(butterworth), '_', TASK,  'NonRever.mat']), 'FowRev_matrix');
    
    % Summarize single subject results
    NonRev(sub) = mean(NR_runs);
    NonRev_matrix{sub} = temp_matrix/n_runs;
    Shifted_FC{sub} = temp_shifted_FC/n_runs;


end

% Save all subjects results
save(fullfile(path_out, ['AllSubj_runs_demeanDetr_filt_', num2str(butterworth), '_', TASK,  'NonRever.mat']), 'NonRev', 'NonRev_matrix', 'Shifted_FC'); 