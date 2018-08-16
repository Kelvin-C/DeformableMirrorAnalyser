%  |**********************************************************************;
%  * Project           : MSci Project: PLAS-Smith-3
%  *
%  * Program name      : read_zernike.m
%  *
%  * Author            : Kelvin Chan
%  *
%  * Date created      : 22 MAR 2018
%  *
%  * Purpose           : Generates Z data from Zernike polynomials.
%  *
%  * Revision History  : v1.0
%  *
%  |**********************************************************************;

function Z = read_zernike(filename, len, numZernike, mask, fitformat, zernikeremove)
% READ_ZERNIKE Convert fitted zernike polynomials (from MATLAB) into Z data
%   filename: name of file (.txt)
%   len: The 1D size of the output Z matrix (N value of NxN matrix)
%   numZernike: Number of Zernike polynomials stored in text file
%   mask: The array which defines which values are not nan.
%         Set mask = 0 for all values to be kept.
%   fitformat: The fitting format (defined in fit_data.m). Usually
%              is 'standard'.
%   zernikeremove: Set to 1 to ignore piston/tilt/defocus. Set to 2 to
%                  ignore piston/tilt, but keep defocus. Anything else to
%                  keep all values.

% Open the Zernike polynomial text file.
file = fopen(filename, 'r');
format = '%f';

%  Store the Zernike polynomials in array N.
N = fscanf(file, format, numZernike);

% Keep all Z values if mask = 0
if mask == 0
    mask = ones(len, len);
end

% Remove piston/tilt/defocus if zernikeremove = 1.
% Remove piston/tilt if zernikeremove = 2.
% Keep all Zernike polynomials for other values.
if zernikeremove == 1
    N_mask = [0; 0; 0; 1; 0];
    N(1:5) = N(1:5) .* N_mask;
elseif zernikeremove == 2
    N_mask = [0; 0; 0];
    N(1:3) = N(1:3) .* N_mask;
end

% Output the Z data from the Zernike polynomials
Z = ZernikeCalc(1:numZernike, N, mask, fitformat);
Z = sum(Z, 3);
end