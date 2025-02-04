% Tenet empírico
% Compute NR per ROI per subject 

clear all;
clc;

pathname = 'E:\Arrow_of_time\data';
SUB_LIST = {'01', '03', '04', '05', '06', '07', '08', '09', '10'};

TASK = {'rest', 'phy', 'amb'};
Tmax = [600, 616, 616];            % Max number of time points to use
% -------------------------------------------------------------------------
% Parameters
N_nodes = 360; 
NSUB = size(SUB_LIST, 2);

% output inizialization
path_out = fullfile(pathname, 'res_tc');
    
if ~exist(path_out, 'dir')
   mkdir(path_out)
end

AC_task = {};

for itask=1:size(TASK, 2)

    AC = zeros(21, NSUB);
    
    for sub=1:NSUB
        sub_ID = SUB_LIST{sub};
        RES = struct;
        
        path_sbj = fullfile(pathname, ['sub-' sub_ID, '\NIFTI_MNI']);
        path_sbj_out = fullfile(pathname, ['sub-' sub_ID, '\tc']);
    
        if ~exist(path_sbj_out, 'dir')
            mkdir(path_sbj_out)
        end
        
        % Load time course (all runs together)
        path_tc = fullfile(path_sbj, ['sub-' sub_ID '_' TASK{itask} '_VOICarpet.nii.gz']);
        info_tc = niftiinfo(path_tc);
        data_tc = niftiread(info_tc);
        n_runs = size(data_tc, 1) / Tmax(itask);
        data_tc_runs = reshape(data_tc, [Tmax(itask), n_runs, N_nodes]);
    
        AC_nodes = zeros(N_nodes, 21, n_runs);
    
        for it=1:n_runs
    
            % // Extract run-time course and compute NR
            ts = squeeze(data_tc_runs(:, it, :))';
            
            for itroi=1:N_nodes
                AC_nodes(itroi, :, it) = autocorr(ts(itroi, :));
            end
         
        end
        
       

        if n_runs > 1
            AC(:, sub) = mean(mean(AC_nodes, 3), 1);
        else
             AC(:, sub) = mean(AC_nodes, 1);
        end
    end

    % Assign to the output variable 
    AC_task{itask} = AC;
end

% Plotting

figure
subplot(1,3,1)
plot(AC_task{1}, Color='black')
hold on
plot(mean(AC_task{1}, 2), LineWidth=3, Color='black')
xticks([1:1:21])
xticklabels([0:1:21])
xline(3, Color='red', LineStyle='--')
yline(0.7)
yline(0.5)
ylabel('Autocorrelation Rest', 'FontSize', 18)
xlabel('LAG (s)', 'FontSize', 18)

subplot(1,3,2)
plot(AC_task{2}, Color='black')
hold on
plot(mean(AC_task{2}, 2), LineWidth=3, Color='black')

xticks([1:1:21])
xticklabels([0:1:21])
xline(3, Color='red', LineStyle='--')
yline(0.7)
yline(0.5)
ylabel('Autocorrelation Physical', 'FontSize', 18)
xlabel('LAG (s)', 'FontSize', 18)

subplot(1,3,3)
plot(AC_task{3}, Color='black')
hold on
plot(mean(AC_task{3}, 2), LineWidth=3, Color='black')

xticks([1:1:21])
xticklabels([0:1:21])
xline(3, Color='red', LineStyle='--')
yline(0.7)
yline(0.5)
ylabel('Autocorrelation Ambiguous', 'FontSize', 18)
xlabel('LAG (s)', 'FontSize', 18)

% legend({'Thin lines = single subject, Thick line = group average'}, 'FontSize', 20)

sgtitle('Autocorrelation Function for fMRI time series', 'FontSize', 25)