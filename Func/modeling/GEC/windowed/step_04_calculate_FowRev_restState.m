% Tenet empírico

clear 
clc;

pathname = 'E:\WB-MotionQuartet\derivatives\';
SUB_LIST = {'01', '03', '04', '05', '06', '07', '08', '09', '10'};
NSUB = size(SUB_LIST, 2);

% Parameters
Tau = 2; 
Tmax = 600; % Max number of time points to use
TR = 1;

butterworth = true; % boolean for band pass filtering the BOlD data

path_out = fullfile(pathname, 'res');
    
if ~exist(path_out, 'dir')
   mkdir(path_out)
end

if butterworth
    Tmax = Tmax+19; % This is because when we filter the time series, some 
    % time points at the end points are deleted to avoid windowing artefacts

    % Bandpass butterworth filter settings
    fnq=1/(2*TR);                  % Nyquist frequency
    flp = 0.008;                   % lowpass frequency of filter (Hz)
    fhi = 0.08;                    % highpass
    Wn=[flp/fnq fhi/fnq];          % butterworth bandpass non-dimensional frequency
    k=2;                           % 2nd order butterworth filter
    [bfilt, afilt]=butter(k,Wn);   % construct the filter
end

%%
NonRev=zeros(NSUB,1); 
NonRev_matrix = {};
for sub=1:NSUB

    sub_ID = SUB_LIST{sub};
    path_sbj = fullfile(pathname, ['sub-' sub_ID, '\func\GEC\']);
    
    % Load resting state time course
    path_tc = fullfile(path_sbj, ['sub-' sub_ID '_rest_VOICarpet.nii.gz']);
    info_tc = niftiinfo(path_tc);
    data_tc = niftiread(info_tc);
    ts = data_tc';
    
    N=size(ts,1); % spatial scale 

    ts = ts(:, 1:min(Tmax, size(ts,2)));

    for seed=1:N
        % demean and detrend:
        ts(seed,:) = detrend(ts(seed,:) - nanmean(ts(seed,:)));
        if butterworth
            signal_filt(seed,:) = filtfilt(bfilt, afilt, double(ts(seed,:)));
        end
    end
    
    if butterworth
        clear ts;
        ts = signal_filt(:,10:end-10);
    end
    new_filt_data = signal_filt';

    % Save as carpet fMRI data after filtering
    outputname = fullfile(path_sbj, ['sub-' sub_ID '_rest_VOICarpet_demeanDetr_filt_', num2str(butterworth), '.nii.gz']);
    niftiwrite(new_filt_data, outputname, info_tc)

    % Save time course as .mat file
    temp = ts';
    save(fullfile(path_sbj, ['sub-' sub_ID '_rest_VOICarpet_demeanDetr_filt_', num2str(butterworth), '.mat']), 'temp');


    % Compute NR
    Tm = size(ts, 2);

    FCtf = corr(ts(:,1:Tm-Tau)',ts(:,1+Tau:Tm)');
    FCtr = corr(ts(:,Tm:-1:Tau+1)',ts(:,Tm-Tau:-1:1)');
    Itauf=-0.5*log(1-FCtf.*FCtf);
    Itaur=-0.5*log(1-FCtr.*FCtr);
    Reference=((Itauf(:)-Itaur(:)).^2)';
    Reference_reshape = reshape(Reference, size(Itauf));
    NonRev_matrix{sub} = Reference_reshape;

    index=find(Reference>quantile(Reference,0.0)); 

    NonRev(sub) = nanmean(Reference(index));
   

end

% Save all subjects results
save(fullfile(path_out, ['AllSubj_restState_demeanDetr_filt_', num2str(butterworth), '_NonRever.mat']), 'NonRev', 'NonRev_matrix');

