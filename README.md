# TVMfuzz  [![DOI](https://sandbox.zenodo.org/badge/369744575.svg)](https://sandbox.zenodo.org/badge/latestdoi/369744575)

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

## dependency and version

TVMfuzz requires Python package ast, astunparse and numpy, also need to install tvm according the instruction [here](https://tvm.apache.org/docs/install/from_source.html) before executing.

By the way, Python version 3.9.1 is required for successful execution.


## Reproducibility

To release reviews from laborious tasks of building experimental environments, we have created a docker image and pushed it to docker hub. The version of TVM installed in our image is 0.7, consistent with the one in our experiments.
You can download the image and reproduce our experiments about TVMfuzz in the following steps:

1)	Input the following commands:

        docker pull mhypony/dlcstudy_tvmfuzz:latest

        docker run -it mhypony/dlcstudy_tvmfuzz:latest /bin/bash

2)	Now you are in our docker container, to eliminate unexpected situations that may corrupt our experiment, you should input the following two commands:

        source /etc/profile

        source activate
  
3)	Now go to the folder called **DLCstudy** and run **run.py**.

5)	Finally, you can check the generated program (**program.py**) in the folder named **byproduct**. 

6)	You can also download the latest version of TVM and compare the difference between executions under TVM 0.7 and TVM latest. If you are lucky, you may find some bugs that we have never found.




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
