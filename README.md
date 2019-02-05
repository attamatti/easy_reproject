USAGE: reproject.py &lt;input mrc or pdb&gt; &lt;pixelsize&gt;

outputs: 
a stack of reprojections un .mrcs format
angles.star - the angles of the reprojections.  

Give it a pdb file or mrc file and get reprojections.
If a pdb is given the program will ask the desired resolution and make a simulated density first.

Projections can be made rotating around a specific axis or be RANDOM!
If random angles was selected the angles.star file can be used to apply the same rotations to a different structure for comparison.

The script requires relion_project (from relion) and e2pdb2mrc.py (from eman)
to work.  Edit the script to update their paths. 
