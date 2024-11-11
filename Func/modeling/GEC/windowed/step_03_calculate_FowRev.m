% Tenet empírico
% Compute NR per ROI per subject 

clear all;
clc;

pathname = 'E:\WB-MotionQuartet\derivatives\';
SUB_LIST = {'01', '03', '04', '05', '06', '07', '08', '09', '10'};
TASK = 'phy';
butterworth = true; 

% Parameters
Tau = 2; 
TR = 1;
NSUB = size(SUB_LIST, 2);

% output inizialization
NonRev = zeros(NSUB, 1);
NonRev_matrix = {};
Shifted_FC = {};

path_out = fullfile(pathname, 'res');
    
if ~exist(path_out, 'dir')
   mkdir(path_out)
end

for sub=1:NSUB
    sub_ID = SUB_LIST{sub};
    RES = struct;
    
    % Load block-wise time course
    path_sbj = fullfile(pathname, ['sub-' sub_ID, '\func\GEC\blocks']);
    data = load(fullfile(path_sbj, ['sub-' sub_ID, '_trials_blocks_demeanDetr_filt_1_', TASK, '.mat']));
    n_blocks = size(data.motion, 2);
    n_vox = size(data.motion{1}, 2);
    
    % Prepare output
    NR_blocks = zeros(n_blocks,1);
    FowRev_matrix = {};
    temp_matrix = zeros(n_vox);    
    temp_shifted_FC = zeros(n_vox);

    for it=1:n_blocks

        % // Extract block-time course and compute NR
        ts = data.motion{it}';
        Tm = size(ts, 2);
        
        FCtf = corr(ts(:, 1:Tm-Tau)', ts(:,1+Tau:Tm)');
        FCtr = corr(ts(:,Tm:-1:Tau+1)', ts(:,Tm-Tau:-1:1)');
        Itauf=-0.5*log(1- FCtf.*FCtf);
        Itaur=-0.5*log(1- FCtr.*FCtr);
        Reference=((Itauf(:)-Itaur(:)).^2)';
        
        % // Reshape reference (non-reversability) to matrix
        Reference_reshape = reshape(Reference, size(Itauf));
        FowRev_matrix{it} = Reference_reshape;
        temp_matrix = temp_matrix + Reference_reshape;
        
        % // Summarize results per subject
        index=find(Reference>quantile(Reference, 0.0));      % can vary quantile, for now we are keeping all the ROIS 
        NR_blocks(it) = nanmean(Reference(index));
        
        % // Storing the shifted FC matrix
        temp_shifted_FC = temp_shifted_FC + FCtf;
    end

   NonRev(sub) = mean(NR_blocks);
   NonRev_matrix{sub} = temp_matrix/n_blocks;
   Shifted_FC{sub} = temp_shifted_FC/n_blocks;

   % Save single-subject results
   save(fullfile(path_sbj, ['sub-', sub_ID, '_trials_blocks_demeanDetr_filt_', num2str(butterworth), '_', TASK,  'NonRever.mat']), 'FowRev_matrix');

end

% Save all subjects results
save(fullfile(path_out, ['AllSubj_trials_blocks_demeanDetr_filt_', num2str(butterworth), '_', TASK,  'NonRever.mat']), 'NonRev', 'NonRev_matrix', 'Shifted_FC'); 