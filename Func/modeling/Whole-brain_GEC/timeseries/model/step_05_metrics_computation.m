clear all;
clc;
close all;

pathname = 'E:\Arrow_of_time\data';


respath = 'E:\Arrow_of_time\data\res_model_tc';
if ~exist(respath, 'dir')
   mkdir(respath)
end

SUB_LIST = {'01', '03', '04', '05', '06', '07', '08', '09', '10'};
TASKS = {'amb', 'phy', 'rest'};
n_nodes = 360;
n_subj = size(SUB_LIST, 2);

mat_gec = zeros(3, n_subj, n_nodes, n_nodes);

for it_su=1:n_subj

    sub_ID = SUB_LIST{it_su};

    % Load data
    co_1 = load(fullfile(pathname, ['sub-', sub_ID, '\tc\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{1}, '_model_avg.mat']));
    co_2 = load(fullfile(pathname, ['sub-', sub_ID, '\tc\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{2}, '_model_avg.mat']));
    co_3 = load(fullfile(pathname, ['sub-', sub_ID, '\tc\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{3}, '_model_avg.mat']));

    mat_gec(1, it_su, :, :) = co_1.results.LIN_HOPF_INDIV.GEC_avg;
    mat_gec(2, it_su,:, :) = co_2.results.LIN_HOPF_INDIV.GEC_avg;
    mat_gec(3, it_su,:, :) = co_3.results.LIN_HOPF_INDIV.GEC_avg;

end

% Save All Subjects average GEC
save(fullfile(respath, 'Allsbj_avg_GEC_model_tc.mat'), 'mat_gec', 'TASKS');

% Computing tropic levels and coherence
val=0.1; %change this value accordingly

for it_ta = 1:length(TASKS)
    for nsub=1:n_subj
        Ceff=squeeze(mat_gec(it_ta, nsub, :, :));
        ASimmetry(it_ta, nsub) = nanmean(nanmean(abs(Ceff-Ceff')));
        
        % Alternative measure of asymmetry
        EC = abs(Ceff-Ceff');
        threshold=val*nanmean(nanmean(EC));
        
        EC(EC<threshold)=0;
        assym_2(it_ta, nsub)=sum(sum(EC>0))/(size(EC,2)*size(EC,2));

        % Computing trophic coherence
        A=Ceff';
        d=sum(A)';
        delta=sum(A,2);
        u=d+delta;
        v=d-delta;
        Lambda=diag(u)-A-A';
        Lambda(1, 1)=0;
        gamma=linsolve(Lambda, v);
        gamma=gamma-min(gamma);
        hierarchicallevels(it_ta, nsub, :)=gamma';
        H=(meshgrid(gamma)-meshgrid(gamma)'-1).^2;
        F0=sum(sum((A.*H)))/sum(sum(A));
        trophiccoherence(it_ta, nsub) = 1-F0; 
        imbalance(it_ta, nsub, :) = v';
    end
end
  
%% // Asymmetry version 2
data = assym_2';
categ = cat(1, repmat(convertCharsToStrings(TASKS{1}), 9, 1), repmat(convertCharsToStrings(TASKS{2}), 9, 1), repmat(convertCharsToStrings(TASKS{3}), 9, 1));
figure
violins = violinplot(data, categ, ShowMedian=true, ShowMean=true);
title('Asymmetry')
saveas(gcf, fullfile(respath, ['AllSubj_Asym_v-02_GEC_', TASKS{1}, '_', TASKS{2}, '_', TASKS{3}, '_violin', '.jpeg']), 'jpeg');
saveas(gcf, fullfile(respath, ['AllSubj_Asym_v-02_GEC_', TASKS{1}, '_', TASKS{2}, '_', TASKS{3}, '_violin', '.svg']), 'svg');


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
categ = cat(1, repmat(convertCharsToStrings(TASKS{1}), 9, 1), repmat(convertCharsToStrings(TASKS{2}), 9, 1), repmat(convertCharsToStrings(TASKS{3}), 9, 1));
figure
violins = violinplot(data, categ, ShowMean=true);
title('Trophic Coherence')
saveas(gcf, fullfile(respath, ['AllSubj_TrophicCoherence_', TASKS{1}, '_', TASKS{2}, '_', TASKS{3}, '_violin', '.jpeg']), 'jpeg');
saveas(gcf, fullfile(respath, ['AllSubj_TrophicCoherence_', TASKS{1}, '_', TASKS{2}, '_', TASKS{3}, '_violin', '.svg']), 'svg');


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