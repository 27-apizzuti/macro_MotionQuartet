clear all; clc;

% Load INSIDEOUT results
TASK = 'rest';
res_amb = load(['E:\WB-MotionQuartet\derivatives\res_tc\AllSubj_runs_demeanDetr_filt_1_' TASK 'NonRever.mat']);
N_SUB = 9;
drivigng_score = zeros(360, N_SUB);

for sub=1:N_SUB
    data = res_amb.Shifted_FC{1, sub};  
    for roi=1:size(data,1)
        drive = data(:, roi);
        follow = data(roi,:);
        diff = drive' - follow;
        drivigng_score(roi, sub) = sum(diff > 0);     % sum the positive
        drivigng_score_scalar(roi, sub) = mean(diff); % average the values
    end
end

% !!! Group result: avg_score = on average how many areas is a seed area
% DRIVE across subjects
avg_score = mean(drivigng_score, 2);
std_avg_score = std(drivigng_score,0, 2);
[sd, r] = sort(avg_score,'descend');

% !!! Group result: p_drive_score = on average is an area driving or
% following? How manu subjects show the same behavior?

idx = drivigng_score_scalar > 0;
p_drive = sum(idx, 2);

idx2 = drivigng_score_scalar < 0;
p_follow = sum(idx2, 2);

% save
save(['E:\WB-MotionQuartet\derivatives\res_tc\AllSubj_runs_demeanDetr_filt_1_' TASK 'NonRever_wholebrain_DRIVING_SCORE.mat'], 'avg_score', 'p_drive', 'p_follow');







