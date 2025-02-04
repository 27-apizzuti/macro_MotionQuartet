clear all; clc;

% Load MODEL result (GEC)
itask = 1;     % 1: amb; 2: phy; 3:rest.

res = load(['E:\Arrow_of_time\data\res_model_tc\Allsbj_avg_GEC_model_tc.mat']);
disp(['Analysing ' res.TASKS{itask}]);

N_SUB = 9;
driveness = zeros(360, N_SUB);
receiveness = zeros(360, N_SUB);
hierarchiness = zeros(360, N_SUB);
drive_rec_diff = zeros(360, N_SUB);

for sub=1:N_SUB
    data = squeeze(res.mat_gec(itask, sub, :,:));  
    driveness(:, sub) = sum(data, 1);
    receiveness(:, sub) = sum(data, 2);
    hierarchiness(:, sub) = driveness(:, sub) + receiveness(:, sub);
    drive_rec_diff(:, sub) = driveness(:, sub) - receiveness(:, sub);
    
end

% !!! Group result: avg_score = on average how many areas is a seed area
% DRIVE, FOLLOW, HIERARCHY across subjects

% save
save(['E:\Arrow_of_time\data\res_model_tc\Allsbj_avg_GEC_model_tc_' res.TASKS{itask}, '_wholebrain_HIERARCHY.mat'], 'driveness', 'receiveness', 'hierarchiness', 'drive_rec_diff');

% -----------------------


clear all

amb = load("E:\Arrow_of_time\data\res_model_tc\Allsbj_avg_GEC_model_tc_amb_wholebrain_HIERARCHY.mat");
phy = load("E:\Arrow_of_time\data\res_model_tc\Allsbj_avg_GEC_model_tc_phy_wholebrain_HIERARCHY.mat");
rest = load("E:\Arrow_of_time\data\res_model_tc\Allsbj_avg_GEC_model_tc_rest_wholebrain_HIERARCHY.mat");

diff_tasks = amb.hierarchiness - phy.hierarchiness;
diff_tasks = mean(diff_tasks, 2);
temp = (amb.hierarchiness + phy.hierarchiness)/2;
diff_task_rest = temp - rest.hierarchiness;
diff_task_rest = mean(diff_task_rest, 2);

save(['E:\Arrow_of_time\data\res_model_tc\Allsbj_avg_GEC_model_tc_AllTask_wholebrain_HIERARCHY.mat'], 'diff_tasks', 'diff_task_rest');








