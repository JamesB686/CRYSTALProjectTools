class Structure_Object:
    def __init__(self):
        pass

    def read_files(self, xyz_object):
        # Read in an xyz object file and check specifications

        import sys
        import os

        self.file_name = xyz_object

        # Allow file name with or without the xyz_obj extension

        if str(self.file_name).endswith('xyz_obj'):
            file_name = self.file_name
        else:
            file_name = self.file_name + '_xyz_obj'

        try:
            # Try to read the file - will exit if no file within the xyz_object folder
            # is specified

            file = open('bin/xyz_objects/' + file_name, 'r')
            self.data = file.readlines()
            file.close()

        except:
            print('EXITING: Please specify an xyz object file')
            sys.exit(1)

    def generate_empty_array(self, n_atoms):
        # Generates an empty numpy array an associates it with the structure object

        import numpy as np

        self.structure_array = np.zeros((n_atoms, 4))

        return self.structure_array

    def generate_array(self, xyz_object):
        # Reads the xyz object into a numpy array for manipulation

        import numpy as np
        from lib.atom_dict import atom_dictionary

        # Read in the xyz object file

        self.read_files(xyz_object)

        # Modify the xyz file so that only the atomic label and coordinates
        # are present in the final list

        data = self.data
        coordinate_data = data[2:]
        n_atoms = len(coordinate_data)

        split_coordinate_data = []

        # Convert the atom labels into numbers and arange in a numpy array

        for string in coordinate_data:
            temp_string = string.split()
            for i in temp_string:
                if len(i) > 0 and i != '\n':
                    split_coordinate_data.append(atom_dictionary.get(i, i))

        # Initialise an empty numpy array with 4 columns and n_atoms rows
        # and fill the rows with the data from split_coordinate_data

        self.structure_array = np.zeros((int(n_atoms), 4))

        i = 0
        j = 0
        while 0 <= i <= (int(n_atoms)-1):
            self.structure_array[i] = [split_coordinate_data[j], split_coordinate_data[j+1],
                                       split_coordinate_data[j+2], split_coordinate_data[j+3]]
            i += 1
            j += 4

        return self.structure_array

    def object_check(self, display: bool = False):
        # Checks the specified structure object for a generated array

        try:
            structure = self.structure_array
        except:
            if display == False:
                return False
            else:
                print('WARNING: Structure Object is empty')
                return False
        else:
            if display == False:
                return True
            else:
                print('Contents of Selected Structure Object:')
                print('--------------------------------------')
                print(structure)
                return True

    def write_file(self, filename):
        # Writes a list into a .cry coordinate file

        transformed_list = []
        for item in self.structure_array:
            for x in item:
                item_string = ''.join(str(x))
                transformed_list.append(item_string)
                transformed_list.append('\t\t')
            transformed_list.append('\n')

        with open('bin/structure_files/' + filename, 'w') as f:
            for i in transformed_list:
                f.write(i)
        f.close()

        return self.structure_array

    def view_data_frame(self, xyz_object):
        # Returns a pandas data frame with the atom and its three
        # cartesian coordinates.
        # Exports this data frame to a csv format

        import pandas as pd

        self.generate_array(xyz_object)

        struc_df = pd.DataFrame(self.structure_array, columns=[
                                'Atom (Number)', 'X-Coordinate', 'Y-Coordinate', 'Z-Coordinate'])
        struc_df.to_csv('structure_csv/' + self.file_name + '.csv')

    def transform(self, xyz_object, atom_index, atom_number, multiple: bool = False, write: bool = False, filename=None):
        # Function to transform any atomn within the molecule
        # Must know the atom number and atomic number.

        import sys

        # Generate the structure array object

        self.generate_array(xyz_object)

        # Check the atom_index and atom_number inputs are correct for the transformation choice

        if multiple == False:
            if (not isinstance(atom_index, int)) or (not isinstance(atom_number, int)):
                print(
                    'WARNING: For single atom transformations, please use an integer input')
                sys.exit(1)

        elif multiple == True:
            if (not isinstance(atom_index, list)) or (not isinstance(atom_number, list)):
                print(
                    'WARNING: For multiple atom transformations, please use a list input')
                sys.exit(1)

        # Edits the structure array for single or multiple transformations.

        if isinstance(atom_index, int):
            self.structure_array[((atom_index - 1), 0)] = atom_number
        elif isinstance(atom_index, list):
            for i, val in enumerate(atom_index):
                self.structure_array[((val - 1), 0)] = atom_number[i]

        if write == True:
            if filename == None:
                filename = self.file_name + '_transformed_obj'
            self.write_file(filename)
            return self.structure_array
        else:
            return self.structure_array

    def translation(self, x_trans, y_trans, z_trans, molecule: bool = True, xyz_output=None,
                    index_range: bool = False, atom_index=None, write: bool = False, filename=None):
        # This function defines translations for the structure objects
        # Default option is to translate all atoms in the molecule
        # with the same translation vectors
        # This can be changed by changing the molecule option.
        # If molecule is changed to false, then an atom index must be specifed

        # If a transformation has been carried out first then use the transformed
        # structure array

        import numpy as np
        import sys

        if xyz_output == None:
            structure = self.structure_array
        else:
            self.generate_array(xyz_output)
            structure = self.structure_array

        if molecule == True:
            # Translation of entire system

            i = 0
            n_rows = np.shape(structure)[0]
            while 0 <= i <= (n_rows-1):
                structure[(i, 1)] = float(structure[(i, 1)] + x_trans)
                structure[(i, 2)] = float(structure[(i, 2)] + y_trans)
                structure[(i, 3)] = float(structure[(i, 3)] + z_trans)
                i += 1

        elif molecule == False:
            # Check the atom index has been specified correctly for the range choice

            if index_range == False:
                if (not isinstance(atom_index, int)) and (not isinstance(atom_index, list)):
                    print('ERROR: Please define the atom(s) to translate')
                    sys.exit(1)
                else:
                    pass
            elif index_range == True:
                if (not isinstance(atom_index, list)) and len(atom_index) != 2:
                    print(
                        'ERROR: For a range of atoms please specify a start and end point')
                    sys.exit(1)
                else:
                    pass

            if index_range == False:
                if isinstance(atom_index, int):
                    structure[(atom_index, 1)] = float(
                        structure[(atom_index, 1)] + x_trans)
                    structure[(atom_index, 2)] = float(
                        structure[(atom_index, 2)] + y_trans)
                    structure[(atom_index, 3)] = float(
                        structure[(atom_index, 3)] + z_trans)
                elif isinstance(atom_index, list):
                    for x in atom_index:
                        structure[((x-1), 1)] = float(
                            structure[((x-1), 1)] + x_trans)
                        structure[((x-1), 2)] = float(
                            structure[((x-1), 2)] + y_trans)
                        structure[((x-1), 3)] = float(
                            structure[((x-1), 3)] + z_trans)

            if index_range == True:
                range_start = atom_index[0]
                range_end = atom_index[1]
                for x in range(range_start, range_end):
                    structure[((x-1), 1)] = float(
                        structure[((x-1), 1)] + x_trans)
                    structure[((x-1), 2)] = float(
                        structure[((x-1), 2)] + y_trans)
                    structure[((x-1), 3)] = float(
                        structure[((x-1), 3)] + z_trans)

        if write == True:
            if filename == None:
                filename = self.file_name + '_translated_obj'
            self.write_file(filename)
            return structure
        else:
            return structure

    def atom_distance(self, atom_list, xyz_object = None):
        # Function to measure the distance between all pairs of atoms in a list of atoms.
        # Prints out the distances (in A) of all combinations of the list items.

        import sys
        from math import sqrt

        if xyz_object == None:
            structure = self.structure_array
        else:
            self.generate_array(xyz_object)
            structure = self.structure_array

        if (not isinstance(atom_list, list)):
            print('ERROR: Atoms must be specified as a list.')
            sys.exit(0)

        self.final_data = []

        for i in atom_list:
            for x in atom_list:
                if i != x:
                    x_dist = structure[(i-1, 1)] - structure[(x-1, 1)]
                    y_dist = structure[(i-1, 2)] - structure[(x-1, 2)]
                    z_dist = structure[(i-1, 3)] - structure[(x-1, 3)]
                    self.total_dist = '{:.4f}'.format(sqrt((x_dist)**2 + (y_dist)**2 + (z_dist)**2))
                    self.final_data.append(str(i) + ' ------> ' + str(x) + '    -:-    ' + self.total_dist)
        
        for data in self.final_data:
            print(data)
        
        return self.final_data

    def centre_point(self, atom_list, xyz_object = None):
        # Function to return the x, y and z coordinate of the centre point of an aribitary
        # number of points.
        
        import sys
        
        if xyz_object == None:
            structure = self.structure_array
        else:
            self.generate_array(xyz_object)
            structure = self.structure_array

        if (not isinstance(atom_list, list)):
            print('ERROR: Atoms must be specified as a list.')
            sys.exit(0)

        atom_num = len(atom_list)

        x_list = []
        y_list = []
        z_list = []


        for atom in atom_list:
            x_list.append(structure[(atom - 1, 1)])
            y_list.append(structure[(atom - 1, 2)])
            z_list.append(structure[(atom - 1, 3)])
        
            
        x_centre = (sum(x_list))/atom_num
        y_centre = (sum(y_list))/atom_num
        z_centre = (sum(z_list))/atom_num

        print(x_centre)
        print(y_centre)
        print(z_centre)

    def atom_num(self, xyz_object=None, atom_index=1, xyz_return = False, print_option=False):
        # Function to return the number of the atom as well as its xyz coordinates and atom type.

        import sys
        from scripts.functions import numpy_array_generator

        if xyz_object == None:
            try:
                structure = self.structure_array
            except:
                print('ERROR: Please specify an xyz object file.')
                sys.exit(0)
        else:
            self.generate_array(xyz_object)
            structure = self.structure_array

        self.atom_info = structure[int(atom_index)-1, :]

        if xyz_return == False:
            if print_option == True:
                print(self.atom_info)
            else:
                pass

            return self.atom_info
        else:
            self.single_xyz = []
            self.single_xyz.append(structure[(int(atom_index)-1, 1)])
            self.single_xyz.append(structure[(int(atom_index)-1, 2)])
            self.single_xyz.append(structure[(int(atom_index)-1, 3)])
            if print_option == True:
                print(self.single_xyz)
            else:
                pass

            return self.single_xyz
        

    def molecule_centre(self, xyz_object=None, atom_index = True, centre_index=0, write: bool = False, filename=None):
        # Function which translates the molecule so that a specified atom index
        # sits at the origin
        # Note that all atoms are translated by the evaluated amount.

        import numpy as np
        import sys

        if xyz_object == None:
            structure = self.structure_array
        else:
            self.generate_array(xyz_object)
            structure = self.structure_array

        n_rows = np.shape(structure)[0]

        if atom_index == True:
            if centre_index > n_rows:
                print('ERROR: Atom index number does not exist in molecule')
                sys.exit(1)
            if (not isinstance(centre_index, int)):
                print('ERROR: Centre index must be a an atom number')
                sys.exit(0)
        else:
            if (not isinstance(centre_index, list)):
                print('ERROR: Centre index must be a list of x, y, z coordinate.')
                sys.exit(0)
            elif len(centre_index) != 3:
                print('ERROR: Length of centre index list must be 3.')
                sys.exit(0)

        origin = [0, 0, 0]
        x_origin = origin[0]
        y_origin = origin[1]
        z_origin = origin[2]

        if atom_index == True:
            x_trans_vector = x_origin - float(structure[(centre_index, 1)])
            y_trans_vector = y_origin - float(structure[(centre_index, 2)])
            z_trans_vector = z_origin - float(structure[(centre_index, 3)])
        else:
            x_trans_vector = x_origin - float(centre_index[0])
            y_trans_vector = y_origin - float(centre_index[1])
            z_trans_vector = z_origin - float(centre_index[2])

        i = 0
        while 0 <= i <= (n_rows-1):
            structure[(i, 1)] = float(structure[(i, 1)] + x_trans_vector)
            structure[(i, 2)] = float(structure[(i, 2)] + y_trans_vector)
            structure[(i, 3)] = float(structure[(i, 3)] + z_trans_vector)
            i += 1

        if write == True:
            if filename == None:
                filename = self.file_name + '_centred_obj'
            self.write_file(filename)
            return structure
        else:
            return structure

    def azimuthal_evaluation(self, x, y):
        # Defines the azimuthal angle based upon x and y cartesian inputs

        from math import atan
        import math

        if x > 0:
            psi = atan(float(y)/float(x))
        elif x < 0 and y >= 0:
            psi = atan(float(y)/float(x)) + math.pi
        elif x < 0 and y < 0:
            psi = atan(float(y)/float(x)) - math.pi
        elif x == 0 and y > 0:
            psi = (math.pi)/2
        elif x == 0 and y < 0:
            psi = -1*((math.pi)/2)
        else:
            psi = 0

        return psi

    def polar_evaluation(self, x, y, z):
        # Function to evaluate the polar angle

        from math import sqrt
        from math import acos

        r = sqrt(x**2 + y**2 + z**2)

        if z < 0:
            phi = -1*acos(z/r)
        else:
            phi = acos(z/r)

        return phi

    def molecule_stack(self, z_distance, polar_angle, xyz_object=None, centre_index=0, xy_rot = None, write=False, filename=None):
        # Function to shift a molecule such that its centre sits at a polar
        # angle to the origin.
        # Requires the z-distance from the origin to evaluate properly.

        import math
        from math import radians

        self.molecule_centre(xyz_object, centre_index)

        if xy_rot == None:
            pass
        else:
            self.molecule_rot_xy(xyz_object, centre_index)

        self.translation(0, 0, z_distance)

        lat_trans = z_distance*math.tan(radians(90 - polar_angle))
    
        self.translation(0, lat_trans, 0)

        if write == True:
            if filename == None:
                filename = self.file_name + '_' + str(polar_angle) + '_' + str(z_distance) + '_obj'
            self.write_file(filename)
            return self.structure_array
        else:
            return self.structure_array

    def molecule_join(self, molecule_name: tuple, write=False, filename=None):
        # Function to join two molecules into one array
        # This can either be added to a new struture object or append one structure array to another.

        import sys
        import numpy as np

        # Check that molecule name variable has been specified as a tuple.
        
        check = self.object_check()    

        if check == False:          
            try:
                # Generate a new structure array containing the specified molecules.
                self.structure_array = np.concatenate((molecule_name), axis=0)
            except ValueError:
                print('ERROR: Please specify the structure array attribute of the structure object.')
                print('Specified as x.structure_array where x is the structure object.')
                sys.exit(1)
            
        elif check == True:
            try:
                # Generate a new structure array containing the specified molecules.
                self.structure_array = np.concatenate((self.structure_array, molecule_name), axis=0)
            except ValueError:  
                print(
                    'ERROR: Please specify the structure array attribute of the structure object.')
                print('Specified as x.structure_array where x is the structure object.')
                sys.exit(1)
        
        if write == True:
            if filename == None:
                filename = self.file_name + '_joined_obj'
            self.write_file(filename)
            return self.structure_array
        else:
            return self.structure_array
