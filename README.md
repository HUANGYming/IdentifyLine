# Localization and direction of vessels with semantic segmentation by Unet
[![logo](https://img.shields.io/badge/HUANGYming-projects-orange?style=flat&logo=github)](https://github.com/HUANGYming) 

![](https://img.shields.io/badge/Linux%20build-pass-green.svg?logo=linux) 

![](https://img.shields.io/badge/Python-3.6.13-green.svg?style=social&logo=python) 
![](https://img.shields.io/badge/anaconda-4.12.0-green.svg?style=social&logo=anaconda) 
![](https://img.shields.io/badge/Opencv-4.1.2.30-green.svg?style=social&logo=opencv) 
![](https://img.shields.io/badge/NumPy-1.19.2-green.svg?style=social&logo=NumPy)



## Table of Contents
- [Result](#result)
- [Installation](#installation)
- [Structure](#structure)
- [Usage](#usage)
- [Reference](#reference)
- [License](#license)



## I. Result


### 1. Black line in the undisturbed environment

![1](https://github.com/HUANGYming/IdentifyLine/blob/main/actions/Blackline.png)

### 2. Line on simulated human leg

![2](https://github.com/HUANGYming/IdentifyLine/blob/main/actions/line.gif)

## II. Installation

**Python >= 3.6** ,Recommend to use Anaconda 
```
numpy==1.19.2
Opencv==4.1.2.30
```

## III. Structure
```
IdentifyLine/
    - actions/
    - Blackline.py
    - LineOnleg.py
    - README.md
```
in which:
- `actions/` store the experimental result 
- `Blackline.py` identify the black line in the undisturbed environment
- `LineOnleg.py` identify the line on simulated human leg
- `README.md` contains toturial

## IV. Usage

Set the experimental environment and run the main function directly





## V. Reference

[1] https://github.com/wpddmcmc

## VI. License
[MIT](LICENSE) © CAIR_CAS HUANGYiming



