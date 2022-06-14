# EC2-Jupyter-Setup.md

EC2 and JupyterLab Setup Instructions from Coding Club #1 and #2

## Coding Club #1

*Original author: Cedric David*

**Create EC2 Instance**

1. https://goto.jpl.nasa.gov/awsconsole 
  a. Log in with JPL credentials
  b. Supply your JPL RSA token (same for VPN): PIN + Token
  d. Ensure the region shown at the top right is “US West (Oregon) us-west-2”
2. Go to EC2 / AMI Catalog / My AMIs(12)
3. De-select “Owned by me”
4. Select one of the JPL-based *EXTERNAL* instances; click “Launch Instance with AMI”.
5. Name and tags: pick a name
6. Key pair (login): Create new key pair (keep all default: Create new key pair, RSA, .pem) Download the file as “KeyPair.pem”
7. Click Launch instance
8. Click on instance and capture the “Private IPv4 addresses xxx.xxx.xx.xx”
9. Got to Mac Terminal:

```bash
chmod 400 KeyPair.pem
ssh -i KeyPair.pem jpluser@xxx.xxx.xx.xx
```

10. Don’t forget to go to “Instance State” and select “Terminate Instance” when you’re done.

## Coding Club #2

**Setup JupyterLab (Single-User)**

1. Start an ec2 instance following the instructions above.
2. Connect to the instance via ssh. 

Remember to set the following parameters appropriately:
* `-i` points the ssh client on your local machine at your pem key to authenticate
* `-L` tunnels traffic on port `9889` between the ec2 instance and your local machine

```shell
ssh -i "KeyPair.pem" jpluser@ec2-x-x-x-x.us-west-2.compute.amazonaws.com -L 9889:localhost:9889
```

OR, perhaps a different user if running an AMI that's not managed by JPL, e.g. `ec2-user` for the Amazon Linux AMI:

```shell
ssh -i "KeyPair.pem" ec2-user@ec2-x-x-x-x.us-west-2.compute.amazonaws.com -L 9889:localhost:9889
```

3. Update packages. Optionally install wget, git, screen etc.

```shell
sudo yum update -y && sudo yum install wget git screen -y
```

4. Download miniconda install script into *tmp/* and execute it with bash. Then, activate the base environment.

```shell
mkdir -p tmp
 
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O tmp/miniconda.sh && \
  bash tmp/miniconda.sh -b -p $HOME/conda && \
  source ~/conda/bin/activate
```

5. Create a new environment called *jupyter* running Python 3.7; activate it; install JupyterLab and other required packages.

```shell
conda create -n jupyter python=3.7 -y && \
  conda activate jupyter && \
  conda install -c conda-forge requests tqdm numpy pandas matplotlib netCDF4 xarray jupyterlab -y
```

6. Start jupyterlab server in a *screen*.

Start a new screen session called *ipylab*:

```shell
screen -S ipylab
```

Use Python to generate and store a hashed password as a shell variable:

```shell
PW="$(python3 -c 'from notebook.auth import passwd; import getpass; print(passwd(getpass.getpass(), algorithm="sha256"))')"
```

Start jupyter lab instance with the following parameters:

```shell
jupyter lab \
    --port=9889 \
    --ip='127.0.0.1' \
    --NotebookApp.token='' \
    --NotebookApp.password="$PW" \
    --notebook-dir="$HOME" \
    --no-browser \
    &
```

Detach the screen by pressing CTRL + A -> D. 

Optionally, append the following line to your `.bash_profile` in order to print the running jupyter servers upon ssh login:

```shell
printf '\n~/conda/envs/jupyter/bin/jupyter server list && echo\n\n' >> .bash_profile
```

7. Access the server through your web browser: http://127.0.0.1:9889/

## Links

* https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html#conda
* https://requests.readthedocs.io/en/master/user/install/
* https://matplotlib.org/stable/#installation
* https://shapely.readthedocs.io/en/latest/
