#! /usr/bin/python


# Matt Iadanza 2014-07-25
# update 2017-02-22

import subprocess
import random
import os
import sys
from subprocess import call


######## UPDATE PATHS TO PDB2MRC AND RELION_PROJECT HERE ######################

pdb2mrc_path = "/fbs/emsoftware2/LINUX/EMAN2.12/bin/e2pdb2mrc.py"
relion_project_path = "/fbs/emsoftware2/LINUX/fbscem/relion3/relion-3.0_beta/build/bin/relion_project"

###############################################################################



#################### no touchy touchy ####################

if os.path.isfile(pdb2mrc_path) == False:
    sys.exit("\nERROR: couldn't find e2pdb2mrc.py -  update the path in the script")


if os.path.isfile(relion_project_path) == False:
    sys.exit("\nERROR: couldn't find relion_project -  update the path in the script")

if len(sys.argv) !=3:
    sys.exit('USAGE: reproject.py <input mrc or pdb> <pixelsize>')

if sys.argv[1].split('.')[1] == 'pdb':
    print('inputted a pdb file')
    res = float(raw_input('what resolution to filter to (A): '))
    box = raw_input('what is the desired boxsize in pixels <x>,<y>,<z>: ')
    
    os.system('{0} {1} {2}.mrc --res {3} --box {4}'.format(pdb2mrc_path,sys.argv[1],sys.argv[1].split('.')[0],res,box))
    file = '{0}.mrc'.format(sys.argv[1].split('.')[0])
elif sys.argv[1].split('.')[1] == 'mrc':
    file = sys.argv[1]
else:
    sys.exit('USAGE: reproject_rln.py <input mrc or pdb> <pixelsize>\nERROR input file needs pdb or mrc extension')
print('Rotate around an axis or random angles?')        
print "1)\tphi\n2)\ttheta\n3)\tpsi\n4)\tRANDOM!\n"
choice = raw_input("Select angle: ")
if choice == "1":
    angle = "phi (rot)"
if choice == "2":
    angle = "theta (tilt)"
if choice == "3":
    angle =  "psi"
if choice in ('1','2','3'):
    delta = float(raw_input("delta %s: " % angle)) 
    angrange = int(raw_input("range (degrees): "))
    numangs = int(angrange/delta)

ext = 'star'
output = open("angles.%s" % ext, "w")
output.write('''data_angles

loop_
_rlnAngleRot #1
_rlnAngleTilt #2
_rlnAnglePsi #3
''')


if choice =="1":
    settheta = float(raw_input("set constant theta (tilt):"))
    setpsi = float(raw_input("set constant psi: "))
    for i in range(1,numangs+2):
        ang = (i-1)*delta    
        output.write ("%s\t%s     %s\n"  %(('%.6s' % ('%.4f' % ang)),('%.6s' % ('%.4f' % settheta)),('%.6s' % ('%.4f' % setpsi))     ))

if choice =="2":
    setphi = float(raw_input("set constant phi (rot):"))
    setpsi = float(raw_input("set constant psi: "))
    for i in range(1,numangs+2):
        ang = (i-1)*delta    
        output.write ("%s     %s     %s\n"  %(('%.6s' % ('%.4f' % setphi)),('%.6s' % ('%.4f' % ang)),('%.6s' % ('%.4f' % setpsi))     ))

if choice =="3":
    setphi = float(raw_input("set constant phi:"))
    settheta = float(raw_input("set constant theta (tilt): "))
    for i in range(1,numangs+2):
        ang = (i-1)*delta    
        output.write ("%s     %s     %s\n"  %(('%.6s' % ('%.4f' % setphi)),('%.6s' % ('%.4f' % settheta)),('%.6s' % ('%.4f' % ang))     ))

if choice == "4":
    numberofrepros = int(raw_input('Number of reprojections: '))
    
    for i in range(1,numberofrepros):
        (phi,theta,psi) = (random.randrange(0,360),random.randrange(0,360),random.randrange(0,360))
        output.write('{0:>3.2f}\t{1:>3.2f}\t{2:>3.2f}\n'.format(phi,theta,psi))

output.close()

#print('relion_project --i {0}.mrc --o reproj --angpix {1} --ang angles.star'.format(sys.argv[1].split('.')[0],sys.argv[2]))
subprocess.call(['{2} --i {0}.mrc --o reproj --angpix {1} --ang angles.star'.format(sys.argv[1].split('.')[0],sys.argv[2],relion_project_path)], shell=True)

        
    
