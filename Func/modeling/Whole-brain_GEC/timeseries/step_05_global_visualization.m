clear all;

HEMI = 'RH';
TASK = 'phy';
N_ROI = 180;

% Read scalar values to attribute scalar map to POI -> vertices and write an SMP file 
% Read POI file with parcellation and POI -> vertices
POI_NAME = ['E:\WB-MotionQuartet\derivatives\res_tc\BV_visuals\Glasser_atlas_' HEMI '.poi'];
SMP_NAME = 'E:\WB-MotionQuartet\derivatives\res_tc\BV_visuals\example_seed_target.smp';

load(['E:\Arrow_of_time\data\res\AllSubj_trials_blocks_demeanDetr_filt_1_' TASK 'NonRever_wholebrain_DRIVING_SCORE.mat'])
%% 
smp = xff(SMP_NAME);
poi = xff(POI_NAME);

if strcmp(HEMI, 'RH')
    avg = avg_score(181:end);
    p_drive = p_drive(181:end);
    p_follow = p_follow(181:end);
else
    avg = avg_score(1:180);

end

avg = (avg / 360);
% Assign values to SMP
for roi=1:N_ROI
    idx = poi.POI(roi).Vertices;
    smp.Map(1).SMPData(idx) = avg(roi);
    smp.Map(2).SMPData(idx) = p_drive(roi);
    smp.Map(3).SMPData(idx) = p_follow(roi);

    % Adjust colormap
    smp.Map(1).LUTName = 'C:/Users/apizz/Documents/BrainVoyager/MapLUTs/pos-red_neg-blue.olt';
    smp.Map(2).LUTName = '<default>';
    smp.Map(3).LUTName = '<default>';

end

smp.SaveAs(['E:\Arrow_of_time\data\res\' TASK, 'WHOLEBRAIN_DRIVING_SCORE_' HEMI '.smp']);
disp('Done.')
