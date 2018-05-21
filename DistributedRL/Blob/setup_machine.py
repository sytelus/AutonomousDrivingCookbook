import os
import traceback
import subprocess
import sys
import shutil

def do_command(cmd):
    print('Executing {0}'.format(cmd))
    try:
        os.system(cmd)
        print('Success!')
        sys.stdout.flush()
    except Exception as e:
        print('Failed. Reason: {0}'.format(traceback.format_exc()))
        sys.stdout.flush()

with open('C:/prereq/log.txt', 'w') as f:
    sys.stdout = f
    
    do_command('conda install -y pip')

    # Install required python packages
    do_command('pip install wheel --upgrade')
    do_command('pip install numpy==1.14.0')
    do_command('pip install pandas==0.22.0')
    do_command('pip install tensorflow-gpu==1.4.0') #1.5.0 requires CUDA 9, which is not installed on the image we have.
    do_command('pip install keras==2.1.3')
    do_command('pip install msgpack==0.5.1')
    do_command('pip install msgpack-rpc-python==0.4')
    do_command('pip install h5py==2.7.1')
    do_command('pip install django==2.0.1')
    do_command('pip install django-ipware==2.0.1')
    do_command('pip install requests==2.18.4')
    
    # Mount the file share
    do_command('call C:\\prereq\\mount.bat')
    do_command('dir z: >> C:\\prereq\\list.txt')
    
    # Configure AirSim to use the car
    do_command('mkdir D:\\Users\\airsim_batchuser\\Documents\\AirSim')
    do_command('echo {"SettingsVersion": 1.0, "SimMode": "Car"} > D:\\Users\\airsim_batchuser\\Documents\\AirSim\\settings.json')
    do_command('call C:\\prereq\\mount.bat')
    
    # Download AirSim if it's not already on disk.
    if not os.path.isdir('D:\\AD_Cookbook_AirSim'):
        do_command('"C:\\Program Files (x86)\\Microsoft SDKs\\Azure\\AzCopy\\AzCopy.exe" /Source:https://airsimtutorialdataset.blob.core.windows.net/e2edl/AD_Cookbook_AirSim.7z /Dest:D:\\\\tmp.7z')
        do_command('Z:\\tools\\7za.exe x D:\\tmp.7z -oD:\\ -y -r')
    
    # Set up visualization scheduled task.
    # This task will kill any running instances of AirSim and restart it when the user logs in
    
    # Task might not exist
    try:
        do_command('schtasks.exe /delete /tn StartAirsimIfAgent /f')
    except:
        pass
    
    do_command('schtasks.exe /create /xml Z:\\scripts_downpour\\run_airsim_on_user_login.xml /RU airsim_batchuser /RP AirSimBatchUser01! /tn StartAirsimIfAgent /IT')