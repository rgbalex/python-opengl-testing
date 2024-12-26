## Steps required for setup:

1. Install Python with PPA

1. Make sure the following are installed on your linux disto

    Note: You will need to make sure you have a valid OpenGL installation. This can be checked by running something akin to `dpkg -L freeglut3-dev` 

    ```bash
    echo Note: Not sure all of these are necessary...
    sudo apt install libjpeg-dev python3.11-dev
    sudo apt-get install libosmesa6
    sudo apt-get install mesa-utils
    sudo apt-get install freeglut3-dev
    ```

1. Install requirements with:
 
    ```bash
    pip install -upgrade pip
    pip install numpy PyOpenGL PyOpenGL-accelerate glfw
    ```
