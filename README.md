This repository has been archived using Zenodo. Anyone can publicly access the artifact via the link [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5109043.svg)](https://doi.org/10.5281/zenodo.5109043).

# TVMfuzz 

## introduction

TVMfuzz is a demo project for fuzzing TVM, a widely-used Deep Learning Compiler, based on the findings in **A Comprehensive Study of Deep Learning Compiler Bugs**. TVMfuzz is capable of analyzing the interrelationship among statements and building test programs given the existing test files in TVM.

This project involves only 3 folders and 1 script.

+ buggyFile: includes 8 bug-triggered programs found by TVMfuzz
+ tests: includes 53 effective test files in TVM for analysis
+ TVMfuzz: includes all the implementation of major features and functions of TVMfuzz
+ run.py: the script for building test programs

After running *run.py*, a new folder named *byproduct* will be created and it contains 3 extra files:

+ asTree.txt: illustrates the AST of test files with the help of Python package *ast*
+ log.txt: records the interrelationship among all involved statements of interest
+ program.py: the generated test program



## Reproducibility

### TVMFuzz

To release reviews from laborious tasks of building experimental environments, we have created a docker image and pushed it to docker hub. The version of TVM installed in our image is 0.7, consistent with the one in our experiments.
You can download the image and reproduce our experiments about TVMfuzz following the **[INSTALL.pdf](https://github.com/anonymousWork000/DLCstudy/blob/master/INSTALL.pdf)** file.



# Dataset

## introduction

This dataset is the basic support for the paper: **A Comprehensive Study of Deep Learning Compiler Bugs**. 

We collected the closed and the merged pull requests that are responsible for fixing bugs from their GitHub repositories over 15 months. In total, we collected 1,361 bug-fixing pull requests and identified 603 bugs, including 318 TVM bugs, 145 Glow bugs, and 140 nGraph bugs.

All the bugs are recorded in the excel table and the bugs of each compiler are displayed in a single worksheet.

## repository

The repositories corresponding to these three compilers are as follows. Since some model loaders of nGraph are in separate repositories, we also collect the related data in the same time period.

TVM ：https://github.com/apache/tvm

Glow: https://github.com/pytorch/glow

nGraph:

https://github.com/NervanaSystems/ngraph

https://github.com/NervanaSystems/ngraph-tf (one model loader of nGraph)

https://github.com/NervanaSystems/ngraph-onnx (one model loader of nGraph)

## information

For each worksheet, the following related information are shown:

- the name of the compiler
- pr_id: short for pull request id
- the title of the pull request(pr)
- the url directed to this pr
- the concrete date when this pr was published
- the number of comments involved
- the number of files involved and their separate names
- the symptom of this bug
- the stage about this bug
- the top root cause of this bug
- sub_causes: short for subcategories of  root causes
- the related framework of the Model Loading bugs

## Plotting
In order to better reproduce the figures in the paper, we provide a drawing scrip (**drawing_script.R**), which can generate all the graphs in our paper. To see the generated graph intuitively, we recommend that you use RStudio to run this script. 
First You just need to download the **dataset** folder in this repository to your computer.

Secondly, you need to run the script(`drawing_script.R`) with RStudio, and then all the figures in our paper will be generated one by one.

Notes: 
1. The dataset file(**dataset.xlsx**) should be placed in the same directory as the **drawing_script.R** file.
2. If the running crash with a message "\`path\` does not exist: ‘dataset.xlsx’", you need set the **working directory** to source file location.

## Citation
Please cite our paper if this work is helpful to you.
```
@inproceedings{10.1145/3468264.3468591,
author = {Shen, Qingchao and Ma, Haoyang and Chen, Junjie and Tian, Yongqiang and Cheung, Shing-Chi and Chen, Xiang},
title = {A Comprehensive Study of Deep Learning Compiler Bugs},
year = {2021},
isbn = {9781450385626},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3468264.3468591},
doi = {10.1145/3468264.3468591},
booktitle = {Proceedings of the 29th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering},
pages = {968–980},
numpages = {13},
keywords = {Deep Learning, Compiler Testing, Empirical Study, Deep Learning Compiler Bug},
location = {Athens, Greece},
series = {ESEC/FSE 2021}
}
```
