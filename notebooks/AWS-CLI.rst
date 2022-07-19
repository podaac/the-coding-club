# Accessing JPL AWS resources via the command line (AWS CLI)

**AWS User Guide: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html**

**AWS CLI Command Reference: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/index.html**

## Pre-requisites
### Assumptions
1. You already have an EC2 instance setup and have the instance ID. To find the instance ID:
    1. Log into JPL AWS: https://goto.jpl.nasa.gov/awsconsole
    2. In the search bar enter “EC2” and select “EC2” from the drop-down list.
    3. The instance ID is located in the “Instance ID” column. You can also click on it to see further details about your instance.
2. You can ssh to your EC2 instance.
3. Jupyter is installed and functioning on the EC2 instance. See this tutorial for more info: https://github.jpl.nasa.gov/gist/jmcnelis/727876436679f37442988fd4b308ac43
4. You are using a Mac to generate keys and run AWS CLI commands. 

### JPL Access Key Generation
Access Key ID and Secret Access Key obtained from JPL script: https://github.jpl.nasa.gov/cloud/Access-Key-Generation

Generate an Access Key and Secret Access Key:
1. Download the latest release for your operating system (https://github.jpl.nasa.gov/cloud/Access-Key-Generation/releases).
2. Navigate to where you downloaded or placed the Access-Key-Generation program.
3. Move the file to a location that is in your path: `mv aws-login.darwin.amd64 /usr/local/bin`
4. Make the file executable: `chmod +x /usr/local/bin/aws-login.darwin.amd64`
5. Symlink the executable so that it is available for the public and gov clouds:
    ```
    ln -s /usr/local/bin/aws-login.darwin.amd64 /usr/local/bin/aws-login-gov.darwin.amd64
    ln -s /usr/local/bin/aws-login.darwin.amd64 /usr/local/bin/aws-login-pub.darwin.amd64
    ```
6. Clear the quarantine extended attribute from the downloaded file: `xattr -r -d com.apple.quarantine /usr/local/bin/aws-login.darwin.amd64`

### Set up the AWS CLI tool
Install the latest version of the AWS CLI for your operating system: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

Install the tool:
1. Download the installer: `curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"`
3. Run the installer: `sudo installer -pkg AWSCLIV2.pkg -target /`
4. Verify that your shell can located the 'aws' executable:
    ```
    which aws
    aws --version
    ```
# Using the AWS CLI tool
1. Log into JPL AWS Public Cloud: `aws-login.darwin.amd64 --pub`
    1. Follow the on-screen instructions to enter your username/password, your RSA SecureID (PIN + token), and the role you would like to assume.
    2. This will create a credential file in `/Users/username/.aws/config`. You need to specify the '--profile' argument when using the AWS CLI tool to access the correct Access Key ID and Secret Access Key.

2. Describe your EC2 instance: `aws --profile saml-pub ec2 describe-instances --instance-ids i-000000000000`
    1. For this and future commands, make sure to replace `i-000000000000` with the instance id of your EC2 instance.

3. Start your EC2 instance: `aws --profile saml-pub ec2 start-instances --instance-ids i-000000000000`

4. Create an SSH tunnel to your notebook: `ssh -i {~/.ssh/key}.pem jpluser@{private_ip} -L 9889:localhost:9889`
    1. Replace `~/.ssh/key` with the path to your AWS SSH key and `{private_ip}` with the private IP of your instance.

5. In your SSH session on the EC2 instance, start a new "screen": `screen -S ipylab`
    1. More info on screen: https://linuxize.com/post/how-to-use-linux-screen/

6. Activate your Jupyter conda environment: `conda activate jupyter`

7. Generate a password to use with the Jupyter notebook server: `PW="$(python3 -c 'from notebook.auth import passwd; import getpass; print(passwd(getpass.getpass(), algorithm="sha256"))')"`
    1. [Enter a password and remember it for later]

8. Start your Jupyter notebook server:
    ```
    jupyter lab \
        --port=9889 \
        --ip='127.0.0.1' \
        --NotebookApp.token='' \
        --NotebookApp.password="$PW" \
        --notebook-dir="$HOME" \
        --no-browser \
        &
    ```

9. Detach the screen by pressing CTRL + A -> D (this will keep the Jupyter lab process running even if your ssh session times out).

10. Access the Jupyter notebook via a web browser on your local machine: http://127.0.0.1:9889/lab

11. Enter the password from step 7.1 at the prompt.

12. When you are done, stop the Jupyter notebook in the web browser: File -> Shutdown 

13. In the EC2 SSH session go back to the screen session you created earlier: `screen -r`

14. Stop the Jupyter notebook server: `ctrl-c`

15. Exit out of the screen session and SSH session.

16. Stop the EC2 instance: `aws --profile saml-pub ec2 stop-instances --instance-ids i-000000000000`

# Thoughts on scripted solutions
- Set up a cronjob to shut your EC2 instance at a specific time each night.
- Script you can execute via ssh to launch a Jupyter notebook.
- Launch Jupyter notebook on boot of the EC2 instance.
- Script to launch EC2 instance, poll instance until running, then launch Jupyter notebook via ssh (bash script on EC2 instance), and print out URL with token.
- Script to shutdown the Juptyer notebook via ssh (bash script on EC2 instance) and shutdown EC2 instance.

