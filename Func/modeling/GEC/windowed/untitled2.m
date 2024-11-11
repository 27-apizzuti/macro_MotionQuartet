clear all; clc;

% Load INSIDEOUT results
res_amb = load("E:\WB-MotionQuartet\derivatives\res_tc\AllSubj_runs_demeanDetr_filt_1_ambNonRever.mat");
% res_amb = load("E:\WB-MotionQuartet\derivatives\res\AllSubj_trials_blocks_demeanDetr_filt_1_phyNonRever.mat");

NSUB = 9;
hMT_row = {};
hMT_col = {};
h = 180;
for sub=1:NSUB
    temp = res_amb.Shifted_FC{1, sub};
    % r = (temp(23+h, :) + temp(2+h, :) + temp(157+h, :) + temp(156+h, :))/4;
    % c = (temp(:, 23+h) + temp(:, 2+h) + temp(:, 157+h) + temp(:, 156+h))/4;
    
    r = temp(23, :);
    c = temp(:, 23);
    hMT_driving{sub} = r;
    hMT_follow{sub} = c;

    delta_gus = temp(84,23) - temp(23,84);
    disp(delta_gus)
    disp(c(84)-r(84))
end