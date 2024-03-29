# Jenkins Hunter

Python3 script that uses a queue and threads to concurrently sweep an IP block for unauthenticated Jenkins instances on the default port of 8080.

This script checks for:

1. Jenkins hosts allowing unauthenticated access to the /script console page

2. Jenkins hosts allowing unauthenticated execution of build jobs (which can be used to launch shell commands)

This can be useful for both blue and red teams. From a red team perspective, unauthenticated Jenkins hosts provide quick initial access points for attackers and this script will help find these hosts quicker. From a blue team perspective, this script can be proactively run to identify unauthenticated Jenkins and remediate them before an attacker does.

Since this script uses threading to run faster, you must first check the ulimit set on your host.

You can check the limit of the number of open file handles on your system by running:

ulimit -n

For Mac this number is often around 250. On Kali and other Linux distros this number is usually 1000+.

Since this is opens connections to ports and IPs concurrently, you'll need to set your thread number when promped accordingly.

Generally, I would recommend setting threads to 250 on Mac systems and 1000 on Kali or other Linux distros unless you follow the steps below to up the ulimit cap on your system.

----------------------------------------

Usage:

1. pip3 install -r requirements.txt

2. python3 jenkins-hunter.py

The enter IP block and thread count when prompted.

-----------------------------------------

I have seen good performance when running this script with 1000 threads. On Kali linux distros, you should be able to run it with 1000 threads with no issues or changes needed. If running on Mac, I recommend following the steps below to up the ulimit on Mac to allow for at least 1000 threads:

STEPS TO PERSISTENTLY INCREASE ulimit on Mac and Linux to allow for more threads:

https://unix.stackexchange.com/questions/108174/how-to-persistently-control-maximum-system-resource-consumption-on-mac

----------------------------------------

DISCLAIMER

Use at your own risk. Do not use without the appropriate authorizations.
