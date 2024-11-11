% // Apply permutation test to check for significance
% One sample t-test 
clear all;
clc;

% Load data
res_phy = load("C:\Users\apizz\Desktop\ArrowOfTime\data\res\AllSubj_trials_blocks_demeanDetr_filt_1_phyNonRever.mat");
res_amb = load("C:\Users\apizz\Desktop\ArrowOfTime\data\res\AllSubj_trials_blocks_demeanDetr_filt_1_ambNonRever.mat");
resultspath = "C:\Users\apizz\Desktop\ArrowOfTime\data\res\";

NR_quant = load(fullfile(resultspath, 'AllSubj_NR_quantile_PHY_AMB_REST.mat'));

% Construct vector: NR[....> subjects_phy][...> subjects_amb]
n_sub = size(res_phy.NonRev, 1);
niter = 10000;
htest = 'ttest';
pthr = 0.001;
n_sub = size(res_phy.NonRev, 1);

data = [res_phy.NonRev', res_amb.NonRev'];
design = [ones(1, n_sub), ones(1, n_sub)+1];
[stats] = permutation_htest2_np(data, design, niter, pthr, htest);

% Load data with different quantile threshold
quantile_range = [100, 30, 20, 10, 5];
design = [ones(1, n_sub), ones(1, n_sub)+1];

figure
set(gcf, 'Position', get(0, 'Screensize'));

for it=1:5
    temp1 = NR_quant.NR_glob(:, it, 1);
    temp2 = NR_quant.NR_glob(:, it, 2);
    data = [temp1', temp2'];
    [stats] = permutation_htest2_np(data, design, niter, pthr, htest);
    disp(['Top ', num2str(quantile_range(it)), ' percent of nodes' ]);
    disp(stats.pvals)
    p = min(stats.pvals);
    
    % // Violine plot-2 category
    data = [temp1'; temp2'];
    categ = cat(1, repmat("PHY", 8, 1), repmat("AMB", 8, 1));
    subplot(1, 5, it)
    violins = violinplot(data, categ, ShowMean=true);
    ylim([0, 0.35])
    title(['top ', num2str(quantile_range(it)), '% p=', num2str(p)]);
    sgtitle('Global Level of Non Reversability');
   
end
saveas(gcf, fullfile(resultspath, 'AllSubj_NR_permTest.jpeg'), 'jpeg');
