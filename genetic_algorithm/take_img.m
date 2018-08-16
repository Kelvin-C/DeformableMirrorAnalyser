%  |**********************************************************************;
%  * Project           : MSci Project: PLAS-Smith-3
%  *
%  * Program name      : take_img.m
%  *
%  * Author            : Kelvin Chan and Alice Cao
%  *
%  * Date created      : 05 MAR 2018
%  *
%  * Purpose           : Uses the camera take an image and finds the sum of
%  *                     the squares of the intensity distribution.
%  *
%  * Revision History  : v1.0
%  *
%  |**********************************************************************;

function sum_sqrs = take_img()

    %Settings for the camera
    exposure = 50;
    gain = 0;
    
    %To reduce computational time, crops the image. The region
    %that is kept is given below:
    %0 = centre, 1 = top-left, 2 = top-right, 3 = bottom-left, 4 = bottom-right
    crop = 0;
    
    %Add NET Assembly
    NET.addAssembly('C:\Program Files\Thorlabs\Scientific Imaging\DCx Camera Support\Develop\DotNet\uc480DotNet.dll')

    %Create camera object
    cam = uc480.Camera;

    %Open the 1st available camera
    cam.Init(0);

    %Set display mode to bitmap (DiB)
    cam.Display.Mode.Set(uc480.Defines.DisplayMode.DiB);

    %Set colour mode to 8-Bit RGB
    %cam.PixelFormat.Set(uc480.Defines.ColorMode.RGBA8Packed);
    cam.PixelFormat.Set(uc480.Defines.ColorMode.Mono8);

    %Set trigger mode to software (single image acquisition)
    cam.Trigger.Set(uc480.Defines.TriggerMode.Software);

    %Allocate image memory
    [~, MemId] = cam.Memory.Allocate(true);

    %Set camera exposure and gain
    cam.Timing.Exposure.Set(exposure);
    cam.Gain.Hardware.Scaled.SetMaster(gain);

    %Obtain image information
    [~, Width, Height, Bits, ~] = cam.Memory.Inquire(MemId);

    %Acquire image
    cam.Acquisition.Freeze(uc480.Defines.DeviceParameter.Wait);

    %Copy image from memory
    [~, tmp] = cam.Memory.CopyToArray(MemId);

    %Reshape Image
    Data = reshape(uint8(tmp), [Bits/8, Width, Height]);
    Data = Data(1, 1:Width, 1:Height);
    Data = permute(Data, [3,2,1]);
    
    %Convert Data into type 'double' instead of uint8 to allow squaring
    Data = double(Data);
    
    %Turn off camera
    cam.Exit;
    
    %Display Image
    %himg = imshow(Data);
    
    %Crops the captured image
    if crop == 0
        r = 8;
        Data = Data((Height/r):(Height/2 + Height/r), (Width/r):(Width/2 + Width/r));
    elseif crop == 1
        Data = Data(1:Height/2, 1:Width/2);
    elseif crop == 2
        Data = Data(1:Height/2, Width/2:Width);
    elseif crop == 3
        Data = Data(Height/2:Height, 1:Width/2);
    elseif crop == 4
        Data = Data(Height/2:Height, Width/2:Width);
    end
    
   %Calculate the sum of the squares
    inty = Data.^2;
    sum_sqrs = sum(sum(inty))*-1;
end