You are a high performing AI assistant tasked with helping me on my daily to dos. I need you to know everything about the company I work at Gradient, my role there, and how parallax works + gradient cloud.

Gradient is an AI R&D lab dedicated to building **open intelligence** through a fully decentralized infrastructure, encompassing **distributed training, serving,** verification, simulation, multi-agent systems, and more.

We are solving the hardest and most ambitious problem in the intersection of Blockchain x AI: How do we train/serve good LLMs over public internet —— Is it even possible to build an OpenAI competitor over a permissionless, autonomous network?

Our current stack includes **Parallax** for distributed serving, **Echo** for distributed reinforcement learning, and **Gradient Cloud** for enterprise solutions.

Backed by **top investors** and a team of **world-class researchers**, Gradient is committed to releasing more frontier research that will unlock a future where **intelligence can be assembled, scaled, and evolved by anyone, anywhere**.

News
[2025/10] 🔥 Parallax won #1 Product of The Day on Product Hunt!
[2025/10] 🔥 Parallax version 0.0.1 has been released!
About
A fully decentralized inference engine developed by Gradient. Parallax lets you build your own AI cluster for model inference onto a set of distributed nodes despite their varying configuration and physical location. Its core features include:

Host local LLM on personal devices
Cross-platform support
Pipeline parallel model sharding
Dynamic KV cache management & continuous batching for Mac
Dynamic request scheduling and routing for high performance
The backend architecture:

P2P communication powered by Lattica
GPU backend powered by SGLang
MAC backend powered by MLX LM
User Guide
Installation:
Prerequisites
Python>=3.11.0,<3.14.0
Ubuntu-24.04 for Blackwell GPUs
Below are installation methods for different operating systems.

Operating System	Windows App	From Source	Docker
Windows	✅️	Not recommended	Not recommended
Linux	❌️	✅️	✅️
macOS	❌️	✅️	❌️
From Source
For Linux/WSL (GPU):
Note: If you are using DGX Spark, please refer to the Docker installation section

git clone https://github.com/GradientHQ/parallax.git
cd parallax
pip install -e '.[gpu]'
For macOS (Apple silicon):
We recommend macOS users to create an isolated Python virtual environment before installation.

git clone https://github.com/GradientHQ/parallax.git
cd parallax

# Enter Python virtual environment
python3 -m venv ./venv
source ./venv/bin/activate

pip install -e '.[mac]'
Next time to re-activate this virtual environment, run source ./venv/bin/activate.

Extra step for development:
pip install -e '.[dev]'
Windows Application
Click here to get latest Windows installer.

After installing .exe, right click Windows start button and click Windows Terminal(Admin) to start a Powershell console as administrator.

❗ Make sure you open your terminal with administrator privileges.

Ways to run Windows Terminal as administrator

Start Windows dependencies installation by simply typing this command in console:

parallax install
Installation process may take around 30 minutes.

To see a description of all Parallax Windows configurations you can do:

parallax --help
Docker
For Linux+GPU devices, Parallax provides a docker environment for quick setup. Choose the docker image according to the device's GPU architechture.

GPU Architecture	GPU Series	Image Pull Command
Blackwell	RTX50 series/B100/B200...	docker pull gradientservice/parallax:latest-blackwell
Ampere/Hopper	RTX30 series/RTX40 series/A100/H100...	docker pull gradientservice/parallax:latest-hopper
DGX Spark	GB10	docker pull gradientservice/parallax:latest-spark
Run a docker container as below. Please note that generally the argument --gpus all is necessary for the docker to run on GPUs.

# For Blackwell
docker run -it --gpus all --network host gradientservice/parallax:latest-blackwell bash
# For Ampere/Hopper
docker run -it --gpus all --network host gradientservice/parallax:latest-hopper bash
# For DGX Spark
docker run -it --gpus all --network host gradientservice/parallax:spark-spark bash
The container starts under parallax workspace and you should be able to run parallax directly.

Uninstalling Parallax
For macOS or Linux, if you've installed Parallax via pip and want to uninstall it, you can use the following command:

pip uninstall parallax
For Docker installations, remove Parallax images and containers using standard Docker commands:

docker ps -a               # List running containers
docker stop <container_id> # Stop running containers
docker rm <container_id>   # Remove stopped containers
docker images              # List Docker images
docker rmi <image_id>      # Remove Parallax images
For Windows, simply go to Control Panel → Programs → Uninstall a program, find "Gradient" in the list, and uninstall it.

Getting Started
We will walk through you the easiest way to quickly set up your own AI cluster.

If you have not installed Parallax yet, please refer to the installation guide and follow the instructions.

With Frontend
Step 1: Launch scheduler
First launch our scheduler on the main node, we recommend you to use your most convenient computer for this.

For Linux/macOS:
parallax run
For Windows, start Powershell console as administrator and run:
parallax run
To allow the API to be accessible from other machines, add the argument --host 0.0.0.0 when launching scheduler.

parallax run --host 0.0.0.0
When running parallax run for the first time or after an update, the code version info might be sent to help improve the project. To disable this, use the -u flag:

parallax run -u
Step 2: Set cluster and model config
Open http://localhost:3001 and you should see the setup interface.

Model select

Select your desired node and model config and click continue.

Note: When running in remote mode, Parallax will use a public relay server to help establish connections between the scheduler and nodes. The public relay server will receive the IP information of both the scheduler and the nodes in order to facilitate this connection.

Step 3: Connect your nodes
Copy the generated join command line to your node and run. For remote connection, you can find your scheduler-address in the scheduler logs.

# local area network env
parallax join
# public network env
parallax join -s {scheduler-address}
# example
parallax join -s 12D3KooWLX7MWuzi1Txa5LyZS4eTQ2tPaJijheH8faHggB9SxnBu
Node join

You should see your nodes start to show up with their status. Wait until all nodes are successfully connected, and you will automatically be directed to the chat interface.

When running parallax join for the first time or after an update, the code version info might be sent to help improve the project. To disable this, use the -u flag:

parallax join -u
Step 4: Chat
Done! You have your own AI cluster now.

Chat

Accessing the chat interface from another non-scheduler computer
You can access the chat interface from any non-scheduler computer, not just those running a node server. Simply start the chat server with:

# local area network env
parallax chat
# public network env
parallax chat -s {scheduler-address}
# example
parallax chat -s 12D3KooWLX7MWuzi1Txa5LyZS4eTQ2tPaJijheH8faHggB9SxnBu
After launching, visit http://localhost:3002 in your browser to use the chat interface.

To allow the API to be accessible from other machines, add the argument --host 0.0.0.0 when launching chat interface.

parallax chat --host 0.0.0.0
Without frontend
Step 1: Launch scheduler
First launch our scheduler on the main node.

parallax run -m {model-name} -n {number-of-worker-nodes}
For example:

parallax run -m Qwen/Qwen3-0.6B -n 2
Please notice and record the scheduler ip4 address generated in the terminal.

Step 2: Connect your nodes
For each distributed nodes including the main node, open a terminal and join the server with the scheduler address.

# local area network env
parallax join
# public network env
parallax join -s {scheduler-address}
For example:

# first node
parallax join -s 12D3KooWLX7MWuzi1Txa5LyZS4eTQ2tPaJijheH8faHggB9SxnBu
# second node
parallax join -s 12D3KooWLX7MWuzi1Txa5LyZS4eTQ2tPaJijheH8faHggB9SxnBu
Step 3: Call chat api with Scheduler
curl --location 'http://localhost:3001/v1/chat/completions' --header 'Content-Type: application/json' --data '{
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": "hello"
      }
    ],
    "stream": true
}'
Note: For models such as Qwen3 and gpt-oss, the "reasoning" (or "thinking") feature is enabled by default. To disable it, add "chat_template_kwargs": {"enable_thinking": false} to your request payload.

Skipping Scheduler
Developers can start Parallax backend engine without a scheduler. Pipeline parallel start/end layers should be set manually. An example of serving Qwen3-0.6B with 2-nodes:

First node:
python3 ./parallax/src/parallax/launch.py \
--model-path Qwen/Qwen3-0.6B \
--port 3000 \
--max-batch-size 8 \
--start-layer 0 \
--end-layer 14
Second node:
python3 ./parallax/src/parallax/launch.py \
--model-path Qwen/Qwen3-0.6B \
--port 3000 \
--max-batch-size 8 \
--start-layer 14 \
--end-layer 28
Call chat API on one of the nodes:

curl --location 'http://localhost:3000/v1/chat/completions' --header 'Content-Type: application/json' --data '{
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": "hello"
      }
    ],
    "stream": true
}'
FAQ
Q: When deploying on cloud servers, I encounter an error like "lattica RPC call failed". What does this mean and how can I resolve it?

A: This error typically occurs when the necessary network ports for communication between the scheduler and nodes are blocked—most often due to firewall or security group settings on your cloud platform.

How to fix:

Ensure that the relevant TCP/UDP ports for both the scheduler and nodes are open and accessible between all machines in your cluster.
By default, the scheduler uses HTTP port 3001, and nodes use HTTP port 3000. You can change these with the --port argument (e.g., parallax run --port <your_port> or parallax join --port <your_port>).
For Lattica (node-to-node) communication, random ports are used by default. It is best to explicitly specify which TCP and UDP ports to use (e.g., --tcp-port <your_tcp_port> --udp-port <your_udp_port>), and then open those ports for inbound and outbound traffic in your cloud provider's security settings.
Check your cloud provider's firewall or network security group configurations:
Open inbound rules for the ports mentioned above on all scheduler and node machines.
Make sure that ports are open to the desired sources (e.g., to all cluster instances, or to your public IPs if required).
After updating the firewall/security group settings to allow these ports, restart your scheduler and nodes.

Q: When running on macOS, I encounter the error: error sending packet on iface address No route to host (os error 65) address=192.168.xxx.xxx. What does this mean and how can I fix it?

A: On macOS, you need to allow your terminal or IDE (such as Terminal, iTerm2, VS Code, Cursor, etc.) access to the local network in order for Parallax to work correctly. If the application prompts you for network access the first time you run Parallax, click "Allow." If you have already denied access, follow these steps to enable it:

Open System Settings from the Apple menu.
Click on Privacy & Security in the sidebar.
Click on Local Network.
For each app listed, turn the ability to access your local network on or off using the toggle switch.
This will ensure Parallax has the proper network permissions for local communication.

Q: When running the scheduler on Windows, nodes on other PCs cannot detect the scheduler ID over the local network. Why can't other machines join the cluster?

A: If you are running Parallax in WSL (Windows Subsystem for Linux), make sure you are using the "Mirrored" networking mode. By default, WSL uses "NAT" (Network Address Translation) mode, which isolates your WSL environment behind a virtual network. As a result, services running inside WSL (such as Parallax scheduler) are not directly accessible from other devices on the LAN.

To ensure that other machines on your network can connect to your WSL instance, change the WSL networking mode to "Mirrored" (supported on Windows 11 version 22H2 or later). In "Mirrored" mode, your WSL environment will share the same network as your host, allowing local network discovery and seamless joining of nodes to your Parallax cluster.
