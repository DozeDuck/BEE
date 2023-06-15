class PDBfile:
    atomic_index = []                                                               # each empty list here is to used as the charactors for object.
    atomic_name = []
    residue_name = []
    chain_name = []
    residue_index = []
    X_peratom = []
    Y_peratom = []
    Z_peratom = []
    bfactor_per_factor = []
    charge_per_factor = []
    Atomtype_per_atom = []
    
    # def __init__(self):
        
    
    def PDBreader(self,filename):                                                   # first method to be called in __main__, used for creating object and charactors.
            self.atomic_index.clear()                                                   # cleaveage the information of previous object before put new record into these charactors
            self.atomic_index.clear()
            self.atomic_name.clear()
            self.residue_name.clear()
            self.chain_name.clear()
            self.residue_index.clear()
            self.X_peratom.clear()
            self.Y_peratom.clear()
            self.Z_peratom.clear()
            self.bfactor_per_factor.clear()
            self.charge_per_factor.clear()
            self.Atomtype_per_atom.clear()
            f = open(filename, "r")                                                     # "filename" = $PATH/crankpep_docking_results/PLDAYL_corrected_top_1.pdb
            for line in f:                                                              # iterate each line in file "f"                     
                    
                    if(line.split()[0] == "ATOM" or line.split()[0] == "HETATM"):       # Judgment Sentence，Used to split each row and then determine whether the first column of the row == ATOM or HETATM
                        self.atomic_index.append(float(line.split()[1]))                # The second column is the atomic number
                        self.atomic_name.append(line.split()[2])                        # The 3rd column is the atom name C CA CD1 CD2 and so on
                        self.residue_name.append(line.split()[3])                       # Column 4 is the residue name TYR ALA etc.
                        self.chain_name.append(line.split()[4])                         # The 5th column is the name of the chain it is on
                        self.residue_index.append(int(line.split()[5]))               # The sixth column is the residue number
                        self.X_peratom.append(float(line.split()[6]))                   # Column 7 is the x-coordinate of the atom
                        self.Y_peratom.append(float(line.split()[7]))                   # The 8th column is the Y-coordinate of the atom
                        self.Z_peratom.append(float(line.split()[8]))                   # The ninth column is the Z-coordinate of the atom
                        self.bfactor_per_factor.append(float(line.split()[9]))          # The 10th column is the B-factor of the atom, which is used to judge the activity level
                        # self.charge_per_factor.append(float(line.split()[9]))          # Column 11 is the charge of the residue
                        try:
                            self.Atomtype_per_atom.append(line.split()[10])                 # Column 12 is the atomic type of the atom C, H, O, N, S, CL, etc.
                        except:
                            self.Atomtype_per_atom.append(" ")
                        #print(line)
    # def Alphabet(self):

            
    def Define_Chains(self):
        self.s = list(map(chr, range(ord('a'), ord('z') + 1)))                                   # generate alphabet
        self.s1 = [] 
        for i in self.s:
            self.s1.append(i.upper())
            
        count = 0
        self.num_chains = []
        self.chain_atoms_num = []
        for i in range(len(self.residue_index)):
            if(self.residue_index[i-1] != self.residue_index[i] and self.residue_index[i-1]+1 != self.residue_index[i]):
                # self.num_chains.append(count)
                # self.chain_atoms_num.append(i-1)
                count += 1
                self.chain_name.append(self.s1[count-1])
            else:
                self.chain_name.append(self.s1[count-1])
        
    


    def Resid_Modifier(self, start):
        diff = start - self.residue_index[0]
        for i in range(len(self.residue_index)):
                self.residue_index[i] += diff


    def PDBwriter(self,filename):
        f = open(filename, "w")                                                             # e.g: f = linesplit[0]+"_PO3.pdb"
        for i in range (0 ,len(self.atomic_index)):                                         # Create a loop, i is a sequence starting from 0, and the number of atoms is the length  
            # print("%4s%7d  %-4s%1s%2s%4d    %8.3f%8.3f%8.3f%6.2f%18s" %  ("ATOM" ,     # Formatted output, %4s, right-aligned, the output occupies 4 columns in total. If the length is less than 4 columns, the left end will be filled with spaces. If it is greater than 4 columns, the actual length will be output as a string
            print("%4s%7d  %-4s%1s%2s%4d    %8.3f%8.3f%8.3f%6.2f%18s" %  ("ATOM" ,
                                             self.atomic_index[i],                          # %7d, right-aligned, the output occupies a total of 7 columns, if the length is less than 7 columns, the left end is filled with spaces, signed decimal certificate integer
                                             self.atomic_name[i],                           # %-4s, left-aligned, the output occupies a total of 4 columns, if the length is less than 4 columns, the right end is filled with spaces, if it is greater than 4 columns, the actual length is output as a string
                                             self.residue_name[i],                          # %1s, right-aligned, the output occupies a total of 1 column. If it is less than 1 column, it will be filled with spaces from the left end. If it is greater than 1 column, the actual length will be output as a string
                                             self.chain_name[i],                            # %2s, right-aligned, the output occupies 2 columns in total. If it is less than 2 columns, it will be filled with spaces from the left end. If it is greater than 2 columns, the actual length will be output as a string
                                             self.residue_index[i],                         # %4d, right-aligned, the output occupies a total of 4 columns, if the length is less than 4 columns, the left end is filled with spaces, a signed decimal certificate integer
                                             self.X_peratom[i],                             # %8.3f, right-aligned, the output occupies a total of 8 columns, including 3 decimal places, if the width of the value is less than 8, fill in a space at the left end, decimal
                                             self.Y_peratom[i],                             # %8.3f, right-aligned, the output occupies a total of 8 columns, including 3 decimal places, if the width of the value is less than 8, fill in a space at the left end, decimal
                                             self.Z_peratom[i],                             # %8.3f, right-aligned, the output occupies a total of 8 columns, including 3 decimal places, if the width of the value is less than 8, fill in a space at the left end, decimal
                                             self.bfactor_per_factor[i],                    # %6.2f, right-aligned, the output occupies a total of 6 columns, including 2 decimal places, if the width of the value is less than 6, fill in a space at the left end, decimal
                                             # self.charge_per_factor[i],                    # %6.2f, right-aligned, the output occupies a total of 6 columns, including 2 decimal places, if the width of the value is less than 6, fill in a space at the left end, decimal
                                             self.Atomtype_per_atom[i]), file = f )         # %12s, right-aligned, the output occupies a total of 12 columns, if it is less than 12 columns, it will be filled with spaces from the left end

        print("END", file = f)
        f.close()
