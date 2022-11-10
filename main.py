from tkinter.filedialog import askopenfilename
from os import name, system, chdir, mkdir
from threading import Thread, Semaphore
from datetime import datetime
from pythonping import ping

try:
    mkdir("Results")
except FileExistsError:
    pass

def clearscreen():
    if name == "nt":
        system("cls")
    else:
        system("clear")

clearscreen()

print("Please choose a file with proxies... (1 pr. line)\n")
while True:
    proxy_file = askopenfilename(title = "Please choose a file with proxies... (1 pr. line)")
    try:
        with open(proxy_file, "r") as proxy_file_opened:
            proxies = proxy_file_opened.readlines()
    except FileNotFoundError:
        continue
    except UnicodeDecodeError:
        print("ERROR: Cannot decode proxy file.")
        continue
    else:
        break

while True:
    delimiter = input("What is the delimiter for your proxies? Example: Ip{delimiter}Port\n")
    if delimiter == "":
        continue
    else:
        break

cleaned_proxies = []
for proxy in proxies[:]:
    cleaned_proxies.append(proxy.replace("\n", "", -1))
    proxies = cleaned_proxies.copy()
for proxy in cleaned_proxies[:]:
    if proxy.count(".") != 3 or proxy.count(delimiter) != 1 or len(proxy.split(delimiter)) != 2:
        try:
            cleaned_proxies.remove(proxy)
        except ValueError:
            pass
    try:
        int(proxy.split(":")[1])
    except ValueError:
        try:
            cleaned_proxies.remove(proxy)
        except ValueError:
            pass
    except IndexError:
        try:
            cleaned_proxies.remove(proxy)
        except ValueError:
            pass

print(f"\nProxies loaded:\n{len(cleaned_proxies)}")

while True:
    try:
        timeout = int(input("\nWhat should the timeout be in seconds? (Higher number = Better accuracy) (Reccomend is 5-10)\n"))
    except ValueError:
        continue
    else:
        break

while True:
    try:
        count = int(input("\nHow many times should the proxies be checked? (Higher number = Better accuracy) (Reccomend is 1-2)\n"))
    except ValueError:
        continue
    else:
        break

while True:
    try:
        threadcount = int(input("\nHow many threads should be used for checking? (Reccomended is the total proxies divided by 20)(Higher = Faster checking)\n"))
    except ValueError:
        continue
    else:
        break

clearscreen()

def checkproxy():
    global done
    if done:
        exit()
    global proxy_iter_point
    proxy_iter_point += 1
    global timeout
    global live_proxies
    global dead_proxies
    try:
        proxy = cleaned_proxies[proxy_iter_point - 1]
    except IndexError:
        done = True
        exit()
    except:
        checkproxy()
    try:
        current_response = ping(proxy.split(delimiter)[0], timeout = timeout, count = count)
    except RuntimeError:
        pass
    except OSError:
        pass
    else:
        if current_response.success():
            screenlock.acquire()
            print(f"Good: {proxy}")
            screenlock.release()
            live_proxies.append(proxy)
        else:
            screenlock.acquire()
            print(f"Bad: {proxy}")
            screenlock.release()
            dead_proxies.append(proxy)
    checkproxy()

def getproxy():
    global done
    if done:
        exit()
    global proxy_iter_point
    proxy_iter_point += 1
    try:
        return cleaned_proxies[proxy_iter_point - 1]
    except IndexError:
        done = True
        exit()
    except:
        return "something went wrong"

print("Beggining to check proxies...\n")

live_proxies = []
dead_proxies = []
proxy_iter_point = 0
done = False
screenlock = Semaphore(value=1)

for thread in range(threadcount):
    Thread(target = checkproxy).start()

while done == False:
    pass

if name == "nt":
    chdir(".\\Results")
else:
    chdir(".//Results")

dateandtime = str(datetime.now()).split(".")[0].replace(":", ".", -1)
mkdir(dateandtime)

if name == "nt":
    chdir(f".\\{dateandtime}")
else:
    chdir(f".//{dateandtime}")

with open("Good.txt", "a") as goods_file:
    for item in live_proxies:
        goods_file.write(f"{item}\n")
with open("Bad.txt", "a") as bads_file:
    for item in dead_proxies:
        bads_file.write(f"{item}\n")