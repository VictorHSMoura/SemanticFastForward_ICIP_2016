
[![Version](https://img.shields.io/badge/version-1.0-brightgreen.svg)](http://www.verlab.dcc.ufmg.br/fast-forward-video-based-on-semantic-extraction/#ICIP2016)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](LICENSE)

# Project #

This project is based on the paper [Fast-Forward Video Based on Semantic Extraction](http://www.verlab.dcc.ufmg.br/semantic-hyperlapse/papers/Final_Draft_ICIP_2016_Fast_Forward_Video_Based_on_Semantic_Extraction.pdf) on the **IEEE International Conference on Image Processing** (ICIP 2016). It implements a semantic fast-forward method for First-Person videos.

For more information and visual results, please access the [project page](http://www.verlab.dcc.ufmg.br/fast-forward-video-based-on-semantic-extraction).

## Contact ##

### Authors ###

* Washington Luis de Souza Ramos - MSc student - UFMG - washington.ramos@outlook.com
* Michel Melo da Silva - PhD student - UFMG - michelms@dcc.ufmg.com
* Mario Fernando Montenegro Campos - Advisor - UFMG - mario@dcc.ufmg.br
* Erickson Rangel do Nascimento - Advisor - UFMG - erickson@dcc.ufmg.br

### Institution ###

Federal University of Minas Gerais (UFMG)  
Computer Science Department  
Belo Horizonte - Minas Gerais -Brazil 

### Laboratory ###

![VeRLab](https://www.dcc.ufmg.br/dcc/sites/default/files/public/verlab-logo.png)

**VeRLab:** Laboratory of Computer Vision and Robotics  
http://www.verlab.dcc.ufmg.br

## Code ##

### Dependencies ###

* MATLAB 2015a or higher
* Python 2.7 (*Tested with 2.7.12*)
* MATLAB Engine for Python

### Usage ###

If you don't want to read all the steps, feel free to use the **Quick Guide**. To see it, execute the first step and click on *Help Index* in the *Help* menu.

1.  **Running the Code:**

	Into the _PythonScripts_ directory, run the following command:
```
 user@computer:<project_path/PythonScripts>: python autorun.py
```

2. **Selecting the Video:**
	
	On the main screen, click on *OpenFile* in the *File* menu. Then select the video that you want to accelerate.
```
 The valid formats are: ".mp4" and ".avi"
```

3. **Choosing the SpeedUp:**

	After selecting the video, choose the speed-up that you want to apply.
```
 The speed-up rate needs to be an integer greater than 1.
```

4. **Setting the Weights:**

    4 weights control the way the video will be accelerated. They are:
	
| Weight | Description | Type | 			
|--------:|-------------|------|
| &alpha; | Tuple of weights related to the shakiness term in the edge weight formulation. | _Integer_ |
| &beta; | Tuple of weights related to the velocity term in the edge weight formulation. | _Integer_ |
| &gamma; | Tuple of weights related to the appearance term in the edge weight formulation. | _Integer_ |
| &eta; | Tuple of weights related to the semantic term in the edge weight formulation. | _Integer_ |
	
Select an integer for each weight. The first is for the semantic part and the second one for the non-semantic part. If you don't change anything, the default weights will be used. _That doesn't mean that they are the best for your video._

```
 The general formula is presented in the paper.
```

5. **Speeding-Up the Video:**
	
	After setting everything, click on the `Speed Up Video` button and check the progress on the screen that'll be opened.
