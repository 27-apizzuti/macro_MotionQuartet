clear all; clc;

% Load INSIDEOUT results

res_amb = load("E:\WB-MotionQuartet\derivatives\res_tc\AllSubj_runs_demeanDetr_filt_1_ambNonRever.mat");

N_SUB = 9;
seed_MT_complex = [2, 23, 156, 157];
target = 86;    % Area 46

for sub=1:N_SUB
    data = res_amb.Shifted_FC{1, sub};  
    
    seed_driving = data(:, [seed_MT_complex, seed_MT_complex+180]);
    seed_following = data([seed_MT_complex, seed_MT_complex+180], :);
    
    seed_driving_mean = nanmean(seed_driving, 2);
    seed_following_mean = nanmean(seed_following, 1);
    
    driving_following(:, sub) = seed_driving_mean - seed_following_mean';
    driving_following_one_roi(:, sub) = nanmean(seed_driving_mean([target, target+180])) - nanmean(seed_following_mean([target, target+180])');
end

% ---------------------------------
% Is MT+ complex driving area 86?
tagert_stat = driving_following([target, target+180], :);
idx = sum(sum(tagert_stat > 0));

disp('Number of subject for which MT_complex is driving: (18 total)')
disp(idx)

idx_avg = sum(driving_following_one_roi > 0);

disp('Number of subject for which MT_complex is driving: (9 total), hemispheres are averaged')
disp(idx_avg)


% ---------------------------------
% How many area is MT+ complex driving?
% !!! Group results of MT+ complex !!!!
% Probability map across subjects for both diriving and following
idx_drive = driving_following > 0;
p_drive = sum(idx_drive, 2);

idx_follow = driving_following < 0;
p_follow = sum(idx_follow, 2);


% !!! Group results of MT+ complex !!!! 
% Averaging the scalar map [-1, 1] across subjects

avg = mean(driving_following, 2);

save('E:\WB-MotionQuartet\derivatives\res_tc\AllSubj_runs_demeanDetr_filt_1_ambNonRever_MT_DRIVING_SCORE.mat', 'avg', 'p_drive', 'p_follow');

% Sorting the values + visualizing help for thresholding
avg_sorted = sort(avg);

figure
plot(avg_sorted)
