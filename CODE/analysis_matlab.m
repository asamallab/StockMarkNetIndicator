%% Last Modified: 11 February 2021
%% Written by: Hirdesh Kumar Pharasi
%% Email: hirdeshpharasi@gmail.com
%% Codes can be used to generate the following:
%% (1) index log-returns
%% (2) mean market correlation 
%% (3) GARCH volatility 
%% (4) minimum risk Markowitz portfolio
%% If you are using this code, kindly cite the following article:
%% A. Samal, H.K. Pharasi, S. J. Ramaia, H. Kannan, E. Saucan, J. Jost & A. Chakraborti, Network geometry and market instability, R. Soc. Open Sci. 8: 201734 (2021).
%% Network geometry and market instability, (Submitted).
%% To work with moving epochs, we denote Fr: epoch #; Pr: price time series as input; daily_retn= daily logarithmic returns matrix of stock prices
%%
%% function for index returns
%% 
function retn= index_return(Pr,shift,epoch,Fr)
a=shift*(Fr-1)+epoch;
b=a-shift;
retn=log(Pr(a))-log(Pr(b));
end

%% 
%% function for mean correlation
%%
function Mean= Corr_mean(daily_retn,shift,epoch,Fr)
r1=shift*(Fr-1)+1;
r2=shift*(Fr-1)+epoch;
Mean=mean2(corrcoef(daily_retn(r1:r2,:)));
end

%%
%% Garch volatility
%% 
function condVol=garchVol(Index)
Index2=Index-mean(Index);
model1=garch('GARCHLags',1,'ARCHLags',1);
[estMd1,estParamCov,logL]=estimate(model1,Index2);
condVar=infer(estMd1,Index2);
condVol=sqrt(condVar);
end

%%
%% portfolio optimization
%%
function risk1=portfolio_optimization(daily_retn,symbol,shift,epoch,Fr)
r1=shift*(Fr-1)+1;
r2=shift*(Fr-1)+epoch;
dailyReturn = daily_retn(r1:r2,:);
p = Portfolio('AssetList',symbol,'RiskFreeRate',0.01/252);
p = estimateAssetMoments(p, dailyReturn);
p = setDefaultConstraints(p);
w1 = estimateMaxSharpeRatio(p);
[risk1, ret1] = estimatePortMoments(p, w1);
end
