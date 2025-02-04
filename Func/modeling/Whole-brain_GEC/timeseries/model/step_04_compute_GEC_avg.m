% Computing average GEC across blocks
clear all;
clc;
close all;

pathname = 'E:\Arrow_of_time\data';
SUB_LIST = {'01', '03', '04', '05', '06', '07', '08', '09', '10'};
TASKS = {'amb', 'phy', 'rest'};
N_nodes = 360;

for it_co=1:size(TASKS, 2)
    for it_su=1:size(SUB_LIST, 2)

        sub_ID = SUB_LIST{it_su};
        
        % Load data
        load(fullfile(pathname, ['sub-', sub_ID, '\tc\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{it_co}, '_model.mat']));
        n_blocks = size(results.LIN_HOPF_INDIV.errorFC, 2);
        
        GEC_avg = zeros(N_nodes);
        for it=1:n_blocks
            GEC_avg = GEC_avg + results.LIN_HOPF_INDIV.GEC{1, it};
            drive = results.LIN_HOPF_INDIV.GEC{1, it}(86,157);
            follow = results.LIN_HOPF_INDIV.GEC{1, it}(157,86);
            
        end
        GEC_avg = GEC_avg / n_blocks;

        results.LIN_HOPF_INDIV.GEC_avg = GEC_avg;

        % Save updated data structure
        save(fullfile(pathname, ['sub-', sub_ID, '\tc\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{it_co}, '_model_avg.mat']), 'results');

    end
end
