class Properties_Object():
    def __init__(self):
        pass

    def read_files(self, prop_output):
        # Function to read in a .f25 propeties file
        # Sourced from CRYSTALpytools

        import sys
        import os

        self.file_name = prop_output

        try:
            # Try to read the file - will exit if no file is specified

            file = open(self.file_name, 'r')
            self.data = file.readlines()
            file.close()

            # Directory path - needs to be specified when function is called

            dir_name = os.path.split(prop_output)[0]
            dir_name = dir_name + '/'
            self.abspath = os.path.join(dir_name)

            # Set the file name of the file to be read in
            self.file_title = os.path.split(prop_output)[1]

        except:
            print('EXITING: Please specify the folder path and file name')
            sys.exit(1)

        if str(self.file_title).endswith('.f25') or str(self.file_title) == 'fort.25':
            pass
        else:
            print('ERROR: Please specify a fort.25 output file')
            sys.exit(1)


    def read_cry_bands(self, prop_output, beta=True, fermi=None):
        # Import in a .f25 properties output file and read in the data
        # Data then used to plot the bands.

        from scripts.functions import num_split
        from scripts.functions import numpy_array_generator
        import sys

        # Read in the properties output file and define the data in that file

        self.read_files(prop_output)
        data = self.data

        # This functionality checks the number of bands in the f25 file and 
        # generates two seperate arrays (alpha and beta) if an unrestricted 
        # formulism has been used to generate the wavefunction.

        line_num = []
        
        for i, val in enumerate(data):
            if '-%-' and 'BAND' in val:
                line_num.append(i)

        # Initialise the specification line and define each variable.

        self.spec_line = data[0]
        self.sys_type = self.spec_line[3]
        self.n_bands = int(self.spec_line.split()[1])
        self.n_kpoints = int(self.spec_line.split()[2])
        self.k_point_dis = float((self.spec_line.split()[4])[0:11])
        if fermi == None:
            self.fermi = float((self.spec_line.split()[4])[11:])
        elif type(fermi) == int:
            self.fermi = float(fermi)
        elif type(fermi) == list and len(fermi) == 2:
            self.fermi = float((fermi[0] + fermi[1])/2)
        else:
            print('ERROR: Fermi assignment is incorrect. Please configure the fermi variable correctly.')
            sys.exit(1)
        self.band_min = float((data[1].split()[0])[0:11])
        self.band_energy = num_split(data[1],num_length=12,line_num=2)
        self.band_min = self.band_energy[0]
        self.band_max = self.band_energy[1]

        # Specify the k-point coordinates for each segment.
        
        self.seg_start_kx = int(data[2].split()[0])
        self.seg_start_ky = int(data[2].split()[1])
        self.seg_start_kz = int(data[2].split()[2])
    
        self.seg_end_kx = int(data[2].split()[3])
        self.seg_end_ky = int(data[2].split()[4])
        self.seg_end_kz = int(data[2].split()[5])

        self.seg_start_xyz = (self.seg_start_kx, self.seg_start_ky, self.seg_start_kz) 
        self.seg_end_xyz  = (self.seg_end_kx, self.seg_end_ky, self.seg_end_kz)

        # Iterate through the set of band eigenvalues and add all values to a list struture.
        
        self.band_points = self.n_bands * self.n_kpoints
        data_list = []

        if self.band_points%6 == 0:
            for i, line in enumerate(data):
                if 3 <= i < ((self.band_points//6) + 3):
                    data_line = num_split(line)
                    for x in data_line:
                        data_list.append(x)
        else:
            for i, line in enumerate(data):
                if 3 <= i < ((self.band_points//6) + 3):
                    data_line = num_split(line)
                    for x in data_line:
                        data_list.append(x)
                elif i == ((self.band_points//6) + 3):
                    data_line = num_split(line, line_num=(self.band_points%6))
                    for x in data_line:
                        data_list.append(x)

        # Initialise an empty i x j numpy array where i is the number of bands
        # and j is the number of k-points.

        self.band_matrix = numpy_array_generator(self.n_kpoints, self.n_bands)

        # Add the eigenvalues from the list to the numpy array.

        t = 0
        j = 0
        p = 0

        while 0 <= t <= (self.n_bands - 1):
            self.band_matrix[(j, t)] = (
                float(data_list[p]) - float(self.fermi))
            t += 1
            p += 1
            if t == (self.n_bands):
                t = 0
                j += 1
                continue
            elif j == (self.n_kpoints - 1) and t == (self.n_bands - 1):
                self.band_matrix[(j, t)] = (float(data_line[-1]) - float(self.fermi))
                break

        if len(line_num) == 2 and beta==True:
            # If the wavefunction has been evaluated under an unrestricted formulism
            # both alpha and beta band strructures will need to be extracted and 
            # added to their own seperate numpy arrays.

            self.alpha_band_matrix = self.band_matrix
            beta_start_line = line_num[1] 

            self.spec_line = data[beta_start_line]
            self.sys_type = self.spec_line[3]
            self.n_bands = int(self.spec_line.split()[1])
            self.n_kpoints = int(self.spec_line.split()[2])

            self.k_point_dis = float((self.spec_line.split()[4])[0:11])
            if fermi == None:
                self.fermi = float((self.spec_line.split()[4])[11:])
            elif type(fermi) == int:
                self.fermi = float(fermi)
            elif type(fermi) == list and len(fermi) == 2:
                self.fermi = float((fermi[0] + fermi[1])/2)
            else:
                print('ERROR: Fermi assignment is incorrect. Please configure the fermi variable correctly.')
                sys.exit(1)
            self.band_energy = num_split(data[beta_start_line + 1],num_length=12,line_num=2)
            self.band_min = self.band_energy[0]
            self.band_max = self.band_energy[1]


            # Iterate through the set of band eigenvalues and add all values to a list struture.

            self.band_points = self.n_bands * self.n_kpoints
            data_list = []

            if self.band_points%6 == 0:
                for i, line in enumerate(data):
                    if (beta_start_line + 3) <= i < (beta_start_line + (self.band_points//6) + 3):
                        data_line = num_split(line)
                        for x in data_line:
                            data_list.append(x)
            else:
                for i, line in enumerate(data):
                    if (beta_start_line + 3) <= i < (beta_start_line + (self.band_points//6) + 3):
                        data_line = num_split(line)
                        for x in data_line:
                            data_list.append(x)
                    elif i == (beta_start_line + (self.band_points//6) + 3):
                        data_line = num_split(line, line_num=(self.band_points%6))
                        for x in data_line:
                            data_list.append(x)

            # Initialise an empty i x j numpy array where i is the number of bands
            # and j is the number of k-points.

            self.beta_band_matrix = numpy_array_generator(self.n_kpoints, self.n_bands)

            # Add the eigenvalues from the list to the numpy array.

            t = 0
            j = 0
            p = 0

            while 0 <= t <= (self.n_bands - 1):
                self.beta_band_matrix[(j, t)] = (float(data_list[p]) - float(self.fermi))
                t += 1
                p += 1
                if t == (self.n_bands):
                    t = 0
                    j += 1
                    continue
                elif j == (self.n_kpoints- 1) and t == (self.n_bands - 1):
                    self.beta_band_matrix[(j, t)] = (float(data_line[-1]) - float(self.fermi))
                    break
            
        else:
            pass
        

    def read_cry_doss(self, prop_output, fermi=None):
        # Function to read in the CRYSTAL f25 DOS and PDOS files and 
        # add the eigenvalue data to a numpy array.
        
        from scripts.functions import num_split
        import sys

        # Read in the DOS data.

        self.read_files(prop_output)
        data = self.data

        # Assign each DOS iteration a line number to find for plotting.

        self.line_num = []

        for i, val in enumerate(data):
            if '-%-' and 'DOSS' in val:
                self.line_num.append(i)

        # Initialise a function that reads the density of states data and apppends the information to
        # a numpy array. This function can then be used in the plot cry doss to plot each plot without
        # having to write a function for each DOS part.

        self.doss_dict = {}
        p = 1

        for x in self.line_num:
            self.doss_spec_line = data[x]
            self.e_points = int(self.doss_spec_line.split()[2])
            self.e_point_dis = float((self.doss_spec_line.split()[4])[0:11])
            if fermi == None:
                self.fermi_e = float((self.doss_spec_line.split()[4])[11:])
            elif type(fermi) == int:
                self.fermi_e = float(fermi)
            elif type(fermi) == list and len(fermi) == 2:
                self.fermi_e = float((fermi[0] + fermi[1])/2)
            else:
                print('ERROR: Fermi assignment is incorrect. Please configure the fermi variable correctly.')
                sys.exit(1)
            try:
                self.first_point = float(
                    (data[x + 1].split()[0])[11:])
            except ValueError:
                self.first_point = float(
                    data[x + 1].split()[1])
            self.doss_num = int(data[x + 2].split()[0])

            # With variable information loaded requirement now is to append all the data into a list structure
            # to be read by the plot cry doss function.

            data_start = x + 3

            doss_data = []

            if self.e_points%6 == 0:
                data_lines = int(self.e_points//6) - 1
                for z, num in enumerate(data):
                    while data_start <= z <= data_start + data_lines:
                        data_line = num_split(num)
                        for x in data_line:
                            doss_data.append(float(x.strip()) - self.fermi_e)
            else:
                data_lines = int(int(self.e_points//6))
                for z, num in enumerate(data):
                    if data_start <= z < data_start + data_lines:
                        data_line = num_split(num)
                        for x in data_line:
                            doss_data.append(float(x.strip()) - self.fermi_e)
                    elif z == data_start + data_lines:
                        data_line = num_split(num, line_num=int(self.e_points)%6)
                        for x in data_line:
                            doss_data.append(float(x.strip()) - self.fermi_e)
            
            self.doss_dict[p] = doss_data
            p += 1

    def plot_cry_bands(self, prop_output, beta = True, band_num = None, 
                       relabel = None, fermi = True, fermi_shift=None, fermi_label = False, save=False, 
                       units = 'eV', title=None, alpha_band_highlight=None, 
                       beta_band_highlight=None, highlight_relabel=False, lower_band=None):
        # Function to plot the band structure as formatted by the read cry bands function.
        # Initialised by running the read cry function.
        # Optimizsed for a Jupyter Notebook environment.

        import matplotlib.pyplot as plt
        import matplotlib.font_manager
        import sys

        plt.rcParams['font.family'] = 'serif'  

        if beta == False:
            self.read_cry_bands(prop_output, beta=False, fermi=fermi_shift)
        else:
            self.read_cry_bands(prop_output, beta=True, fermi=fermi_shift)

        # Define alpha and beta matrices for the bands.

        if beta == True:
            try:
                alpha_matrix = self.alpha_band_matrix
                beta_matrix = self.beta_band_matrix
            except:
                print('ERROR: No alpha and beta band matrices detected.')
                print('Ensure that the wavefunction is evaluated within an unrestricted formulism.')
        else:
            band_matrix = self.band_matrix

        if beta == False and beta_band_highlight != None:
            print('ERROR: No beta bands have been detected.')
            print('Please ensure that you do not request beta band highlights.')
            sys.exit(1)
        else:
            pass

        # Ensure that the correct type of variable is selected for the alpha and beta highlights and sort the list.

        if alpha_band_highlight != None and type(alpha_band_highlight) != list:
            print('ERROR: To highlight alpha bands, please ensure that the variable is given as a list.')
            sys.exit(1)
        elif alpha_band_highlight != None and type(alpha_band_highlight) == list:
            alpha_band_highlight.sort()
        else:
            pass

        if beta_band_highlight != None and type(beta_band_highlight) != list:
            print('ERROR: To highlight beta bands, please ensure that the variable is given as a list.')
            sys.exit(1)
        elif beta_band_highlight != None and type(beta_band_highlight) == list:
            beta_band_highlight.sort()
        else:
            pass

        # If highlight relabel is True, relabel the selected bands so that they align with the current band system.

        if alpha_band_highlight != None:
            if highlight_relabel == True and lower_band != None:
                for i in range(len(alpha_band_highlight)):
                    try:
                        alpha_band_highlight[i] = alpha_band_highlight[i] - int(lower_band)
                    except ValueError:
                        print('ERROR: Please specify an integer for the upper band.')
                        sys.exit(1)
            elif highlight_relabel == True and lower_band == None:
                print('ERROR: No upper band specified in input.')
                sys.exit(1)
            else:
                pass

        if beta_band_highlight != None:
            if highlight_relabel == True and lower_band != None:
                for i in range(len(beta_band_highlight)):
                    try:
                        beta_band_highlight[i] = beta_band_highlight[i] - int(lower_band)
                    except ValueError:
                        print('ERROR: Please specify an integer for the upper band.')
                        sys.exit(1)
            elif highlight_relabel == True and lower_band == None:
                print('ERROR: No upper band specified in input.')
                sys.exit(1)
            else:
                pass  

        # Check that the band numbers in the highlight list are below the total number of bands.

        if band_num != None:

            if relabel == None:
                
                if alpha_band_highlight != None:

                    for band in alpha_band_highlight:
                        if band > int(band_num[-1]):
                            print('ERROR: Highlighted bands specified are greater than the total number of bands.')
                            print('Please ensure that the bands selected to be highlighted are less than the total number.')
                            sys.exit(1)

                if beta_band_highlight != None:

                    for band in beta_band_highlight:
                        if band > int(band_num[-1]):
                            print('ERROR: Highlighted bands specified are greater than the total number of bands.')
                            print('Please ensure that the bands selected to be highlighted are less than the total number.')
                            sys.exit(1)
            
            else:

                if alpha_band_highlight != None:
                
                    for band in alpha_band_highlight:
                        if band > int(band_num[-1] - int(relabel)):
                            print('ERROR: Highlighted bands specified are greater than the total number of bands.')
                            print('Please ensure that the bands selected to be highlighted are less than the total number.')
                            sys.exit(1)

                if beta_band_highlight != None:
                    
                    for band in beta_band_highlight:
                        if band > int(band_num[-1] - int(relabel)):
                            print('ERROR: Highlighted bands specified are greater than the total number of bands.')
                            print('Please ensure that the bands selected to be highlighted are less than the total number.')
                            sys.exit(1)

        else:

            if alpha_band_highlight != None:

                for band in alpha_band_highlight:
                    if band > self.n_bands:
                        print('ERROR: Highlighted bands specified are greater than the total number of bands.')
                        print('Please ensure that the bands selected to be highlighted are less than the total number.')
                        sys.exit(1)

            if beta_band_highlight != None:

                for band in beta_band_highlight:
                    if band > self.n_bands:
                        print('ERROR: Highlighted bands specified are greater than the total number of bands.')
                        print('Please ensure that the bands selected to be highlighted are less than the total number.')
                        sys.exit(1)

        # Define the k-point list variable used for plotting the fermi level.

        k_points = []

        for i in range(0, (self.n_kpoints), 1):
            k_points.append(i)

        # Setting for restricted band evaluation

        if beta == False:
            # Plot each individual band into a plt object and then show the overall structure
            # Band number argument used to plot a specfifc range of bands.
            # Relabel argument required if band min does not equal the first band evaluated.

            if band_num == None:
                if alpha_band_highlight == None:
                    t = 0
                    j = 0

                    while j < self.n_bands:
                        t = 0
                        band = []
                        k_point_list = []
                        while t < self.n_kpoints:
                            band.append(band_matrix[t, j])
                            k_point_list.append(t)
                            t += 1
                        plt.plot(k_point_list, band, color='black', linewidth=0.75)
                        j += 1
                else:
                    t = 0
                    j = 0

                    for band_to_highlight in alpha_band_highlight:
                        while j < self.n_bands:
                            t = 0
                            current_band = []
                            k_point_list_current = []

                            while t < self.n_kpoints:
                                current_band.append(band_matrix[t, j])
                                k_point_list_current.append(t)
                                t += 1

                            if j in alpha_band_highlight:
                                plt.plot(k_point_list_current, current_band, color='red', linewidth=1.25)
                            else:
                                plt.plot(k_point_list_current, current_band, color='black', linewidth=0.75)

                            j += 1
            else:
                if relabel == None:
                    if alpha_band_highlight == None:
                        try:
                            t = 0
                            j = int(band_num[0])

                            while j < int(band_num[-1]):
                                t = 0
                                band = []
                                k_point_list = []
                                while t < self.n_kpoints:
                                    band.append(band_matrix[t, j])
                                    k_point_list.append(t)
                                    t += 1
                                plt.plot(k_point_list, band, color='black', linewidth=0.75)
                                j += 1
                        except:
                            print('ERROR: Specified band labels are not within the evaluated band numbers.')
                    else:
                        try:
                            t = 0
                            j = int(band_num[0])

                            for band_to_highlight in alpha_band_highlight:
                                while j < int(band_num[-1]):
                                    t = 0
                                    current_band = []
                                    k_point_list_current = []

                                    while t < self.n_kpoints:
                                        current_band.append(band_matrix[t, j])
                                        k_point_list_current.append(t)
                                        t += 1

                                    if j in alpha_band_highlight:
                                        plt.plot(k_point_list_current, current_band, color='red', linewidth=1.25)
                                    else:
                                        plt.plot(k_point_list_current, current_band, color='black', linewidth=0.75)

                                    j += 1
                        except:
                            print('ERROR: Specified band labels are not within the evaluated band numbers.')
                else:
                    if alpha_band_highlight == None:
                        t = 0
                        j = int(band_num[0] - int(relabel))

                        while j < int(band_num[-1] - int(relabel)):
                            t = 0
                            band = []
                            k_point_list = []
                            while t < self.n_kpoints:
                                band.append(band_matrix[t, j])
                                k_point_list.append(t)
                                t += 1
                            plt.plot(k_point_list, band, color='black', linewidth=0.75)
                            j += 1
                    else:
                        t = 0
                        j = int(band_num[0] - int(relabel))

                        for band_to_highlight in alpha_band_highlight:
                            while j < int(band_num[-1] - int(relabel)):
                                t = 0
                                current_band = []
                                k_point_list_current = []

                                while t < self.n_kpoints:
                                    current_band.append(band_matrix[t, j])
                                    k_point_list_current.append(t)
                                    t += 1

                                if j in alpha_band_highlight:
                                    plt.plot(k_point_list_current, current_band, color='red', linewidth=1.25)
                                else:
                                    plt.plot(k_point_list_current, current_band, color='black', linewidth=0.75)

                                j += 1

            # Variable to set up the Fermi Line on the band plot.

            if fermi == True:

                fermi_list = []
                s = 0

                while s < self.n_kpoints:
                    fermi_list.append(0)
                    s += 1
                plt.plot(k_points, fermi_list, color = 'blue', linewidth=1.25, label='Fermi Energy')
                if fermi_label == True:
                    plt.legend(loc='upper right')
        
            # Set up labels for both x and y axis.
        
            plt.xticks()

            if units == 'eV':

                ev_conv = 27.211386
                plt.ylabel('Energy (eV)')

                ev_band_min = round((float(self.band_min)-float(self.fermi))*ev_conv)
                ev_band_max = round((float(self.band_max)-float(self.fermi))*ev_conv)
                
                # Here locs is the list of ticks and y_labels are the list of labels for the ticks.
                # Locs are given in Ha and labels in eV.   

                locs = []
                y_labels = []

                for i in range(ev_band_min, (ev_band_max + 1), 1):
                    locs.append(int(i)/ev_conv)
                    y_labels.append('{0:.2f}'.format(int(i)))

                plt.yticks(locs, labels=y_labels)

            else:
                plt.ylabel('Energy (Ha)')

            plt.xlabel('k($\pi$/a)')
            plt.xticks(ticks=[0, (float((self.n_kpoints-1))/2), (self.n_kpoints-1)],
                       labels=['-1', '0', '1'])
            if title == None:
                plt.title(self.file_title[:-4])
            else:
                plt.title(str(title))
            plt.legend(loc='upper right')
            plt.show()

        elif beta == True:
            # For unrestricted band plots use the matplotlib subplot formula.

            plt.subplots(1, 2, sharey=True)
            
            plt.subplot(1, 2, 1)
            
            if band_num == None:
                if alpha_band_highlight == None:
                    t = 0
                    j = 0

                    while j < self.n_bands:
                        t = 0
                        band = []
                        k_point_list = []
                        while t < self.n_kpoints:
                            band.append(alpha_matrix[t, j])
                            k_point_list.append(t)
                            t += 1
                        plt.plot(k_point_list, band, color='black', linewidth=0.75)
                        j += 1
                else:
                    t = 0
                    j = 0

                    for band_to_highlight in alpha_band_highlight:
                        while j < self.n_bands:
                            t = 0
                            current_band = []
                            k_point_list_current = []

                            while t < self.n_kpoints:
                                current_band.append(alpha_matrix[t, j])
                                k_point_list_current.append(t)
                                t += 1

                            if j in alpha_band_highlight:
                                plt.plot(k_point_list_current, current_band, color='red', linewidth=1.25)
                            else:
                                plt.plot(k_point_list_current, current_band, color='black', linewidth=0.75)

                            j += 1

            else:
                if relabel == None:
                    if alpha_band_highlight == None:
                        try:
                            t = 0
                            j = int(band_num[0])

                            while j < int(band_num[-1]):
                                t = 0
                                band = []
                                k_point_list = []
                                while t < self.n_kpoints:
                                    band.append(alpha_matrix[t, j])
                                    k_point_list.append(t)
                                    t += 1
                                plt.plot(k_point_list, band, color='black', linewidth=0.75)
                                j += 1
                        except:
                            print('ERROR: Specified band labels are not within the evaluated band numbers.')
                    else:
                        try:
                            t = 0
                            j = int(band_num[0])

                            for band_to_highlight in alpha_band_highlight:
                                while j < int(band_num[-1]):
                                    t = 0
                                    current_band = []
                                    k_point_list_current = []

                                    while t < self.n_kpoints:
                                        current_band.append(alpha_matrix[t, j])
                                        k_point_list_current.append(t)
                                        t += 1

                                    if j in alpha_band_highlight:
                                        plt.plot(k_point_list_current, current_band, color='red', linewidth=1.25)
                                    else:
                                        plt.plot(k_point_list_current, current_band, color='black', linewidth=0.75)

                                    j += 1
                        except:
                            print('ERROR: Specified band labels are not within the evaluated band numbers.')
                else:
                    if alpha_band_highlight == None:
                        t = 0
                        j = int(band_num[0] - int(relabel))

                        while j < int(band_num[-1] - int(relabel)):
                            t = 0
                            band = []
                            k_point_list = []
                            while t < self.n_kpoints:
                                band.append(alpha_matrix[t, j])
                                k_point_list.append(t)
                                t += 1
                            plt.plot(k_point_list, band, color='black', linewidth=0.75)
                            j += 1
                    else:
                        t = 0
                        j = int(band_num[0] - int(relabel))

                        for band_to_highlight in alpha_band_highlight:
                            while j < int(band_num[-1] - int(relabel)):
                                t = 0
                                current_band = []
                                k_point_list_current = []

                                while t < self.n_kpoints:
                                    current_band.append(alpha_matrix[t, j])
                                    k_point_list_current.append(t)
                                    t += 1

                                if j in alpha_band_highlight:
                                    plt.plot(k_point_list_current, current_band, color='red', linewidth=1.25)
                                else:
                                    plt.plot(k_point_list_current, current_band, color='black', linewidth=0.75)

                                j += 1


            # Variable to set up the Fermi Line on the band plot.

            if fermi == True:

                fermi_list = []
                s = 0

                while s < self.n_kpoints:
                    fermi_list.append(0)
                    s += 1
                plt.plot(k_points, fermi_list, color='blue',
                         linewidth=1.25, label='Fermi Energy')
                if fermi_label == True:
                    plt.legend(loc='upper right')

            # Set up labels for both x and y axis.

            if units == 'eV':
                ev_conv = 27.211386
                plt.ylabel('Energy (eV)')

                ev_band_min = round((float(self.band_min)-float(self.fermi))*ev_conv)
                ev_band_max = round((float(self.band_max)-float(self.fermi))*ev_conv)
                
                # Here locs is the list of ticks and y_labels are the list of labels for the ticks.
                # Locs are given in Ha and labels in eV.   

                locs = []
                y_labels = []

                for i in range(ev_band_min, (ev_band_max + 1), 1):
                    locs.append(int(i)/ev_conv)
                    y_labels.append('{0:.2f}'.format(int(i)))

                plt.yticks(locs, labels=y_labels)

            else:
                plt.ylabel('Energy (Ha)')

            plt.xlabel('k($\pi$/a)')
            if self.seg_start_kz != 0:
                plt.xticks(ticks=[0, (float((self.n_kpoints-1))/2), (self.n_kpoints-1)],
                        labels=['-1', '0', '1'])
            else:
                plt.xticks(ticks=[0, (self.n_kpoints-1)], labels=[str(int(self.seg_start_kz)), str(int(self.seg_end_kz))])
            plt.title('Alpha Bands')

            plt.subplot(1, 2, 2)

            if band_num == None:
                if beta_band_highlight == None:
                    t = 0
                    j = 0

                    while j < self.n_bands:
                        t = 0
                        band = []
                        k_point_list = []
                        while t < self.n_kpoints:
                            band.append(beta_matrix[t, j])
                            k_point_list.append(t)
                            t += 1
                        plt.plot(k_point_list, band, color='black', linewidth=0.75)
                        j += 1
                else:
                    t = 0
                    j = 0

                    for band_to_highlight in beta_band_highlight:
                        while j < self.n_bands:
                            t = 0
                            current_band = []
                            k_point_list_current = []

                            while t < self.n_kpoints:
                                current_band.append(beta_matrix[t, j])
                                k_point_list_current.append(t)
                                t += 1

                            if j in beta_band_highlight:
                                plt.plot(k_point_list_current, current_band, color='red', linewidth=1.25)
                            else:
                                plt.plot(k_point_list_current, current_band, color='black', linewidth=0.75)

                            j += 1

            else:
                if relabel == None:
                    if beta_band_highlight == None:
                        try:
                            t = 0
                            j = int(band_num[0])

                            while j < int(band_num[-1]):
                                t = 0
                                band = []
                                k_point_list = []
                                while t < self.n_kpoints:
                                    band.append(beta_matrix[t, j])
                                    k_point_list.append(t)
                                    t += 1
                                plt.plot(k_point_list, band, color='black', linewidth=0.75)
                                j += 1
                        except:
                            print('ERROR: Specified band labels are not within the evaluated band numbers.')
                    else:
                        try:
                            t = 0
                            j = int(band_num[0])

                            for band_to_highlight in beta_band_highlight:
                                while j < int(band_num[-1]):
                                    t = 0
                                    current_band = []
                                    k_point_list_current = []

                                    while t < self.n_kpoints:
                                        current_band.append(beta_matrix[t, j])
                                        k_point_list_current.append(t)
                                        t += 1

                                    if j in beta_band_highlight:
                                        plt.plot(k_point_list_current, current_band, color='red', linewidth=1.25)
                                    else:
                                        plt.plot(k_point_list_current, current_band, color='black', linewidth=0.75)

                                    j += 1
                        except:
                            print('ERROR: Specified band labels are not within the evaluated band numbers.')
                else:
                    if beta_band_highlight == None:
                        t = 0
                        j = int(band_num[0] - int(relabel))

                        while j < int(band_num[-1] - int(relabel)):
                            t = 0
                            band = []
                            k_point_list = []
                            while t < self.n_kpoints:
                                band.append(beta_matrix[t, j])
                                k_point_list.append(t)
                                t += 1
                            plt.plot(k_point_list, band, color='black', linewidth=0.75)
                            j += 1
                    else:
                        t = 0
                        j = int(band_num[0] - int(relabel))

                        for band_to_highlight in beta_band_highlight:
                            while j < int(band_num[-1] - int(relabel)):
                                t = 0
                                current_band = []
                                k_point_list_current = []

                                while t < self.n_kpoints:
                                    current_band.append(beta_matrix[t, j])
                                    k_point_list_current.append(t)
                                    t += 1

                                if j in beta_band_highlight:
                                    plt.plot(k_point_list_current, current_band, color='red', linewidth=1.25)
                                else:
                                    plt.plot(k_point_list_current, current_band, color='black', linewidth=0.75)

                                j += 1

                                
            # Variable to set up the Fermi Line on the band plot.

            if fermi == True:

                fermi_list = []
                s = 0

                while s < self.n_kpoints:
                    fermi_list.append(0)
                    s += 1
                plt.plot(k_points, fermi_list, color='blue',
                         linewidth=1.25, label='Fermi Energy')

            # Set up labels for both x and y axis.
            
            if self.seg_start_kz != 0:
                plt.xticks(ticks=[0, (float((self.n_kpoints-1))/2), (self.n_kpoints-1)],
                        labels=['-1', '0', '1'])
            else:
                plt.xticks(ticks=[0, (self.n_kpoints-1)], labels=[str(int(self.seg_start_kz)), str(int(self.seg_end_kz))])

            plt.xlabel('k($\pi$/a)')
            plt.tick_params(axis='y', left=False)
            plt.title('Beta Bands')

            if title == None:
                plt.suptitle(self.file_title[:-4]) 
            else:
                plt.suptitle(str(title)) 

            plt.show()

        if save == True:
            plt.savefig(prop_output[:-4] + '_band.png')
        else:
            pass

                       
    def plot_cry_doss(self, prop_output, beta = True, title = None, plot_label = False, units = 'eV', labels = None, save=False, fermi=None):
        # Function to plot a DOSS and PDOS figure using data from an f25 file.
        # Data is read in by the read cry doss function.

        import matplotlib.pyplot as plt
        import sys
        
        plt.rcParams['font.family'] = 'serif'  

        # Read in the properties output for the DOSS.

        self.read_cry_doss(prop_output, fermi=fermi)

        # Set up the points on the energy axis

        energy_axis = []
        i = 0
        while i < self.e_points:
            energy_axis.append(
                float((self.first_point - self.fermi_e) + (self.e_point_dis * i)))
            i += 1

        
        doss_dict_len = len(self.doss_dict)
        doss_len = int(doss_dict_len/2)


        if plot_label == True:
            if labels == None:
                print('ERROR: Please specify a list of labels for the DOS plots.')
                sys.exit(0)
            elif (not isinstance(labels, list)):
                print('ERROR: Please specify the labels as a list of labels.')
                sys.exit(0)
            if beta == True:
                if len(labels) != (doss_len - 1):
                    print('ERROR: Number of labels is not the same as number of DOS plots.')
                    sys.exit(0)
            else:
                if len(labels) != doss_dict_len:
                    print('ERROR: Number of labels is not the same as number of DOS plots.')
                    sys.exit(0)

        if beta == True:
            for f in range(1, doss_len, 1):
                dos_axis_alpha = []
                dos_axis_beta = []
                for x in self.doss_dict[f]:
                    dos_axis_alpha.append((float(x)))
                for x in self.doss_dict[f + doss_len]:
                    dos_axis_beta.append((float(x)))
                plt.plot(energy_axis, dos_axis_alpha, label=labels[f-1] + ' (α)', linestyle='--', color='red', linewidth=1)
                plt.plot(energy_axis, dos_axis_beta, label=labels[f-1] + ' (β)', linestyle='--', color='green', linewidth=1)
                if plot_label == True:
                    plt.title(labels[f-1])
            dos_axis_alpha = []
            dos_axis_beta = []
            for x in self.doss_dict[(doss_len)]:
                dos_axis_alpha.append(float(x))
            for x in self.doss_dict[(2*doss_len)]:
                dos_axis_beta.append(float(x))
            plt.plot(energy_axis, dos_axis_alpha, label='Total', color='black', linewidth=0.75)
            plt.plot(energy_axis, dos_axis_beta, color='black', linewidth=0.75)

            
            if units == 'eV':
                plt.xlabel('Energy (eV)')

                ev_conv = 27.211386

                ev_min = round(float(energy_axis[0])*ev_conv)
                ev_max = round(float(energy_axis[-1])*ev_conv)

                locs = []
                y_labels = []

                for i in range(ev_min, (ev_max + 1), 1):
                    locs.append(int(i)/ev_conv)
                    y_labels.append('{0:.2f}'.format(int(i)))

                plt.xticks(locs, labels=y_labels)

                plt.ylabel('Density of States (States/eV/Cell)')

            else:
                plt.xlabel('Energy (Ha)')
                plt.ylabel('Density of States (States/Ha/Cell)')
                
            plt.axvline(x=0, color='blue', linewidth=1)
            if title == None:
                plt.title(None)
            else:
                plt.title(title)
            plt.legend(loc='upper right')
            plt.show()


        elif beta == False:
            for f in self.doss_dict:
                dos_axis = []
                for x in self.doss_dict[f]:
                    dos_axis.append(float(x))
                plt.plot(energy_axis, dos_axis)
                if labels == True:
                    plt.title(labels[f-1])
            plt.show()
        
        if save == True:
            plt.save_fig(str(prop_output)[:-4] + '_doss.png', bbox_inches='tight')  
        else:
            pass     
            
    

            
            
            
            
       

