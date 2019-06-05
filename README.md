# Puppet, go rogue :smiling_imp:

This project is a Proof of Concept to show the importance of securing a Puppet infrastructure. Through this set-up I show how to attack all the clients behind a Puppet server through a change in a module. This attack is possible if:

* you have a **big number of users**, increasing the risk of their credentials to be stolen or missused.
* the **code is external** to the Puppet Server, having the previous users access to it.
* you have **nodes sharing a Puppet server**.

## How to run this POC

To run the code, clone this repository using the next command, so all the submodules are cloned aswell:
```
git clone --recurse-submodules https://github.com/davidmogar/gorogue.git
```
The next step is to get inside of gorogue-server and build a binary for Linux:
```bash
$ cd gorogue
$ cd gorogue-server
$ GOOS=linux go build -o go_build_main_go_linux
```
Once the binary is ready, run the server using Python (v3+):
```bash
$ python3 server.py
🦑       Run '/opt/puppetlabs/bin/puppetserver foreground'
📋       Command copied to the clipboard
🐋       Press Enter to run the container...
root@76a433f900e2:/#
```
Run now the command specified in the output to start a Pupper Server:
```bash
root@76a433f900e2:/# /opt/puppetlabs/bin/puppetserver foreground
...
```
The server is now ready to listen to agent requests:
```bash
$ python3 agent.py
🙋       Hello, I'm agent-bdaemgnzqoxnd
🐋       Press Enter to run the container...
Info: Downloaded certificate for ca from puppet
Info: Downloaded certificate revocation list for ca from puppet
...
```
Finally, run the agent using `--go-rogue` flag to replace the Puppet Server with the custom rogue server:
```bash
$ python3 agent.py --go-rogue
😈       Going rogue
🙋       Hello, I'm rogue-yhghdbghpqdec
🐋       Press Enter to run the container...
Info: Downloaded certificate for ca from puppet
Info: Downloaded certificate revocation list for ca from puppet
...
```
From this point, all the agent configuration requests will return a malicious catalog :smiling_imp:


## Requirements

You will need the next requirements to run this POC (previous versions could work but haven't been tested):

* Docker version 18+
* Go 1.12+
* Python 3+
