clear all;
clc;
close all;

pathname = 'E:\WB-MotionQuartet\derivatives';    % !!! TO BE CHANGED

respath = 'E:\WB-MotionQuartet\derivatives\GEC';
if ~exist(respath, 'dir')
   mkdir(respath)
end

SUB_LIST = {'01', '03', '04', '05', '06', '07', '08','09', '10'};
TASKS = {'amb', 'phy', 'rest'};
fits_thr = 0.4;
n_nodes = 360;
n_subj = size(SUB_LIST, 2);

mat_gec = zeros(3, n_subj, n_nodes, n_nodes);

for it_su=1:n_subj

    sub_ID = SUB_LIST{it_su};

    % % Load data
    path_sbj = fullfile(pathname, ['sub-', sub_ID, '\func\GEC']);

    co_1 = load(fullfile(path_sbj, ['\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{1}, '_model.mat']));
    co_2 = load(fullfile(path_sbj, ['\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{2}, '_model.mat']));
    co_3 = load(fullfile(path_sbj, ['\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{3}, '_model.mat']));

    % co_3 = load(fullfile(pathname, ['sub-', sub_ID, '\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{3}, '_model_v-02.mat']));

    % co_1 = load(fullfile(pathname, ['sub-', sub_ID, '\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{1}, '_model_fittingThr_', num2str(fits_thr), '.mat']));
    % co_2 = load(fullfile(pathname, ['sub-', sub_ID, '\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{2}, '_model_fittingThr_', num2str(fits_thr), '.mat']));
    % co_3 = load(fullfile(pathname, ['sub-', sub_ID, '\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{3}, '_model_fittingThr_', num2str(fits_thr), '.mat']));
    % co_3 = load(fullfile(pathname2, ['sub-', sub_ID, '\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{3}, '_model_v-02.mat']));


    mat_gec(1, it_su, :, :) = co_1.results.LIN_HOPF_INDIV.GEC;
    mat_gec(2, it_su,:, :) = co_2.results.LIN_HOPF_INDIV.GEC;
    mat_gec(3, it_su,:, :) = co_3.results.LIN_HOPF_INDIV.GEC;

    % disp(sum(sum(isnan(co_3.results.LIN_HOPF_INDIV.GEC_avg))))

end

val=0.1; %change this value accordingly

% Computing tropic levels and coherence
for it_ta = 1:length(TASKS)
    for nsub=1:n_subj
        Ceff=squeeze(mat_gec(it_ta, nsub, :, :));
        ASimmetry(it_ta, nsub) = nanmean(nanmean(abs(Ceff-Ceff')));
        
        % Alternative measure of asymmetry
        EC = Ceff;
        
        threshold=val*nanmean(nanmean(EC));
        
        EC(EC<threshold)=0;
        assym_2(it_ta, nsub)=sum(sum(EC>0))/(size(EC,2)*size(EC,2));
    
        A=Ceff';
        d=sum(A)';
        delta=sum(A,2);
        u=d+delta;
        v=d-delta;
        Lambda=diag(u)-A-A';
        Lambda(100, 100)=0;
        gamma=linsolve(Lambda, v);
        gamma=gamma-min(gamma);
        hierarchicallevels(it_ta, nsub, :)=gamma';
        H=(meshgrid(gamma)-meshgrid(gamma)'-1).^2;
        F0=sum(sum((A.*H)))/sum(sum(A));
        trophiccoherence(it_ta, nsub) = 1-F0; 
        imbalance(it_ta, nsub, :) = v';
    end
end
  
%% Plot results
%// Asymmetry level
data = ASimmetry';
categ = cat(1, repmat(convertCharsToStrings(TASKS{1}), 8, 1), repmat(convertCharsToStrings(TASKS{2}), 8, 1), repmat(convertCharsToStrings(TASKS{3}), 8, 1));
figure
violins = violinplot(data, categ, ShowMedian=true, ShowMean=true);
title('Asymmetry')
saveas(gcf, fullfile(pathname, ['AllSubj_AsymGEC_', TASKS{1}, '_', TASKS{2}, '_', TASKS{3}, '_violin.jpeg']), 'jpeg');

%Stats
data = [ASimmetry(1,:), ASimmetry(2,:)];
design = [ones(1, n_subj), ones(1, n_subj)+1];
[stats] = permutation_htest2_np(data, design, 1000, 0.05, 'ttest');
disp(['Asymmetry means amb: ', num2str(mean(ASimmetry(1,:))), ' vs phy: ', num2str(mean(ASimmetry(2,:))), ' pval ', num2str(min(stats.pvals))])

data = [ASimmetry(1, :), ASimmetry(3, :)];
[stats] = permutation_htest2_np(data, design, 1000, 0.05, 'ttest');
disp(['Asymmetry means amb: ', num2str(mean(ASimmetry(1,:))), ' vs rest: ', num2str(mean(ASimmetry(3,:))), ' pval ', num2str(min(stats.pvals))])

data = [ASimmetry(2, :), ASimmetry(3, :)];
[stats] = permutation_htest2_np(data, design, 1000, 0.05, 'ttest');
disp(['Asymmetry means phy: ', num2str(mean(ASimmetry(2,:))), ' vs rest: ', num2str(mean(ASimmetry(3,:))), ' pval ', num2str(min(stats.pvals))])
% 
%% // Asymmetry version 2
data = assym_2';
categ = cat(1, repmat(convertCharsToStrings(TASKS{1}), 8, 1), repmat(convertCharsToStrings(TASKS{2}), 8, 1), repmat(convertCharsToStrings(TASKS{3}), 8, 1));
figure
violins = violinplot(data, categ, ShowMedian=true, ShowMean=true);
title('Asymmetry')
saveas(gcf, fullfile(respath, ['AllSubj_Asym_v-02_GEC_', TASKS{1}, '_', TASKS{2}, '_', TASKS{3}, '_violin_thr_', num2str(fits_thr), '.jpeg']), 'jpeg');

% Stats
data = [assym_2(1,:), assym_2(2,:)];
design = [ones(1, n_subj), ones(1, n_subj)+1];
[stats] = permutation_htest2_np(data, design, 1000, 0.05, 'ttest');
disp(['Asymmetry means amb: ', num2str(mean(assym_2(1,:))), ' vs phy: ', num2str(mean(assym_2(2,:))), ' pval ', num2str(min(stats.pvals))])

data = [assym_2(1, :), assym_2(3, :)];
[stats] = permutation_htest2_np(data, design, 1000, 0.05, 'ttest');
disp(['Asymmetry means amb: ', num2str(mean(assym_2(1,:))), ' vs rest: ', num2str(mean(assym_2(3,:))), ' pval ', num2str(min(stats.pvals))])

data = [assym_2(2, :), assym_2(3, :)];
[stats] = permutation_htest2_np(data, design, 1000, 0.05, 'ttest');
disp(['Asymmetry means phy: ', num2str(mean(assym_2(2,:))), ' vs rest: ', num2str(mean(assym_2(3,:))), ' pval ', num2str(min(stats.pvals))])

%% // Trophic coherence
data = trophiccoherence';
categ = cat(1, repmat(convertCharsToStrings(TASKS{1}), 8, 1), repmat(convertCharsToStrings(TASKS{2}), 8, 1), repmat(convertCharsToStrings(TASKS{3}), 8, 1));
figure
violins = violinplot(data, categ, ShowMean=true);
title('Trophic Coherence')
saveas(gcf, fullfile(respath, ['AllSubj_TrophicCoherence_', TASKS{1}, '_', TASKS{2}, '_', TASKS{3}, '_violin_thr_', num2str(fits_thr), '.jpeg']), 'jpeg');

% Stats
data = [trophiccoherence(1,:), trophiccoherence(2,:)];
design = [ones(1, n_subj), ones(1, n_subj)+1];
[stats] = permutation_htest2_np(data, design, 1000, 0.05, 'ttest');
disp(['Trophic Coherence means amb: ', num2str(nanmean(trophiccoherence(1,:))), ' vs phy: ', num2str(nanmean(trophiccoherence(2,:))), ' pval ', num2str(min(stats.pvals))])

data = [trophiccoherence(1, :), trophiccoherence(3, :)];
[stats] = permutation_htest2_np(data, design, 1000, 0.05, 'ttest');
disp(['Trophic Coherence means amb: ', num2str(nanmean(trophiccoherence(1,:))), ' vs rest: ', num2str(nanmean(trophiccoherence(3,:))), ' pval ', num2str(min(stats.pvals))])

data = [trophiccoherence(2, :), trophiccoherence(3, :)];
[stats] = permutation_htest2_np(data, design, 1000, 0.05, 'ttest');
disp(['Trophic Coherence means phy: ', num2str(nanmean(trophiccoherence(2,:))), ' vs rest: ', num2str(nanmean(trophiccoherence(3,:))), ' pval ', num2str(min(stats.pvals))])

%% // Hierarchical levels 
% Output structure will hold the p-values  
hl_amb = mean(squeeze(hierarchicallevels(1, :, :)));
hl_phy = mean(squeeze(hierarchicallevels(2, :, :)));
hl_res = mean(squeeze(hierarchicallevels(3, :, :)));

figure
set(gcf, 'Position', get(0, 'Screensize'));
plot(hl_phy)
hold on
plot(hl_amb)
hold on
plot(hl_res)
legend('PHY', 'AMB', 'REST')
ylabel('Hierarchical levels')
xlabel('Nodes')
title('Hierarchical levels')
% saveas(gcf, fullfile(pathname, ['AllSubj_HierarchicalLevels_', TASKS{1}, '_', TASKS{2}, '_', TASKS{3}, '.jpeg']), 'jpeg');
% 
% %% Imbalance
% ib_amb = mean(squeeze(imbalance(1, :, :)));
% ib_phy = mean(squeeze(imbalance(2, :, :)));
% ib_rest = mean(squeeze(imbalance(3, :, :)));
% 
% figure
% set(gcf, 'Position', get(0, 'Screensize'));
% plot(ib_phy)
% hold on
% plot(ib_amb)
% hold on
% plot(ib_rest)
% legend('PHY', 'AMB', 'REST')
% ylabel('Imbalance')
% xlabel('Nodes')
% title('Imbalance')
% saveas(gcf, fullfile(pathname, ['AllSubj_Imbalance_', TASKS{1}, '_', TASKS{2}, '_', TASKS{3}, '.jpeg']), 'jpeg');
% 
%% Test significance // This is not optimized yet
% Output structure will hold the p-values  
mat_stats = zeros(n_nodes, 1);
pthr = 0.05;

for j=1:n_nodes
    arr_1 = squeeze(hierarchicallevels(1, :, j));
    arr_2 = squeeze(hierarchicallevels(3, :, j));    

    if isequal(arr_1, arr_2)
         warning('X and Y are exactly equal and will return a NaN in ttest(X,Y).')
    end

    [H,P,CI,STATS] = ttest(arr_1, arr_2 , pthr, 'both');    % phy != amb
    mat_stats(j, 1) = P;

end

% False Discovery Rate - Benjamini-Hochberg method
q = 0.05;
rejectedH0s = FDR_benjHoch(mat_stats, q);

%% // Compute hierarchical jumps between conditions
% Rank hierarchical level index
[B_amb, I_amb] = sort(hl_amb);
[B_phy, I_phy] = sort(hl_phy);
[B_res, I_res] = sort(hl_res);

% Jumps
phy_to_amb = I_phy-I_amb;

% Visualize nodes that changes their hierarchical levels the most
quantile_range = [0.3, 0.5, 0.7, 0.8, 0.9, 0.95];
colors = {'red', 'blue', 'green', 'black', 'yellow', 'pink'};

figure
set(gcf, 'Position', get(0, 'Screensize'));
subplot(1,2,1)
bar(phy_to_amb)
xlabel('Nodes')
ylabel('Changes in hierarchy')
title('Physical to Ambiguous')
hold on 
subplot(1,2,2)
[B, I] = sort(phy_to_amb);
bar(B)
xlabel('Nodes')
ylabel('Changes in hierarchy')
title('Physical to Ambiguous')

% Find indices of nodes that jump the hierarchy
IDX_nodes = {};

for it=1:length(quantile_range)
    temp = quantile(phy_to_amb, quantile_range(it));    % I can plot the quantile line
    index=find(abs(phy_to_amb) > temp);   
    IDX_nodes{it, 1} = index;
    IDX_nodes{it, 2} = phy_to_amb(index);

    subplot(1,2,1)
    yline(temp, colors{it})
    yline(-temp, colors{it})
    hold on
    subplot(1,2,2)
    yline(temp, colors{it})
    yline(-temp, colors{it})
    hold on
end

saveas(gcf, fullfile(respath, ['AllSubj_HierarchyChangesQuantiles_', TASKS{1}, '_', TASKS{2}, '_thr_', num2str(fits_thr), '.jpeg']), 'jpeg');
% 
%% Renders
n_levels = size(IDX_nodes, 1);
n_nodes = 360;
legend_jumps = {'70', '50', '30', '20', '10', '5'};
for it=1:n_levels
    mask = zeros(1, n_nodes);
    % mask(IDX_nodes{it,1}) = sign(IDX_nodes{it, 2})*10;   % Construct binary mask to visualize
    mask(IDX_nodes{it,1}) = IDX_nodes{it, 2};   % Construct binary mask to visualize

    rangemin = min(mask);
    rangemax = max(mask);
    inv = 0;
    clmap = 'RdYlBu10';
    surfacetype = 2;

    rendersurface_glasser360(mask', rangemin, rangemax, inv, clmap,surfacetype)
    % sgtitle(['Hierarchical jumps top ', legend_jumps{it}])
    saveas(gcf, fullfile(respath, ['NonRev_map_quantile_', num2str(it), '_max_', num2str(rangemax), '_thr_', num2str(fits_thr), '.jpeg']), 'jpeg');

end
