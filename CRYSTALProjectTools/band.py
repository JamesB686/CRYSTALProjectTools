from scripts.init import *
import sys
import os

lines = '-------------------------------------------'

print("###########################################")
print("#              BAND PLOTTER               #")
print("###########################################\n")

try:
    argument = sys.argv[1]

except:
    cur_dir = os.listdir(os.getcwd())
    for file in cur_dir:
        if str(file).endswith('.f25'):
            print(file)
    print(lines)
    print('Please select a band file input.')
    user_file = input('Band Output File: ')
    if str(user_file).endswith('.f25'):
        argument = user_file
    else:
        print('ERROR: File must be end with an f25 extension')
        sys.exit(1)

if argument == '--h' or argument == 'help' or argument == '-help' or argument == '-h':

    bands_help()

std_variable_dict = {
    'beta'       :  True,
    'band_num'   :  None,
    'relabel'    :  False,
    'fermi'      :  True,
    'fermi_label':  False,
    'save'       :  False,
    'units'      :  'eV',
    'title'      :  None   
}

print('Standard Band Settings:')
print(lines)
print('\t- beta         :   True')
print('\t- band_num     :   None')
print('\t- relabel      :   False')
print('\t- fermi        :   True')
print('\t- fermi_label  :   False')
print('\t- save         :   False')
print('\t- units        :   eV')
print('\t- title        :   None')
print(lines)

user_std = input('Proceed with Standard Settings? (Yes/No): ').lower()

if user_std == 'yes':
    beta = True
    band_num = None
    relabel = False
    fermi = True
    fermi_label = False
    save = False
    units = 'eV'
    title = None

else:
    print('Please enter the variables to change followed by a comma (,)')
    user_variables = input('Variables to Edit: ').lower()
    temp_variables = []
    for var in str(user_variables).split(','):
        temp_variables.append(var.strip())
        
    for x in temp_variables:
        if x in std_variable_dict:
            new_value = input(f"Enter new value for {x}: ")
            
            if new_value.lower() == 'true':
                new_value = True
            elif new_value.lower() == 'false':
                new_value = False
            elif new_value.lower() == 'none':
                new_value = None
            else:
                new_value = new_value

            std_variable_dict[x] = new_value

        else:
            print(f"Variable {x} is not recognized.")

    beta = std_variable_dict['beta']
    band_num = std_variable_dict['band_num']
    relabel = std_variable_dict['relabel']
    fermi = std_variable_dict['fermi']
    fermi_label = std_variable_dict['fermi_label']
    save = std_variable_dict['save']
    units = std_variable_dict['units']
    title = std_variable_dict['title']

print('Standard Variables Sucessfully Set.')
print(lines)

user_fermi_shift_choice = input('Fermi Shift (Shift fermi line into the mid point between HOMO and LUMO)? (Yes/No): ').lower()

if user_fermi_shift_choice == 'yes':
    user_homo = input('HOMO Energy: ')
    user_lumo = input('LUMO Energy: ')

    user_homo = float(user_homo)
    user_lumo = float(user_lumo)

    user_fermi_shift = []
    user_fermi_shift.append(user_homo)
    user_fermi_shift.append(user_lumo)

elif user_fermi_shift_choice == 'no':
    user_fermi_shift = None

print(lines)
user_highlight_choice = input('Band Highlighting (Yes/No): ').lower()

if user_highlight_choice == 'yes' and beta == True:
    user_alpha_bands = input('Enter alpha band numbers seperated by a comma (,): ')
    user_beta_bands = input('Enter beta band numbers seperated by a comma (,): ')

    user_alpha_list = []
    user_beta_list = []

    if len(str(user_alpha_bands)) > 0:
        for value in str(user_alpha_bands).split(','):
            user_alpha_list.append(int(value))
    
    if len(str(user_beta_bands)) > 0:
        for value in str(user_beta_bands).split(','):
            user_beta_list.append(int(value))

elif user_highlight_choice == 'yes' and beta == False:
    user_bands = input('Enter band numbers seperated by a comma (,): ')

    user_bands_list = []

    if len(str(user_bands)) > 0:
        for value in str(user_bands).split(','):
            user_bands_list.append(int(value))
    
    user_alpha_list = user_bands_list
    user_beta_list = None

elif user_highlight_choice == 'no':
    user_alpha_list = None
    user_beta_list = None

if user_highlight_choice == 'yes':
    user_band_highlight = input('Is band relabelling required so as to select the correct bands for highlighting? (Yes/No): ').lower()    

    if user_band_highlight == 'yes':
        user_band_highlight = True
        user_lower_band = input('Please enter the lower band number: ')

        user_lower_band = int(user_lower_band)

    elif user_band_highlight == 'no':
        user_band_highlight = False

        user_lower_band = None

print(lines)

band_generate = Properties_Object().plot_cry_bands(argument, title=title, beta=beta, band_num=band_num, relabel=relabel, fermi=fermi, 
                                                   fermi_label=fermi_label, save=save, units=units, alpha_band_highlight=user_alpha_list, beta_band_highlight=user_beta_list,
                                                   fermi_shift=user_fermi_shift, highlight_relabel=user_band_highlight, lower_band=user_lower_band)