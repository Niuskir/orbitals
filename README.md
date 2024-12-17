# A Blender 3D extension to visualize Hydrogen Electron Density orbitals in 3D

Blender 3D is freeware and can be downloaded here: https://www.blender.org/download/

Extension tested on Blender 4.2 & 4.3 Beta 

### Acknowledgement

This Blender Extension is based on "Hydrogen Wavefunctions & Electron Density Plots" in Github: https://github.com/ssebastianmag/hydrogen-wavefunctions/. 

### Execution

The Blender Extension is freeware.

* [Dowload Extension zip file from Github:](https://github.com/Niuskir/orbitals/archive/refs/heads/main.zip)

To install the Extension in Blender search Youtube for "How to install an Extension in Blender".

After installing the Extension in Blender:
1) Change 3D Viewport and Camera object "Clip End" options to 5000
2) Change Blender Render Engine to EEVEE

What this Extension does:

1) Computes the normalized wavefunction as a product of its radial and angular components in 3D
2) Computes the probability density of the hydrogen atom's wavefunction for the quantum state (n,l,m) and number of iso levels you entered.
4) Then uses the Marching cubes algorithm to extract 3D surface data from the probability density data based on specific isosurface values.
5) From the 3D suface data triangulations are generated and the result is a set of vertices and a set of triangular faces.
6) This set of vertices and faces is then used to create Blender meshes and objects representing the probability of finding the electron in a hydrogen atom at the given quantum state and isolevel.
7) The extension automatically creates for each iso level a separate material with a customized transparency + color such that you can visualize in 3D where the electron is most likely to be found   
   
To execute the Extension in the Blender Viewport: Add > Mesh > Generate Electron Orbitals

---

#### Extension Arguments:

The input arguments of the Extension:

1) n (int): principal quantum number (default 3)
2) l (int): azimuthal quantum number (default 1)
3) m (int): magnetic quantum number (default 1)
4) The grid extent (int) (default 480) (higher values will increase compute time)
5) The grid resolution (int) (default 400) (higher value will increate compute time)
6) The number of iso levels (int) (default 1)
7) a0_scale_factor (float): Bohr radius scale factor (float) (default 0.4)
8) Delete all generated iso surfaces objects? (boolean)

The Bohr radius scale factor needs to be specified lower as the n value is higher as otherwise the generated iso surface mesh sizes will exceed the grid extent. For example for n=20, l=13, m=8 the scale factor needs to be 0.03  
You can re-run The Extension as many times as you want. It will automatically delete all previous generated
---

For extremely high quantum numbers, the following effects can be observed:

- The complexity increases even further, resulting in numerous nodes and intricate patterns.
- Evaluating the wavefunction over a vast spatial domain becomes computationally intensive.
- Visualization can become cluttered, making it harder to discern specific details or features.

---
