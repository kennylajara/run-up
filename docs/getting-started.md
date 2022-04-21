# Getting Started with RunUp

## Requirements

You need to have a supported Python version installed on a supported operative system.

* Supported OS: Linux, Windows, MacOS
* Supported Python versions: 3.7, 3.8, 3.9

## Installation

<!--
You can install RunUp from [PyPi](https://pypi.org/project/RunUp/) via PIP with the command:

```
python3 -m pip install runup
```
-->

The installation with PIP will not work as I am still in the process to open source this project. To install it, follow the steps below:

```
# Clone the repo
git clone https://github.com/kennylajara/RunUp.git
# Get into the folder
cd RunUp
# Create and activate environment
python -m venv venv && source venv/bin/activate
# Install development dependencies
pip install -r requirements-dev.txt
# Compile (we are using Cython)
python setup.py build_ext --inplace
# Install package
pip install --editable .
# Test it has been installed successfully
runup --version 
# See how to use the package
runup --help
```

## Basic Example

Here we are going to see a basic example to backup all the files in a directory.

### Basic Setup

To configure RunUp you need to create a file named `runup.yaml` or `runup.yml`. For the simplest configuration, put the code below in the file and place it in the directory containing all the files you want to backup.

```YAML
version: '1'

project:
  example:
    include: 
      - '.'
```

Once you have created the config file, you have to initalize RunUp by executing the following command in the same directory:

```
runup init
```

For details about the meaning of each part of the YAML file and for more advanced setup options visit the [Setup section](setup.md).

### Creating a backup

You can create a new backup by simply executing the following command in the directory where the config file is located:

```
runup backup
```

To see more options visit the [Create Backup section](backup-creation.md).

### Restoring a backup

You can restore the latest by executing the following command from the directory containing the config file:

```
runup restore
```

For more options go to the [Restore Backup section](backup-restoration.md).

## Pro-Tips

### Backup automation

Automating the backup creation is as simple as creating an schedule for the execution of the `runup backup` command. You can do that on Linux and MacOS with Crontab, for Windows you will need to make use of the Task Scheduler. 

How to use the Crontab tool and the Task Scheduler is out of the scope of this documentation but is not so hard to find tutorials on that topic with a simple web search.

### Saving you backup on the cloud

Normally, it is a good idea save a few copies of your backups on different platforms or devices instead of just keeping it local. If you just keep it local and the device fail, well that backup won't be very usefull.

There are many tools syncronize your backups on the cloud but one that we have used and recommend is [RClone](https://rclone.org/). It is a completetly different tool and it has its own documentation.
