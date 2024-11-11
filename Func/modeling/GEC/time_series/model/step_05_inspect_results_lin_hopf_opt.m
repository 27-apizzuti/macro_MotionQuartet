% Figures for the Optimisation of the Linear Hopf Model 
clear all;
clc;
close all;

pathname = 'C:\Users\apizz\Desktop\ArrowOfTime\data\res_model\output_long\';
SUB_LIST = {'01', '03', '04', '05', '06', '07', '09', '10'};
TASKS = {'phy', 'amb', 'rest'};
fits_thr = [0.4, 0.5, 0.6];

% Inspect results for each subject and condition  
perc_good_blocks = zeros(length(TASKS), length(SUB_LIST), length(fits_thr));
num_good_blocks = zeros(length(TASKS), length(SUB_LIST), length(fits_thr));

for it_th=1:length(fits_thr)
    fit_thr = fits_thr(it_th);

    for it_co=1:size(TASKS, 2)
        for it_su=1:size(SUB_LIST, 2)
    
            sub_ID = SUB_LIST{it_su};
            % Load data
            load(fullfile(pathname, ['sub-', sub_ID, '\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{it_co}, '_model.mat']));
            n_blocks = size(results.LIN_HOPF_INDIV.errorFC, 2);
            
            % Output structure
            fitting_value = zeros(1, n_blocks);
            blocks_stat = struct;
            blocks_stat.thr = fit_thr;
            disp(['Fitting threshold ', num2str(fit_thr)])
            disp(['   Analysing results for ' sub_ID, ' ', TASKS{it_co}])
            disp(['      Nr_blocks: ', num2str(n_blocks)])
            for it_blo=1:n_blocks
    
                % Average errorFC and errorCVtau
                fitting_value(1, it_blo) = (results.LIN_HOPF_INDIV.fittFC{1,it_blo} + results.LIN_HOPF_INDIV.fittCVtau{1,it_blo})/2;
                
            end
                % Remove blocks that have low fitting value
                idx = fitting_value > fit_thr;
                idx_pos = find(idx);
                n_gb = sum(idx);
                
                % Compute number of block discarded
                metr = (n_gb / n_blocks)*100;
                blocks_stat.percGoodBlocks = metr;
                blocks_stat.numGoodBlocks = [n_gb, n_blocks];
                disp(['      Percentage of good blocks: ', num2str(metr), ' (n=', num2str(n_gb), ')'])

                % Compute GEC average only considering blocks with good fitting
                GEC_avg = zeros(size(results.LIN_HOPF_INDIV.GEC{1, 1}));
                for it=1:n_gb
                    GEC_avg = GEC_avg + results.LIN_HOPF_INDIV.GEC{1, idx_pos(it)};
                end
                GEC_avg = GEC_avg / n_gb;
    
                % Add results to structure
                perc_good_blocks(it_co, it_su, it_th) = metr;
                num_good_blocks(it_co, it_su, it_th) = n_gb;
                results.LIN_HOPF_INDIV.blocksStat = blocks_stat;
                results.LIN_HOPF_INDIV.GEC_avg = GEC_avg;
    
                % Save updated data structure
                save(fullfile(pathname, ['sub-', sub_ID, '\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{it_co}, '_model_fittingThr_', num2str(fit_thr), '.mat']), 'results');
    
        end
    end
end

% Plot stats as function of threshold
idx = perc_good_blocks > 40;

figure
set(gcf, 'Position', get(0, 'Screensize'));

subplot(1, 3, 1)
t = squeeze(sum(idx(1, :, :)));
bar(t);
title(TASKS{1})
xticklabels(fits_thr)
xlabel('Fitting Threshold')
ylabel('Number of subject (blocks >  40%)')

subplot(1, 3, 2)
t = squeeze(sum(idx(2, :, :)));
bar(t);
title(TASKS{2})
xticklabels(fits_thr)
xlabel('Fitting Threshold')
ylabel('Number of subject (blocks >  40%)')

subplot(1, 3, 3)
t = squeeze(sum(idx(3, :, :)));
bar(t);
title(TASKS{3})
xticklabels(fits_thr)
xlabel('Fitting Threshold')
ylabel('Number of subject (blocks >  40%)')

saveas(gcf, fullfile(pathname, 'GEC_Blocks_Stats.jpeg'), 'jpeg');
