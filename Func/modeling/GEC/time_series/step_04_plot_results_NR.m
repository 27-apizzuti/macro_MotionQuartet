clear all;
clc;

res_phy = load("E:\WB-MotionQuartet\derivatives\res_tc_masked\AllSubj_runs_demeanDetr_filt_1_phyNonRever.mat");

res_amb = load("E:\WB-MotionQuartet\derivatives\res_tc_masked\AllSubj_runs_demeanDetr_filt_1_ambNonRever.mat");

res_rest = load("E:\WB-MotionQuartet\derivatives\res_tc_masked\AllSubj_runs_demeanDetr_filt_1_restNonRever.mat");

resultspath = "E:\WB-MotionQuartet\derivatives\res_tc_masked";

% // Bar plot
X = {"PHY", "AMB", "REST"}';
Y = [mean(res_phy.NonRev), mean(res_amb.NonRev), mean(res_rest.NonRev)];
data = [res_phy.NonRev, res_amb.NonRev, res_rest.NonRev];

figure
bar(Y)
xticklabels(X)
legend('All ROIs')
sgtitle('Global Level of Non Reversability')
saveas(gcf, fullfile(resultspath, 'Barplot_NonRev_Global.jpeg'), 'jpeg');

% // Violine plot-3 category
categ = cat(1, repmat("PHY", 8, 1), repmat("AMB", 8, 1), repmat("REST", 8, 1));
figure
violins = violinplot(data, categ, ShowMean=true);
sgtitle('Global Level of Non Reversability')
saveas(gcf, fullfile(resultspath, 'Violinplot_NonRev_Global.jpeg'), 'jpeg');

% // Line plot per subject
diff = [res_phy.NonRev, res_amb.NonRev, res_rest.NonRev];
x_ax = [1, 2, 3];
figure
plot(x_ax, diff', '-o')
xticks(x_ax)
sgtitle('Global Level of Non Reversability')
xticklabels(X)
legend;
saveas(gcf, fullfile(resultspath, 'LinePlot_NonRev_Global.jpeg'), 'jpeg');

% // Plot single subject NR Matrix
temp = zeros(360);
temp_phy = zeros(360);
temp_amb = zeros(360);

for i=1:size(res_rest.NonRev_matrix, 2)
    
    temp = temp + res_rest.NonRev_matrix{i};
    temp_phy = temp_phy + res_phy.NonRev_matrix{i};
    temp_amb = temp_amb + res_amb.NonRev_matrix{i};
    
    % // Plot deactivated //
    % figure
    % subplot(1,3,1)
    % imagesc(res_amb.NonRev_matrix{i})
    % caxis([0, 0.05])
    % title(['AMB mean ' num2str(mean(res_amb.NonRev_matrix{i}(:))) ' = ' num2str(res_amb.NonRev(i)) ])
    % subplot(1,3,2)
    % imagesc(res_phy.NonRev_matrix{i})
    % caxis([0, 0.05])
    % title(['PHY mean ' num2str(mean(res_phy.NonRev_matrix{i}(:))) ' = ' num2str(res_phy.NonRev(i)) ])
    % subplot(1,3,3)
    % imagesc(res_rest.NonRev_matrix{i})
    % caxis([0, 0.05])
    % title(['REST mean ' num2str(mean(res_rest.NonRev_matrix{i}(:))) ' = ' num2str(res_rest.NonRev(i))])
    % 
end

rest_avg = temp / 9;
phy_avg = temp_phy / 9;
amb_avg = temp_amb / 9;

% // Plot NR matrix averaged across subjects
figure
set(gcf, 'Position', get(0, 'Screensize'));

subplot(1,3,1)
imagesc(amb_avg)
caxis([0, 0.05])
title('AMB')
colorbar;
subplot(1,3,2)
imagesc(phy_avg)
caxis([0, 0.05])
title('PHY')
colorbar;
subplot(1,3,3)
imagesc(rest_avg)
caxis([0, 0.05])
title('REST')
colorbar;
sgtitle('Whole brain non-reversibility')
saveas(gcf, fullfile(resultspath, 'Matrix_NonRev_Global.jpeg'), 'jpeg');
