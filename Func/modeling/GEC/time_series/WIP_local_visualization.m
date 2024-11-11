clear all;

HEMI = 'LH';
N_ROI = 180;

% Read scalar values to attribute scalar map to POI -> vertices and write an SMP file 
% Read POI file with parcellation and POI -> vertices
POI_NAME = ['E:\WB-MotionQuartet\derivatives\res_tc\BV_visuals\Glasser_atlas_' HEMI '.poi'];
SMP_NAME = 'E:\WB-MotionQuartet\derivatives\res_tc\BV_visuals\example_seed_target.smp';

load('E:\WB-MotionQuartet\derivatives\res_tc\BV_visuals\AllSubj_runs_demeanDetr_filt_1_ambNonRever_MT_DRIVING_SCORE.mat')
%% 
smp = xff(SMP_NAME);
poi = xff(POI_NAME);

if strcmp(HEMI, 'RH')
    avg = avg(181:end);
    p_drive = p_drive(181:end);
    p_follow = p_follow(181:end);

end
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

smp.SaveAs([SMP_NAME(1:end-4), '_DRIVING_SCORE_' HEMI '.smp']);
disp('Done.')
