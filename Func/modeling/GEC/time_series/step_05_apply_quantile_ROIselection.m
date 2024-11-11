clear all;
clc;

res_phy = load("E:\WB-MotionQuartet\derivatives\res\AllSubj_runs_demeanDetr_filt_1_phyNonRever.mat");

res_amb = load("E:\WB-MotionQuartet\derivatives\res\AllSubj_runs_demeanDetr_filt_1_ambNonRever.mat");

res_rest = load("E:\WB-MotionQuartet\derivatives\res\AllSubj_runs_demeanDetr_filt_1_restNonRever.mat");

resultspath = "E:\WB-MotionQuartet\derivatives\res";

% // Average subject and obtain one whole brain NR matrix
temp_rest = zeros(360);
temp_phy = zeros(360);
temp_amb = zeros(360);

% Apply quantile ROI selection
quantile_range = [0, 0.7, 0.8, 0.9, 0.95];
NR_glob = zeros(8, size(quantile_range, 2), 3); % subj x quantiles x (phy, amb, rest) 
NR_index = cell(8, size(quantile_range, 2), 3); 

for i=1:size(res_rest.NonRev_matrix, 2)
    
    % Apply quantile on subject data
    for it=1:size(quantile_range, 2)
        thr = quantile_range(it);
        
        % physical
        index=find(res_phy.NonRev_matrix{i}>quantile(res_phy.NonRev_matrix{i}, thr));      % can vary quantile, for now we are keeping all the ROIS 
        NR_glob(i, it, 1) = nanmean(res_phy.NonRev_matrix{i}(index));
        NR_index{i, it, 1} = index;
        
        % ambiguous
        index=find(res_amb.NonRev_matrix{i}>quantile(res_amb.NonRev_matrix{i}, thr));      % can vary quantile, for now we are keeping all the ROIS 
        NR_glob(i, it, 2) = nanmean(res_amb.NonRev_matrix{i}(index));
        NR_index{i, it, 2} = index;
        
        % rest
        index=find(res_rest.NonRev_matrix{i}>quantile(res_rest.NonRev_matrix{i}, thr));      % can vary quantile, for now we are keeping all the ROIS 
        NR_glob(i, it, 3) = nanmean(res_rest.NonRev_matrix{i}(index));
        NR_index{i, it, 3} = index;
    end
        
    % Prepare data average across subjects
    temp_rest = temp_rest + res_rest.NonRev_matrix{i};
    temp_phy = temp_phy + res_phy.NonRev_matrix{i};
    temp_amb = temp_amb + res_amb.NonRev_matrix{i};

 
end

save(fullfile(resultspath, 'AllSubj_NR_quantile_PHY_AMB_REST.mat'), 'NR_glob', 'NR_index');

% // Plot Average NR mean value across subjects
quantile_range = [100, 30, 20, 10, 5];
NR_glob_mean = squeeze(mean(NR_glob, 1));
NR_glob_mean = NR_glob_mean';

figure
plot(NR_glob_mean(1,:), '-o')
hold on
plot(NR_glob_mean(2,:), '-o')
hold on
plot(NR_glob_mean(3,:), '-o')
xlabel('Top % ROIs')
ylabel('Global NR')
ylim([0, 0.18]);
xticks([1:5])
xticklabels(quantile_range)
legend('PHY', 'AMB', 'REST')
title('Global NR as function of quantile ROI selection (single-subj)')
saveas(gcf, fullfile(resultspath, 'NonRev_Global_quantiles_single_subj.jpeg'), 'jpeg');

% Average NR matrices across subjects
quantile_range = [0, 0.7, 0.8, 0.9, 0.95];

phy_avg = temp_phy / 8;
amb_avg = temp_amb / 8;
rest_avg = temp_rest / 8;

NR_glob_glob = zeros(size(quantile_range, 2), 3); % subj x quantiles x (phy, amb, rest) 
NR_index_glob = cell(size(quantile_range, 2), 3); 


for it=1:size(quantile_range, 2)
    thr = quantile_range(it);
    
    % physical
    index=find(phy_avg>quantile(phy_avg, thr));      % can vary quantile, for now we are keeping all the ROIS 
    NR_glob_glob(it, 1) = nanmean(phy_avg(index));
    NR_index_glob{it, 1} = index;
    
    % ambiguous
    index=find(amb_avg>quantile(amb_avg, thr));      % can vary quantile, for now we are keeping all the ROIS 
    NR_glob_glob(it, 2) = nanmean(amb_avg(index));
    NR_index_glob{it, 2} = index;
    
    % rest
    index=find(rest_avg>quantile(rest_avg, thr));      % can vary quantile, for now we are keeping all the ROIS 
    NR_glob_glob(it, 3) = nanmean(rest_avg(index));
    NR_index_glob{it, 3} = index;

end

NR_glob_glob = NR_glob_glob';

% // Plot mean NR for each quantile
quantile_range = [100, 30, 20, 10, 5];

figure
plot(NR_glob_glob(1,:), '-o')
hold on
plot(NR_glob_glob(2,:), '-o')
hold on
plot(NR_glob_glob(3,:), '-o')
ylim([0, 0.18]);
xlabel('Top % ROIs')
ylabel('Mean NR')
xticks([1:5])
xticklabels(quantile_range)
legend('PHY', 'AMB', 'REST')
title('Global NR as function of quantile ROI selection (average)')
saveas(gcf, fullfile(resultspath, 'Mean_NonRev_quantiles_average_matr.jpeg'), 'jpeg');

% // Compute number of common nodes
N_common = zeros(size(quantile_range, 2), 3); % quantile x couple (PA - PR - AR)
val_common = cell(size(quantile_range, 2), 1); 

for it=1:size(quantile_range, 2)
    
    % physical - ambiguous
    [val, pos] = intersect(NR_index_glob{it, 1}, NR_index_glob{it, 2});  % gives common val and its position in 'a'
    N_common(it, 1) = size(val, 1);
    val_common{it} = val;

    % physical - rest 
    [val, pos] = intersect(NR_index_glob{it, 1}, NR_index_glob{it, 3});  % gives common val and its position in 'a'
    N_common(it, 2) = size(val, 1);
    
    % ambiguous - rest
    [val, pos] = intersect(NR_index_glob{it, 2}, NR_index_glob{it, 3});  % gives common val and its position in 'a'
    N_common(it, 3) = size(val, 1);

end

% // Plot number of vox that are in common between condition for each quantile
figure
plot(N_common(:, 1), '-o')
hold on
plot(N_common(:, 2), '-o')
hold on
plot(N_common(:, 3), '-o')
xlabel('Top % ROIs')
ylabel('Number of common voxels')
xticks([1:5])
xticklabels(quantile_range)
legend('PHY-AMB', 'PHY-REST', 'AMB-REST')
title('Number of common voxels')
saveas(gcf, fullfile(resultspath, 'NumVox_NonRev_quantiles_average_matr.jpeg'), 'jpeg');

% Alternative plot
N_common_perc = zeros(size(N_common));

for it=1:size(quantile_range, 2)
    norm_fact = size(NR_index_glob{it, 1}, 1);
    N_common_perc(it, :) = N_common(it, :) /norm_fact * 100;
end

% // Plot percentage of common voxels between condition for each quantile
figure
plot(N_common_perc(:, 1), '-o')
hold on
plot(N_common_perc(:, 2), '-o')
hold on
plot(N_common_perc(:, 3), '-o')
xlabel('Top % ROIs')
ylabel('Percent of common voxels')
xticks([1:5])
xticklabels(quantile_range)
legend('PHY-AMB', 'PHY-REST', 'AMB-REST')
title('Percentage of common voxels')
saveas(gcf, fullfile(resultspath, 'PercentageVox_NonRev_quantiles_average_matr.jpeg'), 'jpeg');


% // Zeroed common nodes from NR-PHY and NR-AMB for each threshold
figure
set(gcf, 'Position', get(0, 'Screensize'));

mask_quant = {};

for it=1:5

    % Binary mask
    mas = zeros(size(temp_phy));
    idx_phy = NR_index_glob{it, 1};
    mas(idx_phy) = 1;
    idx_common = val_common{it, 1};
    [val, pos] = intersect(idx_phy, idx_common);  % gives common val and its position in 'a'
    mas(idx_phy(pos)) = 0;
    mask_quant{it} = mas;

    % // Plotting here
    subplot(1,5, it)
    imagesc(mas)
    caxis([0, 1])
    title(['Top ', num2str(quantile_range(it)), ' %'])
end

sgtitle('NR entries that differ between physical and ambiguous')
saveas(gcf, fullfile(resultspath, 'Mask_NonRev_quantiles_average.jpeg'), 'jpeg');

% Save this binary mask
save(fullfile(resultspath, 'AllSubj_MASK_quantile_PHY_AMB.mat'), 'mask_quant');



