# |**********************************************************************;
# * Project           : MSci Project: PLAS-Smith-3
# *
# * Program name      : uc480.py
# *
# * Author            : Kelvin Chan
# *
# * Date created      : 05 Feb 2018
# *
# * Purpose           : UI created to control the Piezoelectric Actuators
# *
# * Revision History  : v1.0
# *
# |**********************************************************************;

from instrumental.drivers.cameras import uc480
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as anim
from matplotlib.widgets import Slider
from PIL import Image
import tkinter as tk
from tkinter import messagebox

from paramiko import SSHClient
from paramiko.ssh_exception import AuthenticationException, AuthenticationException, BadHostKeyException, SSHException
import socket

import func_optimise
import func_clean
import func_crop

import numpy as np

import time
import os

def mean_std(array):
    if array.ndim == 3:
        array = array.transpose(0, 2, 1)
        new_array = []
        for i in range(len(array)):
            new_array.append([list(map(np.mean, array[i]))] + [list(map(np.std, array[i]))])
        new_array = np.array(new_array).transpose(0, 1, 2)
        return new_array
    array = list(map(np.mean, array)) + list(map(np.std, array))
    return array

def login():
    ip = '169.254.99.105'
    user = 'pi'
    passw = 'raspberry'
    return ip, user, passw

class GUI():

    def __init__(self):
        """
        The initial UI of the software.
        """
        self.__window = tk.Tk()
        self.__initvideobutton()
        self.__initpiezoentry()
        self.__window.mainloop()


    def window(self):
        return self.__window

    def __initvideobutton(self):
        """
        Generates a button to initiate the live-feed window.
        """
        frame = tk.Frame(self.window())
        frame.grid(row=0, column=0)
        videobutton = tk.Button(frame, text="Video", command=self.__openvideo)
        videobutton.pack(side=tk.TOP, padx=10, pady=10)

    def __initpiezoentry(self):
        """
        Creates an entry box to allow user to input the number of piezos on the deformable mirror.
        """
        frame = tk.Frame(self.window())
        frame.grid(row=1, column=0)
        piezolabel = tk.Label(frame, text="Number of Piezos: ")
        self.piezoentry = tk.Entry(frame)
        piezolabel.pack(side=tk.LEFT, padx=5, pady=10)
        self.piezoentry.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.X, expand=True)


    def __openvideo(self):
        """
        Closes the initial UI window and opens the live-feed window.
        """
        piezo_num = self.piezoentry.get()
        try:
            piezo_num = int(piezo_num)
        except ValueError:
            messagebox.showinfo("ERROR!", "Incorrect entry for the number of piezos.")
            return
        self.__window.destroy()
        videoGUI(piezo_num=piezo_num)


class videoGUI():

    def __init__(self, piezo_num, auto=True, figsize=(12, 6), dir="images"):
        """
        The UI with the live-feed of the camera.

        Parameters:
            auto = set auto exposure on or off (default True)
            figsize = size of the live-feed window (default (7,6))
            dir = output of the saved images
        """
        self.__newwindow = tk.Tk()
        self.piezo_sweep_num = tk.StringVar(self.__newwindow)
        self.piezo_sweep_num.set("No Sweep")
        self.__piezo_num = piezo_num
        self.makePiezoWindow()

        # self.__window = tk.Tk()
        #
        # self.__image_dir = dir
        # if not os.path.exists(self.__image_dir):
        #     os.makedirs(self.__image_dir)
        #
        # self.__pause = False
        # self.__pause_message = "LIVE"
        #
        # label = tk.Label(self.__window, text="Press P to pause, A to retrieve voltage data, SPACE to save voltage data, ENTER to save image")
        # label.pack(pady=5, padx=10)
        #
        # self.__pauselabel = tk.Label(self.__window, text=self.__pause_message)
        # self.__pauselabel.pack(pady=5, padx=10)
        #
        # pausebutton = tk.Button(self.__window, text="PAUSE/START", command=lambda: self.__pause_start())
        # pausebutton.pack(pady=5, padx=10)

        ip, user, raspberry = login()

        try:
            self.__client = SSHClient()
            self.__client.load_system_host_keys()
            self.__client.connect(ip, username=user, password=passw)
        except (BadHostKeyException, AuthenticationException,
                SSHException, socket.error) as e:
            messagebox.showinfo('ERROR!', "Failed to connect to Raspberry Pi")

        # self.fig = plt.Figure(figsize=figsize)
        # self.ax = self.fig.add_subplot(121)
        #
        # try:
        #     self.cam = uc480.UC480_Camera()
        # except Exception:
        #     messagebox.showinfo('ERROR!', "Failed to connect to the camera")
        #     self.__window.destroy()
        # self.cam.set_auto_exposure(enable=auto)
        #
        # img = self.cam.grab_image()
        # self.im = self.ax.imshow(img, cmap='gray', vmin=0, vmax=255)
        # self.cb = self.fig.colorbar(self.im)
        #
        # self.axplot = self.fig.add_subplot(122)
        # self.axplot.set_title("Phases (solved)")
        # self.axplot.set_ylabel('$Phase$', fontsize=18)
        # self.axplot.set_xlabel('$Voltage$ $(V)$', fontsize=18)
        # self.phase_values = [[], []]
        # self.voltages = []
        #
        # self.canvas = FigureCanvasTkAgg(self.fig, master=self.__window)
        # self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        # self.canvas.draw()
        #
        # self.__window.bind("<Key>", self.__key)
        # self.__window.after(1, lambda: self.__window.focus_force())
        #
        # self.__an = anim.FuncAnimation(self.fig, self.refreshimage, interval=200, blit=False, repeat=True)
        # self.__window.mainloop()

    def makePiezoWindow(self):
        """
        Creates the window that allows control of the piezos.
        Sweeping over a range of duty cycles for a particular piezo with other piezos constant is possible.
        """
        self.opto_entries = []
        self.dc_entries = []
        self.channel_entries = []

        self.piezo_sweep_bool = False
        self.piezo_sweep_ind = -1

        #Creates the UI in the window
        for i in range(self.__piezo_num):
            frame = tk.Frame(self.__newwindow)
            frame.grid(row=i, column=0)

            piezo_line_label = tk.Label(frame, text="%s: "%i, font='Helvetica 14 bold')
            opto_text = tk.Label(frame, text="Optoswitch number: ")
            opto_entry = tk.Entry(frame)
            opto_entry.insert(tk.END, '%i' % (i+1))
            channel_text = tk.Label(frame, text="PWM channel number: ")
            channel_entry = tk.Entry(frame)
            channel_entry.insert(tk.END, '%i' %i)

            piezo_line_label.pack(side=tk.LEFT, padx=5, pady=5)
            opto_text.pack(side=tk.LEFT, padx=5, pady=5)
            opto_entry.pack(side=tk.LEFT, pady=5, fill=tk.X, expand=True)
            channel_text.pack(side=tk.LEFT, padx=5, pady=5)
            channel_entry.pack(side=tk.LEFT, pady=5, fill=tk.X, expand=True)
            frame_col1 = tk.Frame(self.__newwindow)
            frame_col1.grid(row=i, column=1)

            frame = tk.Frame(self.__newwindow)
            frame.grid(row=i, column=2)

            #Allow entries to sweep a piezo
            if self.piezo_sweep_num.get() != "No Sweep":
                if i == int(self.piezo_sweep_num.get()):
                    self.piezo_sweep_bool = True
                    self.piezo_sweep_ind = i

                    dc_text_start = tk.Label(frame_col1, text="Duty Cycle Start: ")
                    self.dc_entry_start = tk.Entry(frame_col1)
                    self.dc_entry_start.insert(tk.END, '0')
                    dc_text_end = tk.Label(frame, text="Duty Cycle End: ")
                    self.dc_entry_end = tk.Entry(frame)
                    self.dc_entry_end.insert(tk.END, '100')
                    dc_text_num = tk.Label(frame, text="Number of points: ")
                    self.dc_entry_num = tk.Entry(frame)
                    self.dc_entry_num.insert(tk.END, '100')

                    dc_text_start.pack(side=tk.LEFT, padx=5, pady=5)
                    self.dc_entry_start.pack(side=tk.LEFT, pady=5, fill=tk.X, expand=True)
                    dc_text_end.pack(side=tk.LEFT, padx=5, pady=5)
                    self.dc_entry_end.pack(side=tk.LEFT, pady=5, fill=tk.X, expand=True)
                    dc_text_num.pack(side=tk.LEFT, padx=5, pady=5)
                    self.dc_entry_num.pack(side=tk.LEFT, pady=5, fill=tk.X, expand=True)

                else:
                    dc_text = tk.Label(frame_col1, text="Duty Cycle Value: ")
                    dc_entry = tk.Entry(frame_col1)
                    dc_entry.insert(tk.END, '0')
                    dc_text.pack(side=tk.LEFT, padx=5, pady=5)
                    dc_entry.pack(side=tk.LEFT, pady=5, fill=tk.X, expand=True)
                    self.dc_entries.append(dc_entry)

            else:
                dc_text = tk.Label(frame_col1, text="Duty Cycle Value: ")
                dc_entry = tk.Entry(frame_col1)
                dc_entry.insert(tk.END, '0')
                dc_text.pack(side=tk.LEFT, padx=5, pady=5)
                dc_entry.pack(side=tk.LEFT, pady=5, fill=tk.X, expand=True)
                self.dc_entries.append(dc_entry)

            self.opto_entries.append(opto_entry)
            self.channel_entries.append(channel_entry)

        range_piezo_num = range(self.__piezo_num)
        range_piezo_num = list(map(str, range_piezo_num))
        self.piezo_dropdown = ['No Sweep'] + range_piezo_num

        #Creates the dropdown window to input which piezo to sweep
        frame = tk.Frame(self.__newwindow)
        frame.grid(row=self.__piezo_num)
        change_volt_button = tk.Button(frame, text="Output Duty Cycles", command=self.outputDC)
        piezo_sweep_option = tk.OptionMenu(frame, self.piezo_sweep_num, *self.piezo_dropdown,
                                      command=lambda _: self.__refresh_newwindow())
        change_volt_button.pack(side=tk.LEFT, padx=5, pady=5)
        piezo_sweep_option.pack(side=tk.LEFT, padx=5, pady=5)

        #Allows the enter key to send data to the Raspberry Pi
        self.__newwindow.bind("<Key>", self.__piezokey)
        self.__newwindow.after(1, lambda: self.__newwindow.focus_force())

    def __refresh_newwindow(self):
        """
        Recreate the window with the new GUI for looping.
        """
        for widget in self.__newwindow.winfo_children():
            widget.destroy()
        self.makePiezoWindow()

    def __piezokey(self, event):
        if event.char == '\r': #ENTER KEY
            self.outputDC()

    def __pause_start(self):
        """
        This changes the live-feed status when video is paused/started.
        """
        self.__pause = not(self.__pause)
        if self.__pause == False:
            self.__pauselabel['text'] = 'LIVE'
            self.__an.event_source.start()
        elif self.__pause == True:
            self.__pauselabel['text'] = 'PAUSED'
            self.__an.event_source.stop()


    def __key(self, event):
        """
        Pauses a video with 'p' key is pressed.
        Saves an image when 'enter' or 'return' key is pressed.
        """
        if event.char == 'p':
            self.__pause_start()
        img = self.cam.grab_image()

        if event.char == 'a':
            self.__pause_start()
            self.__collectdata()
            #messagebox.showinfo("SUCCESS!", "Voltage data is collected from the Raspberry Pi!")
            #save_img = Image.fromarray(img, mode='L')  # float32
            #i = self.__checkfile()
            #save_img.save(self.__image_dir + "/image_%s.tif" %i, "TIFF")
            #self.__analyse(file_number=i)
            messagebox.showinfo("SUCCESS!", "Image is analysed!")
            self.__pause_start()

        if event.char == ' ':
            for i in range(len(self.voltages)):
                voltages_str = ['{:f}'.format(x) for x in self.voltages[i]]
                self.write_voltage("voltages.txt", voltages_str)
            messagebox.showinfo('Save Message', "Voltages are saved in voltages.txt")

        if event.char == '\r': #ENTER KEY
            self.__pause_start()
            save_img = Image.fromarray(img, mode='L')  # float32
            i = self.__checkfile()
            save_img.save(self.__image_dir + "/image_%s.tif" %i, "TIFF")
            messagebox.showinfo('Save Message', "image_%s.tif has been saved!" %i)
            self.__pause_start()

    def write_voltage(self, filename, voltages):
        """
        Writes the voltages to end of filename.
        """
        file = open(filename, 'a')
        delimiter = '\t'
        text = delimiter.join(voltages)
        file.write(text + '\n')
        file.close()

    def __checkfile(self):
        """
        Makes sure the new image file do not have the same number as another image.
        Returns a number that is appended onto the name.
        """
        i = -1
        file_exist = True
        while file_exist == True:
            i += 1
            filename = self.__image_dir + "/image_%s.tif" %i
            file_exist = os.path.isfile(filename)
        return i

    def refreshimage(self, anim_number):
        """
        Refreshes the live-feed.
        """
        if self.__pause == False:
            img = self.cam.grab_image()
            self.im.set_data(img)
            return img
        return

    def outputDC(self):
        """
        Outputs duty cycle, optoswitch numbers and PWM channels to the PI to turn on the circuit.
        Measures were taken to prevent duty cycles from exceeding the range (0 to 100)
        """
        dc_list = list(map(lambda entry: entry.get(), self.dc_entries))
        opto_list = list(map(lambda entry: entry.get(), self.opto_entries))
        channel_list = list(map(lambda entry: entry.get(), self.channel_entries))
        if self.piezo_sweep_bool:
            dc_start = self.dc_entry_start.get()
            dc_end = self.dc_entry_end.get()
            dc_num = self.dc_entry_num.get()
            try:
                sweep_info = [dc_start, dc_end, dc_num]
                dc_start = float(dc_start)
                dc_end = float(dc_end)
                dc_num = int(dc_num)
                sweep_text = '-'.join(sweep_info)
                if dc_start > dc_end or dc_end > 100 or dc_start < 0 or dc_num < 0:
                    messagebox.showinfo("ERROR", "One of the inputs is not within range")
                    return
            except ValueError:
                messagebox.showinfo("ERROR", "One of the inputs is not a number")
                return

        for i in range(self.__piezo_num):
            try:
                channel_list[i] = int(channel_list[i])
                opto_list[i] = int(opto_list[i])
                if self.piezo_sweep_bool:
                    if i < self.__piezo_num - 1:
                        dc_list[i] = float(dc_list[i])
                        if dc_list[i] < 0 or dc_list[i] > 100:
                            messagebox.showinfo("ERROR", "An duty cycle input is not within range")
                            return
            except ValueError:
                messagebox.showinfo("ERROR", "One of the inputs is not a number")
                return

        channel_list = list(map(str, channel_list))
        opto_list = list(map(str, opto_list))
        dc_list = list(map(str, dc_list))

        if self.piezo_sweep_bool:
            dc_list.insert(self.piezo_sweep_ind, sweep_text)

        ch_text = ':'.join(channel_list)
        dc_text = ':'.join(dc_list)
        opto_text = ':'.join(opto_list)

        print("Duty Cycle List: ")
        print(dc_list)

        stdin, stdout, stderr = self.__client.exec_command('python /home/pi/circuit_data_test/ssh_run.py %s %s %s' %(ch_text, dc_text, opto_text))
        print("stderr feedback:")
        print(stderr.readlines())
        messagebox.showinfo("SUCCESS!", "Info is sent to the Raspberry Pi to be processed!")

    def __collectdata(self):
        """
        Gets the voltages from the Raspberry Pi and reads the last voltage.
        """
        stdin, stdout, stderr = self.__client.exec_command('python /home/pi/circuit_data_test/ssh_run.py')
        time.sleep(1)
        ftp = self.__client.open_sftp()
        file = ftp.file('/home/pi/circuit_data_test/voltages.txt', "r", -1)
        lines = file.readlines()[-1]
        voltages = lines.split('\t')
        voltages = list(map(float, voltages))
        self.voltages.append(voltages)
        file.close()
        ftp.close()

    def __analyse(self, file_number, vertical_fringes=False):
        """
        The idea was to take an image from Michelson interferometry and analyse the image instantly.
        """
        # DETAILS OF THE IMAGES
        folder = self.__image_dir
        base_name = 'image_'
        file_ext = '.tif'

        no_of_repeats = 1
        no_of_images = 1

        if vertical_fringes == False:
            max_space = 1024
            x = np.arange(1024)
            xlen = 1024
        else:
            max_space = 1280
            x = np.arange(1280)
            xlen = 1280

        # crop_intervals = max_space / (no_of_repeats + 1)
        # crop_spacing = np.arange(0, max_space, crop_intervals)

        # LISTS OF PARAMETERS FROM FITTING
        amp_values = np.zeros((no_of_images, no_of_repeats))
        k_values = np.zeros((no_of_images, no_of_repeats))
        phase_values = np.zeros((no_of_images, no_of_repeats))
        offset_values = np.zeros((no_of_images, no_of_repeats))

        intensity_values = np.zeros((no_of_images, no_of_repeats, xlen))
        intensity_values_fit = np.zeros((no_of_images, no_of_repeats, xlen))

        file_number_str = str(file_number)
        file_number = 0

        # OPEN .tif FILE
        filename = folder + '/' + base_name + file_number_str + file_ext

        for repeat_number in range(no_of_repeats):
            new_image = func_crop.crop_algorithm(filename, vertical_fringes=vertical_fringes,
                                                 min_crop=200,
                                                 max_crop=300)

            new_image = np.asarray(new_image.convert('L'))
            new_image = func_clean.clean_algorithm(new_image)

            optimised_data = func_optimise.optimise_algorithm(new_image)

            amp_values[file_number, repeat_number] = optimised_data[0]
            k_values[file_number, repeat_number] = optimised_data[1]
            phase_values[file_number, repeat_number] = optimised_data[2]
            offset_values[file_number, repeat_number] = optimised_data[3]

            intensity_values[file_number, repeat_number] = optimised_data[4]
            intensity_values_fit[file_number, repeat_number] = optimised_data[5]

            for u in range(1, len(self.voltages)):
                diff = phase_values[u - 1] - phase_values[u]
                diff_sign = np.sign(diff)
                while abs(diff) > np.pi / 2:
                    phase_values[u] = phase_values[u] + diff_sign * np.pi
                    diff = abs(phase_values[u] - phase_values[u - 1])

        self.phase_values[0].append(mean_std(phase_values)[0])
        self.phase_values[1].append(mean_std(phase_values)[1])

        print(mean_std(phase_values)[0])
        print(self.phase_values)

        # PLOT THE INFORMATION INTO GRAPHS
        for i in range(len(self.voltages)):
            self.axplot.errorbar(self.voltages[i], self.phase_values[0], yerr=self.phase_values[1], fmt='gx-',
                                 label='phase')
        plt.draw()






