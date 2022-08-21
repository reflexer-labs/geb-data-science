## Setup and run 
## For MacOS/LinuxOS
`source env.sh`

`python -m venv venv`

`source venv/bin/activate`

`python -m pip install --upgrade pip`

`python -m pip install -r requirements.txt`

`$export ETH_RPC_URL=<your ETH_RPC_URL> before launching jupyter-lab` 

`jupyter-lab`

## For Bash on WindowsOS
`source env.sh`

`python -m venv venv`

`source venv/Scripts/activate` 

`python -m pip install --upgrade pip`

`python -m pip install -r requirements.txt`

`add ETH_RPC_URL=<your ETH_RPC_URL> as a NEW user variable -> Windows Settings -> Advanced System Settings -> Advanced Tab -> Environment Variables -> User Variables for USER` 

`jupyter-lab`
