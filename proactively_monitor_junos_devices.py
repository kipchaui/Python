# Imports all required modules
import concurrent.futures
import shutil
import difflib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from netmiko import ConnectHandler
import time
import datetime

# Starts time counter
t1 = time.perf_counter()


# Opens a file with a list of all device IPs
def fetch_ip_addresses():
    with open('hosts_file') as devices:
        addresses = devices.read().splitlines()
    return addresses


def monitor_devices(address):
    # The devices login credentials
    device_info = {
        'ip': address,
        'username': 'admin',
        'password': 'admin123',
        'device_type': 'juniper'
    }
    # Opens log file
    log_file = open('error_file.txt', 'a')

    try:
        # Creates a session to each device
        session = ConnectHandler(**device_info)
        # Runs the command on each device
        output = session.send_command('show chassis alarms')
        # opens a new file based on device hostname, this file will store previous alarms
        device_cfg_old = open(session.base_prompt.replace('admin@', '') + '_old.txt', "r+")
        # Opens a new file based on device hostname, this file will store current alarms and it writes current alarms on it
        with open(session.base_prompt.replace('admin@', '') + '_new.txt', 'w') as device_cfg_new:
            device_cfg_new.write(output.strip())
        with open(session.base_prompt.replace('admin@', '') + '_new.txt', 'r+') as device_cfg_new:
            templines = device_cfg_new.readlines()
            templines1 = []
            for string in templines:
                if (string != "\n"):
                    templines1.append(string)
        with open(session.base_prompt.replace('admin@', '') + '_new.txt', 'w') as device_cfg_new:
            for line in templines1:
                if not line.startswith(('#','{')):
                    device_cfg_new.write(line)

        # Compares previous alarms with respect to current alarms
        with open(session.base_prompt.replace('admin@', '') + '_old.txt', 'r') as old_file, open(
                session.base_prompt.replace('admin@', '') + '_new.txt', 'r') as new_file:
            fromlines = old_file.readlines()
            tolines = new_file.readlines()
            # Stores the previous and current alarms in table html format and highlights differences
            difference = difflib.HtmlDiff().make_file(fromlines, tolines, fromdesc='Previous', todesc='Current')
            # Opens a file to store the differences
            diff1 = session.base_prompt.replace('admin@', '') + '_diff.txt'
            # Checks whether there is any difference between current and previous alarms
            with open(diff1, 'w+') as outFile:
                outFile.seek(0)
                outFile.truncate()
                for line in tolines:
                    if line not in fromlines:
                        outFile.write(line)
                outFile.seek(0)
                first_char = outFile.read(1)
                # if there are no differences the program ends
                if not first_char:
                    print('There is no new alarm')
                # If there are differences, the programs triggers and email to support team
                else:
                    print('There is/are new alarm(s)')
                    fromaddr = 'admin@gmail.com'
                    toaddrlst = ['tech@gmail.com','support@gmail.com','admin@gmail.com']
                    toaddr = ', '.join(toaddrlst)

                    # More on MIME and multipart: https://en.wikipedia.org/wiki/MIME#Multipart_messages
                    msg = MIMEMultipart()
                    msg['From'] = fromaddr
                    msg['To'] = toaddr
                    msg['Subject'] = 'Proactive Monitoring - ' + session.base_prompt.replace('admin@', '')
                    msg.attach(MIMEText(difference, 'html'))

                    # Sending the email via Gmail's SMTP server on port 587
                    server = smtplib.SMTP('smtp.gmail.com', 587)

                    # SMTP connection is in TLS (Transport Layer Security) mode. All SMTP commands that follow will be encrypted.
                    server.starttls()

                    # Logging in to Gmail and sending the e-mail
                    server.login('admin@gmail.com', 'admin123')
                    server.sendmail(fromaddr, toaddrlst, msg.as_string())
                    server.quit()
        # Replaces the previous device alarms with new device alarm
        shutil.copyfile(session.base_prompt.replace('admin@', '') + '_new.txt',
                        session.base_prompt.replace('admin@', '') + '_old.txt')
    # Captures exceptions of a device and logs on a file
    except Exception as e:
        now = datetime.datetime.now()
        log_file.write('~~~~~~~~~~~~The device threw below error on ' + str(
            datetime.datetime.strftime(now, '%d-%m-%Y %H:%M:%S')) + '~~~~~~~~~~' + '\n')
        log_file.write(str(e))
    finally:
        pass


# Creates concurrent sessions to all routers same time
with concurrent.futures.ThreadPoolExecutor() as exe:
    ip_addresses = fetch_ip_addresses()
    results = exe.map(monitor_devices, ip_addresses)

# Calculates how long it took to execute the whole script
t2 = time.perf_counter()
print(f'The script finished executing in {round(t2 - t1, 2)} seconds.')
