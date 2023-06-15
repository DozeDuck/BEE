import os 
import sys
import getopt
import subprocess
# export EPSHOME where you saved the tools, e.g: export EPSHOME="/home/your_directory/EPS"

args=sys.argv[1:]                                                                   # get arguments from usr's input; filename is sys.arg[0], so args start from [1:]
start = ''
end =''
cutoff = ''
mode = ''
biastep = ''
output_name = ''
sudo_password = ''


#optarg for the input example -c 6 -m 3 -b 1
try:
   opts, args = getopt.getopt(args,"h:s:e:c:m:b:o:p:",["help","start =",          # getopot.getopt(sys.arg, short_option‘-h,-i,-t,-p,etc’, long_option'--help,--input_seq,--receptor)
                                    "end =",                                   # with usr's input e.g -i PLDXPAL -c2, the 'getopt' function can grab them and save them seprately into 'opts' and 'args'
                                    "cutoff ="
                                    "mode =",
                                    "biastep =",
                                    "output_name =",
                                    "sudo_password ="])
except getopt.GetoptError:
   print ('pipline_for_eBDIMS_PD2_SCWRL4.py -s <start.pdb> -e <end.pdb> -c <cutoff> -m <mode> -b <biastep> -o <output_name> -p <sudo_password>')
   sys.exit(2)                                                                      # Exiting the program raises a SystemExit exception, 0 means normal exit, and others are abnormal exits.
 
for opt, arg in opts:                                                               # Generate several pairs of value, e.g: opr,arg = -i,PLDXPAL
   if opt == '-h':
      print ('pipline_for_eBDIMS_PD2_SCWRL4.py -s <start.pdb> -e <end.pdb> -c <cutoff> -m <mode> -b <biastep> -o <output_name> -p <sudo_password>')
      sys.exit()
   elif opt in ("-s", "--start"):
      start = arg
   elif opt in ("-e", "--end"):
      end = arg
   elif opt in ("-c", "--cutoff"):
      cutoff = int(arg)
   elif opt in ("-m", "--mode"):
      mode = int(arg)
   elif opt in ("-b", "--biastep"):
      biastep = int(arg)
   elif opt in ("-o", "--output_name"):
      output_name = arg
   elif opt in ("-p", "--sudo_pw"):
      sudo_password = str(arg)


class EPS:                                                                      # EPS = eBDIMS + PD2 + SCWRL4
    pdbparser   = os.environ['EPSHOME']+"/pdbParser"                            # Told python where are the tools
    eBDIMS      = os.environ['EPSHOME']+"/eBDIMS"
    pd2HOME     = os.environ['EPSHOME']+"/pd2_public-master"
    pd2         = os.environ['EPSHOME']+"/pd2_public-master/bin"
    scwrl4      = os.environ['EPSHOME']+"/scwrl4/Scwrl4"
    start_frame = 'none'
    end_frame   = 'none'  
    cut_off     =  6
    mo_de       =  3
    bia_step    =  1
    out_put     = 'none'
    
 

    
    def __init__(self, startPDB, endPDB, cutOFF, moDE, biaSTEP, outPUT, sudoPW):
        self.start_frame = startPDB  
        self.end_frame   = endPDB 
        self.cut_off     = cutOFF
        self.mo_de       = moDE
        self.bia_step    = biaSTEP
        self.out_put     = outPUT
        self.sudo_pw     = sudoPW
        
        
    def pdbParser(self):
        os.system(self.pdbparser + ' --start ' + self.start_frame +' --target ' + self.end_frame)
        pass
    
    def eBDIMS_general(self):
        os.system(self.eBDIMS + ' start.pdb target.pdb ' + str(self.cut_off) +' ' + str(self.mo_de) + ' ' + str(self.bia_step))
        os.system('mkdir forward ; mv DIMS*pdb ./forward/')
        os.system(self.eBDIMS + ' target.pdb start.pdb ' + str(self.cut_off) +' ' + str(self.mo_de) + ' ' + str(self.bia_step))
        os.system('mkdir reverse ; mv DIMS*pdb ./reverse/')
        pass
    
    def pd2_ca2main(self):
        # forward_step_list = []
        # reverse_step_list = []
        
        # add CA to forward frames
        # a,f = subprocess.getstatusoutput(['ls forward | wc -l'])
        # a,n = subprocess.getstatusoutput(['ls forward'])
        # print(n)
        # for i in range(500, (int(f)+1)*500, 500):
        #     forward_step_list.append(i)
        os.system('count=500 && for i in `ls forward | grep DIMS*`; do mv forward/$i forward/forward_$count; count=$(($count+500)); done')  # 把eBDIMS生成的DIMS_MD000500.pdb等文件改称forwrd_500
        os.system('for i in forward/forward*; do pd2_ca2main --database '+ self.pd2HOME +'/database/ --ca2main:new_fixed_ca --ca2main:bb_min_steps 500 -i $i -o $i.pdb; date; done')  # 使用PD2把forward_500添加骨架CA原子并输出名为foward_500.pdb
        
        # add CA to reverse frames
        # a,r = subprocess.getstatusoutput(['ls reverse | wc -l'])
        # a,m = subprocess.getstatusoutput(['ls reverse'])
        # # print(m)
        # for i in range(500, (int(r)+1)*500, 500):
        #     reverse_step_list.append(i)
        os.system('count=500 && for i in `ls reverse | grep DIMS*`; do mv reverse/$i reverse/reverse_$count; count=$(($count+500)); done')
        os.system('for i in reverse/reverse*; do pd2_ca2main --database '+ self.pd2HOME +'/database/ --ca2main:new_fixed_ca --ca2main:bb_min_steps 500 -i $i -o $i.pdb; date; done')
        pass
    
    def scwrl4_sidechain(self):
        os.system('for i in `ls forward | grep pdb$`; do rm forward/${i%.*}; done')             # 删除PD2中产生的无后缀的forward_文件
        os.system('for i in `ls forward | grep pdb$`; do echo "' +self.sudo_pw + '" | sudo -S ' + self.scwrl4 +' -i forward/$i -o forward/$i.pdb; done') # scwrl4工作
        os.system('rm forward/*0.pdb')                                                          # 删除PD2中生成的forward_.pdb文件，此时仅保留SCWRL4生成的forward_.pdb.pdb文件
        os.system('for i in `ls forward | grep pdb$`; do mv forward/$i forward/${i%.*}; done') # 仅保留forward_.pdb.pdb后缀中的1个.pdb变成forward_.pdb
        
        os.system('for i in `ls reverse | grep pdb$`; do rm reverse/${i%.*}; done')             # 删除PD2中产生的无后缀的forward_文件
        os.system('for i in `ls reverse | grep pdb$`; do sudo "' +self.sudo_pw + '" | sudo -S ' + self.scwrl4 +' -i reverse/$i -o reverse/$i.pdb; done') # scwrl4工作
        os.system('rm reverse/*0.pdb')                                                          # 删除PD2中生成的forward_.pdb文件，此时仅保留SCWRL4生成的forward_.pdb.pdb文件
        os.system('for i in `ls reverse | grep pdb$`; do mv reverse/$i reverse/${i%.*}; done') # 仅保留forward_.pdb.pdb后缀中的1个.pdb变成forward_.pdb

        pass
    
    
    
    

univers = EPS(start,end, cutoff, mode, biastep, output_name, sudo_password)
univers.pdbParser()
univers.eBDIMS_general()
univers.pd2_ca2main()
univers.scwrl4_sidechain()
