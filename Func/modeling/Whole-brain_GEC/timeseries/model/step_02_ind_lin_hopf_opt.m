%% Linear hopf model optimisation script - PER SUBJECT

% This script will optimise the structural connectivity connectivity through iterative
% learning, leading to a minimised error between the empirical FC and the
% simulated FC PER SUBJECT
clear all;
clc;

pathname = 'E:\Arrow_of_time\data';    % !!! TO BE CHANGED
SUB_LIST = {'01', '03', '04', '05', '06', '07', '08', '09', '10'};
TASKS = {'amb', 'phy', 'rest'};
% ------------------------------------------------------------------------
% Dataset parameters
N = 360;    % number of nodes
TR = 1;     % s 
tau = 2;    % s

% Structural connectivity
C = load(fullfile(pathname, "sc_glasser360afni.mat"));

C = C.sc_glasser360afni;
maxC = 0.2;
C = C/max(max(C))*maxC; 

% Parameters of the model
sigma = 0.01;
epsFC = 0.0004;
epsCOV = 0.0001;

for it_task=1:size(TASKS, 2)                            % // Number of condition

    TASK = TASKS{1, it_task};
    disp(['Working on ', TASK])

    for k=1:size(SUB_LIST, 2)                            % // Number of subjects
        
        sub_ID = SUB_LIST{k};

        disp(['    sub-', num2str(sub_ID)])

        path_sbj = fullfile(pathname, ['sub-', sub_ID], '\tc');
        data = load(fullfile(path_sbj, ['sub-', sub_ID, '_runs_blocks_demeanDetr_filt_1_', TASK,  '_f_diff.mat']));
        results = struct;

        for l=1:size(data.data, 2)                     % // Number of blocks 

            disp(['       run ', num2str(l)])
            ts_block = data.data{1, l}';
    
            % Number of time points
            Tm=size(ts_block, 1); 
    
            % Working with the Timepoints x Nodes (tst)
            tst=ts_block;
    
            % Computing Functional Connectivity
            FCemp=corrcoef(tst); % tst is ts transposed
    
            % Covariation of the timeseries analysis Timepoints x Nodes
            COVemp = cov(tst);
    
            for s=1:N
                for j=1:N
                    sigratio(s,j)=1/sqrt(COVemp(s,s))/sqrt(COVemp(j,j));
                    % Compute the cross-covariance between two brain areas at all
                    % timepoints with a lag tau
                    [clag lags] = xcov(tst(:,s),tst(:,j),tau); 
                    indx=find(lags==tau);
                    % Normalizing the empirical cross covariation between two brain
                    % areas across time
                    COVtauemp(s,j)=clag(indx)/size(tst,1);
                end
            end
            % Multiplying the empirical COV matrix per subject times the sigratio
            COVtauemp = COVtauemp.*sigratio;
            COVtauemp = COVtauemp;
    
            %%%%%%%% MODEL OPTIMISATION
            Cnew = C;   % // structural connectivity
            olderror=100000;
    
            disp(['       Starting model optimization'])
            tic
            
            for iter=1:5000
    
                % Linear Hopf FC
                [FCsim, COVsim, COVsimtotal, A] = hopf_int(Cnew, data.F_diff_blocks{1,l}, sigma); 
                COVtausim = expm((tau*TR)*A)*COVsimtotal;
                COVtausim = COVtausim(1:N,1:N);
            
                for s=1:N
                    for j=1:N
                        sigratiosim(s,j)=1/sqrt(COVsim(s,s))/sqrt(COVsim(j,j));
                    end
                end
                
                COVtausim=COVtausim.*sigratiosim;
                results.LIN_HOPF_INDIV.errorFC{l}(iter)=mean(mean((FCemp-FCsim).^2));
                results.LIN_HOPF_INDIV.errorCOVtau{l}(iter)=mean(mean((COVtauemp-COVtausim).^2));
    
                if mod(iter,100)<0.1
                    errornow=mean(mean((FCemp-FCsim).^2)) + mean(mean((COVtauemp-COVtausim).^2));
                    results.LIN_HOPF_INDIV.errornow_hist{l}(iter)=errornow;
                    if  (olderror-errornow)/errornow<0.001
                        % break;
                    end
                    if  olderror<errornow
                        break
                    end
                    olderror=errornow;
                end
    
                for s=1:N  %% learning
                    for j=1:N
                        if (C(s,j)>0 || j==N/2+s)   
                            Cnew(s,j)=Cnew(s,j)+epsFC*(FCemp(s,j)-FCsim(s,j)) ...
                                +epsCOV*(COVtauemp(s,j)-COVtausim(s,j));
                            if Cnew(s,j)<0
                                Cnew(s,j)=0;
                            end
                        end
                    end
                end
                Cnew = Cnew/max(max(Cnew))*maxC;
            end
    
            %%%%%%%%%%% RESULTS
            
            toc
            GEC=Cnew;
            results.LIN_HOPF_INDIV.GEC{l} = GEC;
            [FCsim, COVsim, COVsimtotal, A] = hopf_int(GEC, data.F_diff_blocks{1,l}, sigma);
            COVtausim = expm((tau*TR)*A)*COVsimtotal;
            COVtausim = COVtausim(1:N, 1:N);
            
            for s=1:N
                for j=1:N
                    sigratiosim(s,j) = 1/sqrt(COVsim(s,s))/sqrt(COVsim(j,j));
                end
            end
    
            COVtausim = COVtausim.*sigratiosim;
            results.LIN_HOPF_INDIV.COVtausim{l} = COVtausim;
            results.LIN_HOPF_INDIV.fittFC{l} = corr2(FCemp, FCsim);
            results.LIN_HOPF_INDIV.fittCVtau{l} = corr2(COVtauemp, COVtausim);
        end

        disp('       Save results')    
        
        % Save results 
        save(fullfile(path_sbj, ['sub-' sub_ID, '_demeanDetr_filt_1_', TASK, '_model.mat']), 'results');
    
    end

end