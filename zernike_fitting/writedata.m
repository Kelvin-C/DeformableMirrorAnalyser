%  |**********************************************************************;
%  * Project           : MSci Project: PLAS-Smith-3
%  *
%  * Program name      : writedata.m
%  *
%  * Author            : Kelvin Chan
%  *
%  * Date created      : 23 MAR 2018
%  *
%  * Purpose           : Writes Zernike polynomials to a text file.
%  *
%  * Revision History  : v1.0
%  *
%  |**********************************************************************;

function writedata(filename, N)
% WRITEDATA Writes Zernike polynomials to a text file.
%   filename: Name of text file that is used to stored the polynomials
%   N: The array of polynomials.

file = fopen(filename, 'wt');

fprintf(file, '%f\n' , N);
fclose(file)

end