% calculation of empirical frequency for each node, in each subject, in
% each condition

pathname = 'E:\WB-MotionQuartet\derivatives';
SUB_LIST = {'01', '03', '04', '05', '06', '07', '08', '09', '10'};
TASK = {'phy', 'amb', 'rest'};
TR = 1;

for itsu=1:size(SUB_LIST, 2)   % // Subjects 
    sub_ID = SUB_LIST{itsu};

    for itco=1:size(TASK, 2)       % // Conditions

        disp(['Working on subject ', num2str(sub_ID), ' ', TASK{itco}]);
       
        % Load data
        path_sbj = fullfile(pathname, ['sub-' sub_ID, '\func\GEC']);
        path_out = fullfile(pathname, ['sub-' sub_ID, '\func\GEC']);
        data_str = load(fullfile(path_sbj, ['sub-' sub_ID, '_' TASK{itco} '_VOICarpet_demeanDetr_filt_1.mat']));
    
        clear signal_filt Power_Areas;
    
        % Output structure
        F_diff_blocks = {};
        data = {};
        if strcmp(TASK{itco},'rest')
            n_runs = 1;
        else
            n_runs = size(data_str.temp_sig_filt, 2);
        end
        
        for k=1:n_runs   % // Runs

            if strcmp(TASK{itco},'rest')
                ts=data_str.temp_sig_filt(:, :)';
            else
                ts=squeeze(data_str.temp_sig_filt(:, k, :))';
            end
            
            clear signal_filt Power_Areas;
            
            % Number of Nodes (N), Number of Timepoint after reduction
            [N, Tmax]=size(ts);
            
            Ts = Tmax*TR;                % The time length of the scan
            freq = (0:Tmax/2-1)/Ts;      % Frequency of the scan
            nfreqs=length(freq);         % Half of the total timepoints
            disp(['  Computing f for run ', num2str(k), '/', num2str(n_runs)])

            for seed=1:N
                % At node level computing the discrete Fourier transform after the
                % zscore normalisation of the timeseries and take only the absolute
                % values
                pw = abs(fft(zscore(ts(seed, :))));
        
                % This is taking the first half of the timepoints and elevating
                % every number to the power of 2/frequency(TT/TR)
                PowSpect = pw(1:floor(Tmax/2)).^2/(Tmax/TR);
        
                % Applying gaussian filter to the Power Spectra
                Power_Areas = gaussfilt(freq, PowSpect, 0.005);
                
                % Obtaining the Brain Areas that possess the max Power
                [~, index] = max(Power_Areas); % look for index of the the maximum power
                index = squeeze(index);
                
                % Saving per subject and seed the freq value associated with the max
                % Power Area
                F_diff_blocks{1, k}(1, seed) = freq(index); % save the frequency which has highest power
            
            end
            data{1, k} = ts;
        end
        
        % Save results
        disp('  Save data_blocks + f_blocks')
        save(fullfile(path_sbj, ['sub-' sub_ID, '_trials_blocks_demeanDetr_filt_1_', TASK{itco}, '_f_diff.mat']), 'F_diff_blocks', 'data');
    
    end
end