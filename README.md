# Rundle Retrievers

## The Challenge

To create a program that would find the optimal resource extraction path for up to two drill rigs on a remote island,
while ensuring that local flora and fauna are preserved.

The challenge requires both an optimal algorithm and a visualization that is easy to use for non-programmers.

## Authors

- Grant Achuzia
- Matteo Golin
- Hamnah Quereshi
- Hetarthi Soni

## Requirements

**Language:** Python 3.11

All Python dependencies are listed in the [requirements.txt](./requirements.txt) file.

## Quickstart

**This quick start guide assumes you have already installed Python 3.11 or greater from the
[Python website](https://www.python.org/downloads/)**

**It also assumes that you have clone this project repository from GitHub.**

To start the UI and computation, follow these steps:

- Open your terminal within the project's root directory.
  - You can open it in the file explorer on Windows and type `cmd` in the file explorer's file path bar if you are not
    familiar with opening the terminal and using `cd` to navigate directories.
- Install the project dependencies using `pip install -r requirements.txt`.
  - Note that the `pip install` command may be different on Unix based operating systems. You may need to use `pip3`.
- Run the main application using `py app.py` on Windows, or `python3 app.py` on Linux.
- After a few seconds, you should see an output similar to the following:

```console
* Serving Flask app 'app'
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:8000
Press CTRL+C to quit
```

- CTRL + click on the displayed URL (`http://127.0.0.1:8000`) or paste it into your browser search bar to open the UI.
- You can now click the "Next Day" button on the UI to compute the next step of the simulation.

## Tools & Technologies

<img alt="Python" src="https://img.shields.io/badge/-Python-ffbc03?&logo=Python&style=for-the-badge" /> <img alt="Javascript" src="https://img.shields.io/badge/Javascript-f7df1e?style=for-the-badge&logo=Javascript&logoColor=black"> <img alt="HTML" src="https://img.shields.io/badge/HTML-F05032?style=for-the-badge&logo=html5&logoColor=white"> <img alt="CSS" src="https://img.shields.io/badge/CSS-46a2f1?style=for-the-badge&logo=css3&logoColor=white"> <img alt="Flask" src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white">
