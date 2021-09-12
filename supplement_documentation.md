---
title: "Code Supplement Documentation"
subtitle: "for _Reinforcement Learning with General LTL Objectives Is Impossible_"
geometry: margin=2cm
output: pdf_document
mainfont: DejaVuSerif.ttf
sansfont: DejaVuSans.ttf
monofont: DejaVuSansMono.ttf 
mathfont: texgyredejavu-math.otf 
header-includes:
- |
  ```{=latex}
    \usepackage{fontspec}
    \setmainfont{Times Roman}
  ```
---

# Overview

In this code supplement, you will be able to:

* Reproduce the results in Section 5 and Appendix F of the paper.
* Visualize constructed counterexample MDPs for different LTL formulas.

This code supplement has the following directory structure:

```bash
code_supplement
├── Dockerfile                  # For building a Docker image
├── models                      # Stores environment MDP and LTL specifications
│   ├── rl_ltl_pac_paper.ltl    # LTL formula used by Section 5
│   └── rl_ltl_pac_paper.prism  # Environment MDP used in Section 5
├── mungojerrie                 # Modified version of Mungojerrie
├── plots                       # For storing plots
└── rl_ltl_pac.ipynb            # Main notebook for reproduction of experiments
```

The main interface of this supplement is `rl_ltl_pac.ipynb`, which is an IPython notebook that contains all relevant code for reproducing our results. 


# Prerequisites


## Docker

Since this artifact contains native code that needs to be compiled from source, we have prepared a `Dockerfile` script to avoid potential compatibility issues. 
We thus recommend using Docker to execute the artifact.

If you don't have Docker installed, you may follow the [Docker's installation guide](https://docs.docker.com/get-docker/) to install Docker on your machine.

Lastly, if you will be using a virtual Docker environment such as "Docker for Mac", we recommend making sure at least 4 CPU cores and 8GB of RAM are available for running this artifact. You may consult this [StackOverflow answer](https://stackoverflow.com/questions/37871540/how-many-cpus-does-a-docker-container-use#answer-37871814) for more details on how to control the CPU limit.


## Port

The main artifact requires an open port on `8081`.
Please make sure that port `8081` is available on your machine. 

If the port `8081` is not available, you may also modify the last line of `Dockerfile` to substitute all occurrences of `8081` to an available port on your machine. You will also need to perform the same substitution when running any command in this document.


# Running


## Building a Docker Image

Once you have Docker installed, the first step is to build a Docker image.
The `Dockerfile` script takes care of installing all the dependencies and creating this image.
The command below builds an image named `rl_ltl_pac`. 
```bash
cd path/to/code_supplement
docker build -t rl_ltl_pac .
```
Note that building this Docker image takes around 15 mins on our 12-core machine.


## Starting the Main Notebook

Once you have built the Docker image, you can run the following command to start a Jupyter notebook session from within a Docker container.
```bash
docker run -it -p 8081:8081 --rm rl_ltl_pac
```

If the above command succeeds, you should see outputs from a Jupyter notebook similar to the following:
```bash
[.... NotebookApp] 
    
    To access the notebook, open this file in a browser:
        file:///root/.local/share/jupyter/runtime/nbserver-7-open.html
    Or copy and paste one of these URLs:
        http://.....:8081/?token=....
     or http://127.0.0.1:8081/?token=XXXXXXX
```

Then, you may use a browser to open the printed url [http://127.0.0.1:8081/?token=XXXXXXX](http://127.0.0.1:8081/?token=XXXXXXX).
This will bring up a Jupyter notebook session, listing the file directory available to the session.
You may click on the core notebook file `rl_ltl_pac.ipynb` to start running the notebook.

Once you have started the notebook, you may follow the notebook to reproduce the results in the paper. 

# Cleanup

To remove the built Docker image, run:

```bash
docker image rm rl_ltl_pac
```

**Thank you for your attention to this artifact!**
