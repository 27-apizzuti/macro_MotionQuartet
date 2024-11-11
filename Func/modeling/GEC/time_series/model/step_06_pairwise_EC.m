% Figures for the Optimisation of the Linear Hopf Model 
clear all;
clc;
close all;

pathname = 'E:\WB-MotionQuartet\derivatives';    % !!! TO BE CHANGED
SUB_LIST = {'01', '03', '04', '05', '06', '07', '08', '09', '10'};
TASKS = {'amb', 'rest'};
n_nodes = 360;
n_subj = size(SUB_LIST, 2);

% Load structural connectivity
load("D:\Git\macro_MotionQuartet\Func\modeling\GEC\model\sc_glasser360afni.mat");
idx_sc = sc_glasser360afni > 0;
n_tot = sum(sum(idx_sc));

% Create GEC matrix with all subjects
mat_gec_1 = zeros(n_nodes, n_nodes, n_subj);
mat_gec_2 = zeros(n_nodes, n_nodes, n_subj);
avg_gec = zeros(n_subj, 2);

figure
set(gcf, 'Position', get(0, 'Screensize'));
for it_su=1:n_subj

    sub_ID = SUB_LIST{it_su};
    path_sbj = fullfile(pathname, ['sub-', sub_ID, '\func\GEC']);

    % Load data
    co_1 = load(fullfile(path_sbj, ['\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{1}, '_model.mat']));
    co_2 = load(fullfile(path_sbj, ['\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{2}, '_model.mat']));
    mat_gec_1(:,:, it_su) = co_1.results.LIN_HOPF_INDIV.GEC;
    mat_gec_2(:,:, it_su) = co_2.results.LIN_HOPF_INDIV.GEC;


    % Plot matrix
    subplot(3, 8, it_su)
    imagesc(mat_gec_1(:,:, it_su))
    title([sub_ID, ' ', TASKS{1}])
    caxis([0, 0.3])

    
    subplot(3, n_subj, it_su+n_subj)
    imagesc(mat_gec_2(:,:, it_su))
    title([sub_ID, ' ', TASKS{2}])
    caxis([0, 0.3])

    subplot(3, n_subj, it_su+(n_subj*2))
    imagesc(mat_gec_1(:,:, it_su) - mat_gec_2(:,:, it_su))
    title([sub_ID, ' ', TASKS{1} '-' TASKS{2}])
    caxis([-0.05, 0.05])

    % Compute average GEC per subject
    m1 = mat_gec_1(:,:, it_su);
    m2 = mat_gec_2(:,:, it_su);
    avg_gec(it_su, 1) = mean(mean(m1(idx_sc)));
    avg_gec(it_su, 2) = mean(mean(m2(idx_sc)));

end

sgtitle('Effective connectivity matrices')
% saveas(gcf, fullfile(pathname, ['AllSubj_GEC_', TASKS{1}, '_', TASKS{2} '.jpeg']), 'jpeg');

% // Violine plot-2 category
data = avg_gec;
categ = cat(1, repmat(convertCharsToStrings(TASKS{1}), 8, 1), repmat(convertCharsToStrings(TASKS{2}), 8, 1));
figure
violins = violinplot(data, categ, ShowMean=true);

data = [avg_gec(:, 1)', avg_gec(:, 2)'];
design = [ones(1, n_subj), ones(1, n_subj)+1];
[stats] = permutation_htest2_np(data, design, 1000, 0.05, 'ttest');
sgtitle(['Global Level of EC ', TASKS{1}, ' ', TASKS{2}, ' p ', num2str(min(stats.pvals))]);
% saveas(gcf, fullfile(pathname, ['AllSubj_GEC_', TASKS{1}, '_', TASKS{2} '_violin.jpeg']), 'jpeg');

% Output structure will hold the p-values  
mat_stats = zeros(n_nodes);
pthr = 0.05;

for i=1:n_nodes
    for j=1:n_nodes
        arr_1 = squeeze(mat_gec_1(i,j, :));
        arr_2 = squeeze(mat_gec_2(i,j, :));

        if (i ~= j) && (sc_glasser360afni(i, j) > 0)
            if isequal(arr_1, arr_2)
                 warning('X and Y are exactly equal and will return a NaN in ttest(X,Y).')
            end
                [H,P,CI,STATS] = ttest(arr_1, arr_2 , pthr, 'both');    % phy != amb
                mat_stats(i, j) = P;
               
       end

    end
end

% Plot p-value matrix
figure
subplot(1,2,1)
mat = mat_stats;
mat(mat > 0.05) = 0;
imagesc(mat)
caxis([0, 0.05])
title('uncorr p-vals')

subplot(1,2,2)
imagesc(sc_glasser360afni)
caxis([0, 1])
title('structural connectivity')

sgtitle(['uncorrected p values matrix for EC ', TASKS{1}, ' ', TASKS{2}]);
% saveas(gcf, fullfile(pathname, ['AllSubj_uncorrpvals_', TASKS{1}, '_', TASKS{2} '.jpeg']), 'jpeg');
disp(num2str(sum(mat(:) > 0)))

s = (sum(mat(:) > 0) / (n_nodes*n_nodes)) * 100;
s2 = (sum(mat(:) > 0) / (n_tot)) * 100;


%% ttest both side
% Remove zeros - come from structural connectivity
mat_flat = mat_stats(:);
idx = (mat_flat > 0 & idx_sc(:) >0);
idx_pos = find(idx);
pvals = mat_flat(idx);

% Uncorrected pvalues
uncorr = (mat_flat < 0.05) & idx_sc(:) >0;
temp = sum(uncorr > 0);
disp(num2str(temp))
perc = (temp/ n_tot)*100;
disp(['For ', TASKS{1} ' and ', TASKS{2}, ' ', num2str(perc), ' percent have p val < 0.05 before FDR correction'])
uncorr_mat = reshape(uncorr, size(mat_stats));

% False Discovery Rate - Benjamini-Hochberg method
q = 0.05;
rejectedH0s = FDR_benjHoch(pvals, q);

% Initialize output
corr_mat_flat = zeros(size(mat_flat));

for it=1:size(rejectedH0s, 1)
    pos_p = rejectedH0s(it);    % index inside the vector without zeros
    id = idx_pos(pos_p);

    corr_mat_flat(id) = 1;
end

corr_mat1 = reshape(corr_mat_flat, size(mat_stats));

% Save corrected matrix - significant p-values
% save(fullfile(pathname, ['AllSbj_FDR_corrected_both_side_ttest_', TASKS{1}, '_', TASKS{2}, '.mat']), 'uncorr_mat', 'corr_mat1', 'sc_glasser360afni');

%% Quantify number of pairwise gec survived the FDR correction
temp = sum(corr_mat1(idx_sc) > 0);
perc = (temp/ n_tot)*100;
disp(['For ', TASKS{1} ' and ', TASKS{2}, ' ', num2str(perc), ' percent of initially optimazed entries survided FDR correction'])