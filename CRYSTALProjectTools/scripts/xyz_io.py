class XYZ_Object:
    def __init__(self):
        pass

    def read_files(self, xyz_output):
        # Function to read the xyz output file
        # Sourced from CRYSTALpytools

        import sys
        import os

        self.file_name = xyz_output

        try:
            # Try to read the file - will exit if no file is specified

            file = open(self.file_name, 'r')
            self.data = file.readlines()
            file.close()

            # Directory path - check if has been specifed and append if

            dir_name = os.path.split(xyz_output)[0]
            dir_name = dir_name + '/'
            self.abspath = os.path.join(dir_name)

            # Set the file name of the file to be read in
            self.file_title = os.path.split(xyz_output)[1]

        except:
            print('EXITING: Please specify the folder path and file name')
            sys.exit(1)
        
    def generate_xyz_file(self, xyz_output):
        # Checks that the output extension and thus file type is .xyz

        import sys

        # Reads in the xyz file as specified in the function

        self.read_files(xyz_output)

        # Checks whether the file type specified is a .xyz and
        # checks that the xyz file is not empty

        if self.file_title[-3:] == 'xyz' and len(self.data) > 0:
            pass
        elif self.file_title[-3:] != 'xyz':
            print('EXITING: Please specify an XYZ file')
            sys.exit(1)
        elif len(self.data) == 0:
            print('EXITING: XYZ File is empty')
            sys.exit(1)
        
        # Checks the length of the xyz file and returns
        # the final iteration of the file.

        data = self.data
        file_title = self.file_title
        abspath = self.abspath

        # Assigns the number of atoms in the molecule

        atom_num = data[0].split()[0]
        data_length = len(data)
        iteration_length = (int(atom_num) + 2)

        # Checks whether there are more than one iterations

        if data_length == iteration_length:
            # Pass if only one iteration in file
            pass
        else:
            # Selects the final iteration and overwrite to data
           data = data[-iteration_length:]

        # Writes the xyz file to a new single file in the same specifed
        # directory

        final_file_name = str(file_title[:-4]) + '_final_iteration.xyz'
        self.xyz_object_file_name = str(file_title[:-4]) + '_xyz_obj'

        with open(abspath + final_file_name, 'w') as f:
            for line in data:
                f.write(line)
        f.close()

        with open('lib/xyz_objects/' + self.xyz_object_file_name, 'w') as f:
            for line in data:
                f.write(line)
        f.close()
    
    def xyz_file_assign(self, xyz_output):

        self.generate_xyz_file(xyz_output)

        file_name = self.xyz_object_file_name

        return file_name
    

    





        



    






        





