#! /bin/python3

import os
import shutil
import sys

def is_ansible_installed():
    output = shutil.which("ansible")
    if output is None:
        rep = input("Ansible is not installed, do you want to install it? (y/n): ")

        if rep == "y":
            os.system("sudo apt install -y ansible python3-pip")
        else:
            sys.exit()


def configure_python_modules():
    os.system("pip3 install pyvmomi")
    os.system("pip3 install --upgrade pip setuptools")
    os.system("pip3 install --upgrade git+https://github.com/vmware/vsphere-automation-sdk-python.git")


def configure_vmware_module():
    enabled = False
    with open("/etc/ansible/ansible.cfg") as in_file:
        content = in_file.readlines()

    with open("/etc/ansible/ansible.cfg", "w") as out_file:
        for line in content:
            if line == "enable_plugins = vmware_vm_inventory\n":
                print("Module is already enabled in the ansible configuration")
                enabled = True

        for line in content:
            if enabled != True:
                if line == "[inventory]\n":
                    line = line + "enable_plugins = vmware_vm_inventory\n"
            out_file.write(line)

def configure_credentials():
    if os.path.exists("Terraform/provider.tf") is False:
        shutil.copyfile("provider.tf", "Terraform/provider.tf")
    if os.path.exists("Terraform/inv.vmware.yml") is False:
        shutil.copyfile("inv.vmware.yml", "Terraform/inv.vmware.yml")

    print("Please enter your credentials")
    host = input("hostname : ")
    user = input("username : ")
    password = input("password : ")
    az_blob_key = input("Azure Blob Key : ")

    with open("Terraform/provider.tf") as in_tf:
        content = in_tf.readlines()

    with open("Terraform/provider.tf", "w") as out_tf:
        for line in content:
            if '  user           = "' in line:
                line = '  user           = "' + user + '"\n'
            if '  password       = "' in line:
                line = '  password       = "' + password + '"\n'
            if '  vsphere_server = "' in line:
                line = '  vsphere_server = "' + host + '"\n'
            if '    access_key = "' in line:
                line = '    access_key = "' + az_blob_key + '"\n'
            out_tf.write(line)


    with open("Terraform/inv.vmware.yml") as in_an:
        content = in_an.readlines()

    with open("Terraform/inv.vmware.yml", "w") as out_an:
        for line in content:
            if 'hostname:' in line:
                line = 'hostname: ' + host + '\n'
            if 'username:' in line:
                line = 'username: ' + user + '\n'
            if 'password:' in line:
                line = 'password: ' + password + '\n'
            out_an.write(line)


def azure_cli_installation():
    output = shutil.which("az")
    if output is None:
        rep = input("Azure CLI is not installed, do you want to install it? (y/n): ")

        if rep == "y":
            os.system("curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash")
        else:
            sys.exit()



###TODO:
###     1 - SSH keys
###     2 - pyhon plugins for vmware
###
if __name__ == "__main__":
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
    is_ansible_installed()

    azure_cli_installation()

    configure_vmware_module()

    configure_python_modules()

    configure_credentials()


