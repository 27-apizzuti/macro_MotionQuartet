% 
% clear all
% HEMI = 'RH';
% 
% % Read scalar values to attribute scalar map to POI -> vertices and write an SMP file 
% % Read POI file with parcellation and POI -> vertices
% SMP_NAME = ['E:\WB-MotionQuartet\derivatives\MNI_template\MNI_0pt6\amb_models.smp'];
% 
% smp = xff(SMP_NAME);
% idx = smp.Map(1).SMPData > 1;
% smp.Map(1).SMPData(idx) = 0;
% 
% smp.SaveAs(['E:\WB-MotionQuartet\derivatives\MNI_template\MNI_0pt6\amb_models_model1.smp']);
% disp('Done.')
% 

clear all
HEMI = 'RH';

% Read scalar values to attribute scalar map to POI -> vertices and write an SMP file 
% Read POI file with parcellation and POI -> vertices
SMP_NAME = ['E:\WB-MotionQuartet\derivatives\MNI_template\MNI_0pt6\amb_models.smp'];

smp = xff(SMP_NAME);
idx = smp.Map(1).SMPData < 2;
smp.Map(1).SMPData(idx) = 0;

idx = smp.Map(1).SMPData > 2;
smp.Map(1).SMPData(idx) = 0;

smp.SaveAs(['E:\WB-MotionQuartet\derivatives\MNI_template\MNI_0pt6\amb_models_model2.smp']);
disp('Done.')