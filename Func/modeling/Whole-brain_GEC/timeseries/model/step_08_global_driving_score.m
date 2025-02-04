clear all; clc;

% Load MODEL result (GEC)
itask = 1;     % 1: amb; 2: phy; 3:rest.

res = load(['E:\Arrow_of_time\data\res_model_tc\Allsbj_avg_GEC_model_tc.mat']);
disp(['Analysing ' res.TASKS{itask}]);

N_SUB = 9;
drivigng_score = zeros(360, N_SUB);

for sub=1:N_SUB
    data = squeeze(res.mat_gec(itask, sub, :,:));  
    for roi=1:size(data,1)
        drive = data(:, roi);
        follow = data(roi, :);
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
save(['E:\Arrow_of_time\data\res_model_tc\Allsbj_avg_GEC_model_tc_' res.TASKS{itask}, '_wholebrain_DRIVING_SCORE.mat'], 'avg_score', 'p_drive', 'p_follow');







