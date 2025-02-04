fc_mean = zeros(9,2);
fc_fct_mean = zeros(9,2);
nr_mean = zeros(9,2);
Reference_reshape = {};
NR_new = zeros(9,2);

for sub=1:9
    fc_mean(sub, 1) = nanmean(nanmean(block.Shifted_FC{1, sub}));
    fc_mean(sub, 2) = nanmean(nanmean(tc.Shifted_FC{1, sub}));
    
    % COMPUTING NR ON THE AVERAGED MATRIX
    % block
    FCtf = block.Shifted_FC{1, sub};
    FCtr = block.Shifted_FC{1, sub}';

    Itauf=-0.5*log(1- FCtf.*FCtf);
    Itaur=-0.5*log(1- FCtr.*FCtr);
    Reference=((Itauf(:)-Itaur(:)).^2)';
    Reference_reshape{sub,1} = reshape(Reference, size(Itauf));
    NR_new(sub,1) = nanmean(nanmean(Reference));
    
    % time series
    FCtf = tc.Shifted_FC{1, sub};
    FCtr = tc.Shifted_FC{1, sub}';
    
    Itauf=-0.5*log(1- FCtf.*FCtf);
    Itaur=-0.5*log(1- FCtr.*FCtr);
    Reference=((Itauf(:)-Itaur(:)).^2)';
    Reference_reshape{sub,2} = reshape(Reference, size(Itauf));
    NR_new(sub,2) = nanmean(nanmean(Reference));
    % ------------------------------
   
    fc_fct_mean(sub, 1) = nanmean(nanmean(abs(block.Shifted_FC{1, sub}-block.Shifted_FC{1, sub}')));
    fc_fct_mean(sub, 2) = nanmean(nanmean(abs(tc.Shifted_FC{1, sub}-tc.Shifted_FC{1, sub}')));

    nr_mean(sub, 1) = nanmean(nanmean(block.NonRev_matrix{1, sub}));
    nr_mean(sub, 2) = nanmean(nanmean(tc.NonRev_matrix{1, sub}));
end
