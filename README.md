# orbitals
 Blender Extension to visualize surfaces representing the probability of finding the electron in a hydrogen atom

This Extension:

1) Computes the normalized wavefunction as a product of its radial and angular components
2) Computes the probability density of the hydrogen atom's wavefunction for a given quantum state (n,l,m)
4) Then uses the Marching cubes algorithm to extract 3D surface data from the probability density data based on specific isosurface values.
5) From the 3D suface data triangulations are generated and the result is a set of vertices and a set of triangular faces.
6) This set of vertices and faces is then used to create a mesh representing the probability of finding the electron in a hydrogen atom at the given quantum state and isolevel. 

You can define the following:
1) n (int): principal quantum number
2) l (int): azimuthal quantum number
3) m (int): magnetic quantum number
4) The grid extent
5) The grid resolution
6) The number of iso levels
7) a0_scale_factor (float): Bohr radius scale factor

Tested in Blender 4.2.0 Stable and 4.3 Alpha.

After installing the Extension (using Install from disk), do the following:
1) Change viewport "Clip End" to 10000
2) Change "Transparent Max Bounces" for Cycles Rendering to at least 10 above the number of isolevels you have defined 
