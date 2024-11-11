% calculation of empirical frequency for each node, in each subject, in
% each condition

for i=1:length(conditions)

    for k=1:length(data.(conditions{i}).ses)

        for l=1:data.(conditions{i}).ses(k)
            ts=data.(conditions{i}).ts{l,k};
            
            clear signal_filt Power_Areas;

            for seed=1:N
                ts(seed,:)=detrend(ts(seed,:)-nanmean(ts(seed,:)));
                %signal_filt(seed,:) =filtfilt(bfilt,afilt,ts(seed,:));
            end

            %Substracting the first and last 10 timepoints
            %ts=signal_filt(:,Trim:end-Trim);

            %Number of Nodes (N), Number of Timepoint after reduction
            [N, Tmax]=size(ts);

            Ts = Tmax*TR; %The time length of the scan
            freq = (0:Tmax/2-1)/Ts;%frequency of the scan
            nfreqs=length(freq); %Half of the total timepoints

            for seed=1:N
                % At node level computing the discrete Fourier transform after the
                % zscore normalisation of the timeseries and take only the absolute
                % values
                pw = abs(fft(zscore(ts(seed,:))));

                % This is taking the first half of the timepoints and elevating
                % every number to the power of 2/frequency(TT/TR)
                PowSpect = pw(1:floor(Tmax/2)).^2/(Tmax/TR);

                % Applying gaussian filter to the Power Spectra
                Power_Areas=gaussfilt(freq,PowSpect,0.005);
                
                % Obtaining the Brain Areas that possess the max Power
                [~,index]=max(Power_Areas); % look for index of the the maximum power
                index=squeeze(index);
                
                % Saving per subject and seed the freq value associated with the max
                % Power Area
                results.(conditions{i}).F_diff{l,k}(:,seed)=freq(index); % save the frequency which has highest power
            end
            results.(conditions{i}).FCemp{l,k}=corrcoef(ts'); % put it here in case you don't run sanity check
        end
    end
    results.(conditions{i}).F_diff_avg = squeeze(mean(results.(conditions{i}).F_diff{l,k},1));
end