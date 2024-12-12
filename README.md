# Hydrogen Wavefunctions & Electron Density orbitals visualization in 3D

An Extension for Blender 3D Fee Software Modeling which allows you to visualize 
electron probability density wave functions in a Hydrogen atom/

Blender 3D is freeware and you can download it here: https://www.blender.org/download/

Extension tested on Blender 4.2 & 4.3 Beta 

### Acknowledgement

This Blender Extension is based on the "Hydrogen Wavefunctions & Electron Density Plots" work which can be found here: https://github.com/ssebastianmag/hydrogen-wavefunctions/

### Execution

* [Dowload Extension zip file from Github:](https://github.com/Niuskir/orbitals/archive/refs/heads/main.zip)
Install Extension in Blender (search Youtube "How to install an Extension in Blender".

After installing the Extension (using option "Install from disk"), do the following:
1) Change viewport "Clip End" to 10000
2) Change "Transparent Max Bounces" for Cycles Rendering to at least 10 above the number of isolevels you have defined

This Extension:

1) Computes the normalized wavefunction as a product of its radial and angular components
2) Computes the probability density of the hydrogen atom's wavefunction for a given quantum state (n,l,m)
4) Then uses the Marching cubes algorithm to extract 3D surface data from the probability density data based on specific isosurface values.
5) From the 3D suface data triangulations are generated and the result is a set of vertices and a set of triangular faces.
6) This set of vertices and faces is then used to create a mesh representing the probability of finding the electron in a hydrogen atom at the given quantum state and isolevel.

To execute: Add > Mesh > Generate Electron Orbitals

---

#### Arguments:

The input arguments of the Extension:

1) n (int): principal quantum number
2) l (int): azimuthal quantum number
3) m (int): magnetic quantum number
4) The grid extent
5) The grid resolution
6) The number of iso levels
7) a0_scale_factor (float): Bohr radius scale factor

---

#### Input args:

|    Parameter    |            Description            | Value |  Constraint   |
|:---------------:|:---------------------------------:|:-----:|:-------------:|
|        n        |  Principal quantum number ($n$)   |   3   |    1 <= n     |
|        l        | Azimuthal quantum number ($\ell$) |   2   | 0 <= l <= n-1 |
|        m        |   Magnetic quantum number ($m$)   |   1   | -l <= m <= l  |
| Grid extent     | The size of the grid used         |  480  |               |
| Grid resolution | The resolution of the grid        |  200  |               |
| Isolevels       | Number of isolevels to generate   |  10   |               |
| a0_scale_factor | Bohr radius scale factor ($a_0$)  |  0.3  |               |


#### Output:

<p align='left'>
  <!-- <img src='https://github.com/ssebastianmag/hydrogen-wavefunctions/blob/edda6d746cbe2163f2e92e1191126d0fe7d6488a/img/(3%2C2%2C1)%5Blt%5D.png' width=60% /> -->
</p>

---

#### Input args:

|    Parameter    |            Description            | Value |  Constraint   |
|:---------------:|:---------------------------------:|:-----:|:-------------:|
|        n        |  Principal quantum number ($n$)   |   3   |    1 <= n     |
|        l        | Azimuthal quantum number ($\ell$) |   2   | 0 <= l <= n-1 |
|        m        |   Magnetic quantum number ($m$)   |   1   | -l <= m <= l  |
| Grid extent     | The size of the grid used         |  480  |               |
| Grid resolution | The resolution of the grid        |  200  |               |
| Isolevels       | Number of isolevels to generate   |  10   |               |
| a0_scale_factor | Bohr radius scale factor ($a_0$)  |  0.3  |               |

#### Output:

<p align='left'>
  <!-- <img src='https://github.com/ssebastianmag/hydrogen-wavefunctions/blob/edda6d746cbe2163f2e92e1191126d0fe7d6488a/img/(3%2C2%2C1)%5Bdt%5D.png' width=60% /> -->
</p>

---

#### Input args:

|    Parameter    |            Description            | Value |  Constraint   |
|:---------------:|:---------------------------------:|:-----:|:-------------:|
|        n        |  Principal quantum number ($n$)   |   3   |    1 <= n     |
|        l        | Azimuthal quantum number ($\ell$) |   2   | 0 <= l <= n-1 |
|        m        |   Magnetic quantum number ($m$)   |   1   | -l <= m <= l  |
| Grid extent     | The size of the grid used         |  480  |               |
| Grid resolution | The resolution of the grid        |  200  |               |
| Isolevels       | Number of isolevels to generate   |  10   |               |
| a0_scale_factor | Bohr radius scale factor ($a_0$)  |  0.3  |               |

#### Output:

<p align='left'>
  <!-- <img src='https://github.com/ssebastianmag/hydrogen-wavefunctions/blob/edda6d746cbe2163f2e92e1191126d0fe7d6488a/img/(4%2C3%2C0)%5Blt%5D.png' width=60% /> -->
</p>

---

#### Input args:

|    Parameter    |            Description            | Value |  Constraint   |
|:---------------:|:---------------------------------:|:-----:|:-------------:|
|        n        |  Principal quantum number ($n$)   |   3   |    1 <= n     |
|        l        | Azimuthal quantum number ($\ell$) |   2   | 0 <= l <= n-1 |
|        m        |   Magnetic quantum number ($m$)   |   1   | -l <= m <= l  |
| Grid extent     | The size of the grid used         |  480  |               |
| Grid resolution | The resolution of the grid        |  200  |               |
| Isolevels       | Number of isolevels to generate   |  10   |               |
| a0_scale_factor | Bohr radius scale factor ($a_0$)  |  0.3  |               |

#### Output:

<p align='left'>
  <!-- <img src='https://github.com/ssebastianmag/hydrogen-wavefunctions/blob/edda6d746cbe2163f2e92e1191126d0fe7d6488a/img/(4%2C3%2C0)%5Bdt%5D.png' width=60% /> -->
</p>

---

#### Input args:

|    Parameter    |            Description            | Value |  Constraint   |
|:---------------:|:---------------------------------:|:-----:|:-------------:|
|        n        |  Principal quantum number ($n$)   |   3   |    1 <= n     |
|        l        | Azimuthal quantum number ($\ell$) |   2   | 0 <= l <= n-1 |
|        m        |   Magnetic quantum number ($m$)   |   1   | -l <= m <= l  |
| Grid extent     | The size of the grid used         |  480  |               |
| Grid resolution | The resolution of the grid        |  200  |               |
| Isolevels       | Number of isolevels to generate   |  10   |               |
| a0_scale_factor | Bohr radius scale factor ($a_0$)  |  0.3  |               |

#### Output:

<p align='left'>
  <!-- <img src='https://github.com/ssebastianmag/hydrogen-wavefunctions/blob/edda6d746cbe2163f2e92e1191126d0fe7d6488a/img/(4%2C3%2C1)%5Bdt%5D.png' width=60% /> -->
</p>

As we examine the electron density plots corresponding to the quantum numbers above, 
we notice that with increasing principal quantum number $n$, 
the complexity of the wavefunction grows Specifically:

- The number of nodes (regions where the probability density is zero) increases.
- The electron's spatial distribution expands, covering larger regions around the nucleus. 
- The overall shape of the atomic orbital becomes more intricate and detailed.

---

#### Input args:

|    Parameter    |            Description            | Value |  Constraint   |
|:---------------:|:---------------------------------:|:-----:|:-------------:|
|        n        |  Principal quantum number ($n$)   |   3   |    1 <= n     |
|        l        | Azimuthal quantum number ($\ell$) |   2   | 0 <= l <= n-1 |
|        m        |   Magnetic quantum number ($m$)   |   1   | -l <= m <= l  |
| Grid extent     | The size of the grid used         |  480  |               |
| Grid resolution | The resolution of the grid        |  200  |               |
| Isolevels       | Number of isolevels to generate   |  10   |               |
| a0_scale_factor | Bohr radius scale factor ($a_0$)  |  0.3  |               |

#### Output:

<p align='left'>
  <!-- <img src='https://github.com/ssebastianmag/hydrogen-wavefunctions/blob/edda6d746cbe2163f2e92e1191126d0fe7d6488a/img/(9%2C6%2C1)%5Bdt%5D.png' width=60% /> -->
</p>

---

#### Input args:

|    Parameter    |            Description            | Value |  Constraint   |
|:---------------:|:---------------------------------:|:-----:|:-------------:|
|        n        |  Principal quantum number ($n$)   |   3   |    1 <= n     |
|        l        | Azimuthal quantum number ($\ell$) |   2   | 0 <= l <= n-1 |
|        m        |   Magnetic quantum number ($m$)   |   1   | -l <= m <= l  |
| Grid extent     | The size of the grid used         |  480  |               |
| Grid resolution | The resolution of the grid        |  200  |               |
| Isolevels       | Number of isolevels to generate   |  10   |               |
| a0_scale_factor | Bohr radius scale factor ($a_0$)  |  0.3  |               |

#### Output:

<p align='left'>
  <!-- <img src='https://github.com/ssebastianmag/hydrogen-wavefunctions/blob/edda6d746cbe2163f2e92e1191126d0fe7d6488a/img/(20%2C10%2C5)%5Bdt%5D.png' width=60% /> -->
</p>

For extremely high quantum numbers, the following effects can be observed:

- The complexity increases even further, resulting in numerous nodes and intricate patterns.
- Evaluating the wavefunction over a vast spatial domain becomes computationally intensive.
- Visualization can become cluttered, making it harder to discern specific details or features.

---
