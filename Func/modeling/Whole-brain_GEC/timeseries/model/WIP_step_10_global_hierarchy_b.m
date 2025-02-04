clear all; clc;

% Load MODEL result (GEC)
itask = 3;     % 1: amb; 2: phy; 3:rest.

res = load(['E:\Arrow_of_time\data\res_model_tc\Allsbj_avg_GEC_model_tc.mat']);
disp(['Analysing ' res.TASKS{itask}]);

% Average GEC across subjects first
data = squeeze(mean(res.mat_gec(itask, :, :,:),2));  
driveness = sum(data, 1);
driveness = driveness';
receiveness = sum(data, 2);
hierarchiness = driveness + receiveness;
drive_rec_diff = driveness - receiveness;


% !!! Group result: avg_score = on average how many areas is a seed area
% DRIVE, FOLLOW, HIERARCHY across subjects

% save
save(['E:\Arrow_of_time\data\res_model_tc\WIP_Allsbj_avg_GEC_model_tc_' res.TASKS{itask}, '_wholebrain_HIERARCHY.mat'], 'driveness', 'receiveness', 'hierarchiness', 'drive_rec_diff');

% -----------------------


clear all

amb = load("E:\Arrow_of_time\data\res_model_tc\WIP_Allsbj_avg_GEC_model_tc_amb_wholebrain_HIERARCHY.mat");
phy = load("E:\Arrow_of_time\data\res_model_tc\WIP_Allsbj_avg_GEC_model_tc_phy_wholebrain_HIERARCHY.mat");
rest = load("E:\Arrow_of_time\data\res_model_tc\WIP_Allsbj_avg_GEC_model_tc_rest_wholebrain_HIERARCHY.mat");

diff_tasks = amb.hierarchiness - phy.hierarchiness;
% t = diff_tasks(diff_tasks(1:180) >0)
% temp = prctile(t, 90)
% 
temp = (amb.hierarchiness + phy.hierarchiness)/2;
diff_task_rest = temp - rest.hierarchiness;

save(['E:\Arrow_of_time\data\res_model_tc\WIP_Allsbj_avg_GEC_model_tc_AllTask_wholebrain_HIERARCHY.mat'], 'diff_tasks', 'diff_task_rest');








