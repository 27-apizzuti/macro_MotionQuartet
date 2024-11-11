% Computing LAG-BASED CORRELATION

clear all
clc

tau = 2;
ts = load("E:\Arrow_of_time\data\sub-01\tc\sub-01_amb_VOICarpet_demeanDetr_filt_1.mat");
ts_run1 = squeeze(ts.temp_sig_filt(:,1,:));

mt = (ts_run1(:,2) + ts_run1(:,23) +ts_run1(:,156) +ts_run1(:,157))/4;
frontal = ts_run1(:,86);

data = [mt, frontal]';

% Gustavo's FCf
FCtf = corr(data(:, 1:616-tau)', data(:, 1+tau:616)');

% Ale's
mt_forward = circshift(mt, tau); 
mt_backward = circshift(mt, -tau);

driving_ale = corr(mt_backward, frontal);
following_ale = corr(mt_forward, frontal);

delta_ale = driving_ale - following_ale;
delta_gus = FCtf(2,1) - FCtf(1,2);

% Model cov computation
[clag lags] = xcov(mt, frontal, tau); 
indx=find(lags==tau);
% Normalizing the empirical cross covariation between two brain
% areas across time
COVtauemp=clag(indx)/size(mt,1);

[clag lags] = xcov(frontal, mt, tau); 
indx=find(lags==tau);
% Normalizing the empirical cross covariation between two brain
% areas across time
COVtauemp=clag(indx)/size(mt,1);


% ----------------------
tau = 2;
ts = load("E:\WB-MotionQuartet\derivatives\sub-01\func\GEC\time_series\sub-01_amb_VOICarpet_demeanDetr_filt_1.mat");
ts_run1 = ts.temp_sig_filt(:,:,1);

mt = (ts_run1(:,2) + ts_run1(:,23) +ts_run1(:,156) +ts_run1(:,157))/4;
frontal = ts_run1(:,84);
back = ts_run1(:, 100);

data = [mt, frontal, back]';

% Gustavo's FCf
FCtf = corr(data(:, 1:616-tau)', data(:, 1+tau:616)');

% Ale's
mt_forward = circshift(mt, tau); 
mt_backward = circshift(mt, -tau);

driving_ale_frontal = corr(mt_backward, frontal);
following_ale_frontal = corr(mt_forward, frontal);

driving_ale_back = corr(mt_backward, back);
following_ale_back = corr(mt_forward, back);




