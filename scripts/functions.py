def xyz_to_cry(xyz_output):
    # Function to convert xyz file to a .crystal file
    # suitable for input into CRYSTAL17

    import os
    import sys
    from lib.atom_dict import atom_dictionary


    file_name = xyz_output
    file_title = os.path.split(xyz_output)[1]
    
    # Check whether the xyz file has been checked and formatted

    if str(file_title[:-4]).endswith('final_iteration'):
        pass
    else:
        print('WARNING: xyz file has not be formatted by generate_xyz_file().')
        print('Do you wish to continue?')
        user_continue = input('Yes/No: ')
        if user_continue == 'Yes':
            pass
        else:
            sys.exit(1)

    # Carry out the file conversion
    file = open(file_name, 'r')
    xyz_data = file.readlines()
    file.close()
    xyz_data = xyz_data[2:]

    crystal_data = []

    # Split the data and append it to the new crystal_data list
    # then rejoin the data and write to a new .cry file

    for string in xyz_data:
        temp_string = string.split(' ')
        for i in temp_string:
            crystal_data.append(atom_dictionary.get(i, i))
        
    crystal_data = ' '.join(crystal_data)
    cry_file = file_name[:-20]
    cry_file_name = str(cry_file) + '_coordinates.cry'
  
    with open(cry_file_name, 'w') as f:
        for line in crystal_data:
            f.write(line)
    f.close()
    

def num_split(data, num_length = 12, line_num = 6):
    # Function to split a .f25 line into individual numbers and append the resulting split 
    # numbers to a list. Useful for data where there are no obvious delimiters between data 
    # in the lines. Here num_length is length of each number and line_num is the number of 
    # numbers in the line.
    
    # While loop iterates through the data and appends the resulting split lines to a list

    line_list = []
    i = 0
    while i < (line_num):
        line_list.append(data[(i*num_length):((i+1)*num_length)])
        i += 1
    
    return line_list


def numpy_array_generator(n_rows, n_columns):
    # Function to initialise a numpy array of zeros of specifed shape.

    import numpy as np

    empty_array = np.zeros((n_rows, n_columns))

    return empty_array


def bands_help():
    # Function to print out all the available arguments for the band plotter with detailed information and default values.

    print("When calling the band plotting function, the command line instruction can be used:\n")
    print("    band /path/to/file/filename.f25\n")

    print("Alternatively, one can simply call the band function, and the program will prompt the file to be entered in.\n")

    print("The program is semi-specific to a particular class of metal complex and therefore should be used appropriately.\n")

    print("The following arguments are available for the band plotting system with their respective default values:\n")

    print("    - beta (True)                   :  Required if the band has been plotted in an unrestricted formalism.")
    print("    - band_num (None)               :  A list of two numbers that specify a range of bands to be plotted.")
    print("    - relabel (None)                :  Single number that specifies the minimum band if that is not the first band evaluated.")
    print("    - fermi (True)                  :  Generates a Fermi line on the plot.")
    print("    - fermi_label (False)           :  Generates the Fermi label in the legend.")
    print("    - save (False)                  :  Saves a copy of the output plot as a PNG file.")
    print("    - units ('eV')                  :  Sets the units of the plot (choice of eV or Ha).")
    print("    - title (None)                  :  Generates a title for the plot.")
    print("    - alpha_band_highlight (None)   :  A list containing the set of alpha bands that wish to be highlighted in the plot.")
    print("    - beta_band_highlight (None)    :  A list containing the set of beta bands that wish to be highlighted in the plot.")
    print("    - highlight_relabel (False)     :  Boolean for relabeling the highlighted bands so that they are commensurate with the band labels.")
    print("    - lower_band (None)             :  Number specifying the lower band to change.\n")

    print("The following values are modifiable, however often only the defaults are necessary.")
    print("Therefore, there is an option to use the default values for the following arguments:\n")

    print("    - beta")
    print("    - band_num")
    print("    - relabel")
    print("    - fermi")
    print("    - fermi_label")
    print("    - save")
    print("    - units")
    print("    - title\n")

    print("The highlighting will be checked via a single user input, which if returned true will open up the highlighting optionality.")

    exit()

def doss_help():
    # Function to print out the available arguments for the doss plotter with detailed information and default values.

    print("###########################################")
    print("#            DOSS PLOTTER HELP            #")
    print("###########################################\n")
    print("When calling the doss plotting function, the command line instruction can be used:\n")
    print("    doss /path/to/file/filename.f25\n")
    print("Alternatively, one can simply call the doss function, and the program will prompt the file to be entered in.\n")
    print("The program is semi-specific to a particular class of metal complex and therefore should be used appropriately.\n")
    print("The following arguments are available for the doss plotting system with their respective default values:\n")
    print("    - beta (True)                   :  Required if the DOSS has been plotted in an unrestricted formalism.")
    print("    - fermi (None)                  :  List of two numbers to move the fermi line by a specifie value.")
    print("    - save (False)                  :  Saves a copy of the output plot as a png file.")
    print("    - units ('eV')                  :  Sets the units of the plot (choice of eV or Ha).")
    print("    - title (None)                  :  Generates a title for the plot.")
    print("    - plot_label (False)            :  Boolean for generating labels for the overlayed plots.")
    print("    - labels (None)                 :  List of labels for the plot.\n")
    print("The following values are modifiable; however, often only the defaults are necessary.")
    print("Therefore, there is an option to use the default values for the following arguments:\n")
    print("    - beta")
    print("    - fermi")
    print("    - save")
    print("    - units")
    print("    - title\n")
    print("The labeling will be checked via a single user input, which if returned true will open up the labeling optionality.")

    exit()
        