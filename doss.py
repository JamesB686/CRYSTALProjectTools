from scripts.init import *
import sys
import os

lines = '-------------------------------------------'

print("###########################################")
print("#              DOSS PLOTTER               #")
print("###########################################\n")


try:
    argument = sys.argv[1]

except:
    cur_dir = os.listdir(os.getcwd())
    for file in cur_dir:
        if str(file).endswith('.f25'):
            print(file)
    print(lines)
    print('Please select a doss file input.')
    user_file = input('DOSS Output File: ')
    if str(user_file).endswith('.f25'):
        argument = user_file
    else:
        print('ERROR: File must be end with an f25 extension')
        sys.exit(1)

if argument == '--h' or argument == 'help' or argument == '-help' or argument == '-h':

    doss_help()

std_variable_dict = {
    'beta'      : True,
    'save'      : False,
    'units'     : 'eV',
    'title'     : None,
}

print('Standard DOSS Settings:')
print(lines)
print('\t- beta         :   True')
print('\t- save         :   False')
print('\t- units        :   eV')
print('\t- title        :   None')
print(lines)

user_std = input('Proceed with Standard Settings? (Yes/No): ').lower()

if user_std == 'yes':
    beta = True
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

user_labels = input('Specify labels for the plot? (Yes/No): ').lower()

if user_labels == 'yes':
    user_plot_label = True

    if beta == True:
        print('Labels are applied to both alpha and beta plots.') 
        print('Therefore if only one extra projection is used, only one label is required (Total labelled automatically)')      
    
    else:
        print('Labels only required for extra projections. Total labelled automatically.')
    
    user_labels_string = input('Enter labels seperated by a comma (,): ')
    user_label_list = []

    for label in str(user_labels_string).split(','):
        user_label_list.append(str(label).strip())

else:
    user_plot_label = False
    user_label_list = None

print(lines)   

doss_generate = Properties_Object().plot_cry_doss(argument, beta=beta, title=title, plot_label=user_plot_label,
                                                  labels=user_label_list, fermi=user_fermi_shift,
                                                  save=save, units=units)
