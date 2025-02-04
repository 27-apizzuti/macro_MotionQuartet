% clear all;
% 
% HEMI = 'RH';
% TASK = 'phy';
% N_ROI = 180;
% 
% % Read scalar values to attribute scalar map to POI -> vertices and write an SMP file 
% % Read POI file with parcellation and POI -> vertices
% POI_NAME = ['E:\Arrow_of_time\data\visuals\Glasser_atlas_' HEMI '.poi'];
% SMP_NAME = 'E:\Arrow_of_time\data\visuals\example_seed_target_4maps.smp';
% 
% load(['E:\Arrow_of_time\data\res_model_tc\WIP_Allsbj_avg_GEC_model_tc_', TASK, '_wholebrain_HIERARCHY.mat'])
% %% 
% smp = xff(SMP_NAME);
% poi = xff(POI_NAME);
% 
% if strcmp(HEMI, 'RH')
%     driveness = driveness(181:end, :);
%     receiveness = receiveness(181:end, :);
%     hierarchiness = hierarchiness(181:end, :);
%     drive_rec_diff = drive_rec_diff(181:end, :);
% else
%     driveness = driveness(1:180, :);
%     receiveness = receiveness(1:180, :);
%     hierarchiness = hierarchiness(1:180, :);
%     drive_rec_diff = drive_rec_diff(1:180, :);
% 
% 
% end
% 
% % Average across participants
% driveness = mean(driveness, 2);
% receiveness = mean(receiveness, 2);
% hierarchiness = mean(hierarchiness, 2);
% drive_rec_diff = mean(drive_rec_diff, 2);
% 
% % Assign values to SMP
% for roi=1:N_ROI
%     idx = poi.POI(roi).Vertices;
%     smp.Map(1).SMPData(idx) = driveness(roi);
%     smp.Map(2).SMPData(idx) = receiveness(roi);
%     smp.Map(3).SMPData(idx) = hierarchiness(roi);
%     smp.Map(4).SMPData(idx) = drive_rec_diff(roi);
% 
%     % Adjust colormap
%     smp.Map(1).LUTName = '<default>';
%     smp.Map(2).LUTName = '<default>';
%     smp.Map(3).LUTName = '<default>';
%     smp.Map(4).LUTName = '<default>';
% 
%     % Adjust map name
%     smp.Map(1).Name = 'Driveness';
%     smp.Map(2).Name = 'Receiveness';
%     smp.Map(3).Name = 'Hierarchiness';
%     smp.Map(4).Name = 'Drive minus Rec';
% 
% end
% 
% % Adjust min-max
% smp.Map(1).LowerThreshold = min(driveness);
% smp.Map(2).LowerThreshold = min(receiveness);
% smp.Map(3).LowerThreshold = min(hierarchiness);
% smp.Map(4).LowerThreshold = min(drive_rec_diff);
% 
% 
% smp.Map(1).UpperThreshold = max(driveness);
% smp.Map(2).UpperThreshold = max(receiveness);
% smp.Map(3).UpperThreshold = max(hierarchiness);
% smp.Map(4).UpperThreshold = max(drive_rec_diff);
% 
% 
% smp.SaveAs(['E:\Arrow_of_time\data\res_model_tc\WIP_' TASK, 'WHOLEBRAIN_HIERARCHY_' HEMI '.smp']);
% disp('Done.')


%% ----------------
clear all
HEMI = 'RH';

% Read scalar values to attribute scalar map to POI -> vertices and write an SMP file 
% Read POI file with parcellation and POI -> vertices
POI_NAME = ['E:\Arrow_of_time\data\visuals\Glasser_atlas_' HEMI '.poi'];
SMP_NAME = 'E:\Arrow_of_time\data\visuals\example_seed_target.smp';

load(['E:\Arrow_of_time\data\res_model_tc\WIP_Allsbj_avg_GEC_model_tc_AllTask_wholebrain_HIERARCHY.mat'])

smp = xff(SMP_NAME);
poi = xff(POI_NAME);

if strcmp(HEMI, 'RH')
    diff_tasks = diff_tasks(181:end);
    diff_task_rest = diff_task_rest(181:end);
else
    diff_tasks = diff_tasks(1:180);
    diff_task_rest = diff_task_rest(1:180);

end

% Assign values to SMP
for roi=1:N_ROI
    idx = poi.POI(roi).Vertices;
    smp.Map(1).SMPData(idx) = diff_tasks(roi);
    smp.Map(2).SMPData(idx) = diff_task_rest(roi);


end

% Adjust colormap
smp.Map(1).LUTName = '<default>';
smp.Map(2).LUTName = '<default>';

% Adjust map name
smp.Map(1).Name = 'Amb minus Phy';
smp.Map(2).Name = 'Task minus Rest';

% Adjust min-max
smp.Map(1).LowerThreshold = min(diff_tasks);
smp.Map(2).LowerThreshold = min(diff_task_rest);

smp.Map(1).UpperThreshold = max(diff_tasks);
smp.Map(2).UpperThreshold = max(diff_task_rest);


smp.SaveAs(['E:\Arrow_of_time\data\res_model_tc\WIP_WHOLEBRAIN_HIERARCHY_changes_' HEMI '.smp']);
disp('Done.')