# SpaceZ
Using the gRPC framework, SpaceZ Deep Space Network allows you to launch multiple vehicles into space, deploy their payloads into orbit, and receive data from them.

# Instructions To Run Program
1. This program was written using Python 3.10.3 and it is therefore recommended to use this when running the program. To install, go to the link below.

https://www.python.org/downloads/release/python-3103/

Scroll down to Files and click the Windows installer (64-bit) option. Once the .exe is downloaded, run the installer. On the first window, please check the box at the bottom that says "Add Python 3.10 to PATH" and then click the "Customize installation" option. On the Optional Features page, please ensure all boxes are checked and click Next. On the Advanced Options page, it's recommended to check the "Install for all users" box. Click Install.

2. Once Python 3.10.3 is installed, create a new directory in which you will be cloning this repository into and enter that directory. This can be done with the following command on your command prompt:

mkdir new_directory

3. Once your new directory is created, you can enter it using the command:

cd new_directory

4. Once in this directory, you can clone this repository into your directory with command:

git clone https://github.com/muhammadhraj/SpaceZ.git

5. Now enter the SpaceZ subdirectory with:

cd SpaceZ

6. Now you can install all dependencies for this program with:

pip install -r requirements.txt (If this doesn't work, try replacing "pip" with "pip3")

7. Finally, you're ready to run the program with the command:

python DSN.py (If you get a python command not found error, try replacing "python" with "python3" in this command)

Your SpaceZ Network is now up and running!

When closing the program, please allow a few seconds for the program to close all connections. The program assumes localhost ports 50050-50059 are open. If another process is using any of these ports, please free them before trying to run the DSN.py program.


