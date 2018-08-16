%  |**********************************************************************;
%  * Project           : MSci Project: PLAS-Smith-3
%  *
%  * Program name      : genetic_algorithm.m
%  *
%  * Author            : Kelvin Chan and Alice Cao
%  *
%  * Date created      : 05 MAR 2018
%  *
%  * Purpose           : Initiates the genetic algorithm optimisation
%  *
%  * Revision History  : v1.0
%  *
%  |**********************************************************************;

function [x, fval] = genetic_algorithm()
%Start the timer
tic

%Define the Fitness Function
FitnessFunction = @fitness_func;

%Number of Actuators
numberOfVariables = 3;

% Values are duty cycles (range from 0 to 100)
LB = [0 0 0];   % Lower bound
UB = [100 100 100];  % Upper bound

%Initiate Optimisation and plot graph whilst running
opts = optimoptions(@ga,'PlotFcn',{@gaplotbestf,@gaplotstopping});

%Population Size (number of trials per generation)
opts.PopulationSize = 20;

%Number of Generations
generations = 20;

%The lower and upper bound for the duty cycle of each variable/actuator
opts.InitialPopulationRange = [0 0 0; 100 100 100];

%Define max number of generations
opts = optimoptions(opts,'MaxGenerations', generations,'MaxStallGenerations', 100);

%Run the Genetic Algorithm
[x,Fval,exitFlag,Output] = ...
    ga(FitnessFunction,numberOfVariables,[],[],[],[], LB, UB, [],opts);

fprintf('The number of generations was : %d\n', Output.generations);
fprintf('The number of function evaluations was : %d\n', Output.funccount);
fprintf('The best function value found was : %g\n', Fval);

%Stop time and show the computational time.
toc

