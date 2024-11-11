% Figures for the Optimisation of the Linear Hopf Model 
clear all;
clc;
close all;

pathname = 'E:\WB-MotionQuartet\derivatives';    % !!! TO BE CHANGED
SUB_LIST = {'01', '03', '04', '05', '06', '07', '08', '09', '10'};
TASKS = {'phy', 'amb', 'rest'};

% Plot Results for each subject and condition  
for it_co=1:size(TASKS, 2)
    for it_su=1:size(SUB_LIST, 2)

        sub_ID = SUB_LIST{it_su};

        % Load data
        path_sbj = fullfile(pathname, ['sub-', sub_ID, '\func\GEC']);
        res = load(fullfile(path_sbj,  ['\sub-', sub_ID, '_demeanDetr_filt_1_', TASKS{it_co}, '_model.mat']));
        
        if iscell(res.results.LIN_HOPF_INDIV.errorFC)
            n_blocks = size(res.results.LIN_HOPF_INDIV.errorFC, 2);
            
            % Compute GEC similary across blocks
            GECsim = zeros(n_blocks);
    
            for it=1:n_blocks
                gec1 = res.results.LIN_HOPF_INDIV.GEC{1, it};
                for it2=1:n_blocks
                    gec2 = res.results.LIN_HOPF_INDIV.GEC{1, it2};
                    GECsim(it, it2) = corr(gec1(:), gec2(:));
                end
            end
            
            % Zeroing the diagonal of GECsim mtrix
            GECsim(find(eye(size(GECsim)))) = 0;
        
            % Plot
            figure
            for it_blo=1:n_blocks
                subplot(2, 2, 1)
                plot(res.results.LIN_HOPF_INDIV.errorFC{1,it_blo})
                xlabel('Iterations')
                ylabel('Error FC')
                ylim([0, 0.7])
                hold on
                subplot(2, 2, 2)
                plot(res.results.LIN_HOPF_INDIV.errorCOVtau{1,it_blo})
                xlabel('Iterations')
                ylabel('Error Covariance tau')
                hold on
                ylim([0, 0.7])
                subplot(2, 2, 3)
                imagesc(GECsim)
                caxis([-1, 1])
                title('GEC similarity')  
                
            end
            subplot(2, 2, 4)
            plot(cell2mat(res.results.LIN_HOPF_INDIV.fittFC), '-o')
            hold on
            plot(cell2mat(res.results.LIN_HOPF_INDIV.fittCVtau), '-o')
            hlg = legend('fittFC', 'fittCVtau', 'Location','best');
            xlabel('Blocks')
            ylabel('Goodness of fit')
            yline(0.5, '--')
            ylim([0.1, 1])
            fontsize(hlg,'decrease')

            % Save figure
            sgtitle(['Model results sub-', sub_ID, ' ', TASKS{it_co}])
            saveas(gcf, fullfile(path_sbj, ['\ModelResults_', TASKS{it_co}, '.jpeg']), 'jpeg');
        else
            n_blocks = 1;
            
            % Compute GEC similary across blocks
            GECsim = zeros(n_blocks);
    
            for it=1:n_blocks
                gec1 = res.results.LIN_HOPF_INDIV.GEC;
                for it2=1:n_blocks
                    gec2 = res.results.LIN_HOPF_INDIV.GEC;
                    GECsim(it, it2) = corr(gec1(:), gec2(:));
                end
            end
            
            % Zeroing the diagonal of GECsim mtrix
            GECsim(find(eye(size(GECsim)))) = 0;
            
            % Plot
            figure
            for it_blo=1:n_blocks
                subplot(2, 2, 1)
                plot(res.results.LIN_HOPF_INDIV.errorFC)
                xlabel('Iterations')
                ylabel('Error FC')
                % ylim([0, 0.7])
                hold on
                subplot(2, 2, 2)
                plot(res.results.LIN_HOPF_INDIV.errorCOVtau)
                xlabel('Iterations')
                ylabel('Error Covariance tau')
                hold on
                % ylim([0, 0.7])
                subplot(2, 2, 3)
                imagesc(GECsim)
                caxis([-1, 1])
                title('GEC similarity')  
                
            end
                subplot(2, 2, 4)
                plot(res.results.LIN_HOPF_INDIV.fittFC, '-o')
                hold on
                plot(res.results.LIN_HOPF_INDIV.fittCVtau, '-o')
                hlg = legend('fittFC', 'fittCVtau', 'Location','best');
                xlabel('Blocks')
                ylabel('Goodness of fit')
                yline(0.5, '--')
                ylim([0.1, 1])
                fontsize(hlg,'decrease')
    
                % Save figure
                sgtitle(['Model results sub-', sub_ID, ' ', TASKS{it_co}])
                saveas(gcf, fullfile(path_sbj, ['\ModelResults_', TASKS{it_co}, '.jpeg']), 'jpeg');
            end
    
            
    
    end
end