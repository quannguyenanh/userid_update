from sys import argv
from urllib2 import Request, urlopen, URLError, HTTPError
import paramiko
import os

# args[1]: email
# args[2]: userID
# args[3]: password

# extract params
def extract_input():
    if len(argv) != 4:
        print "Enter 3 params as: email, userID, password"    
    email = argv[1]
    userID = argv[2]
    password = argv[3]
    
    #extract domain name from userID
    domain = userID.split('@')
    domain = domain[-1]
    return email, userID, password, domain

# open file to modify
def modify_file(file_name, userID, email, password):
    #test
    userID = 'dad'
    email = 'test@a.com'
    password = '1234'
    found = False
    line_update = userID + ':' + email + ':' + password + '\n'
    for line in fileinput.input(file_name, inplace=1):
        if userID in line:
            line = line_update
            found = True
        sys.stdout.write(line)
    if found == False:
        file = open(file_name, 'a')
        file.write(line_update)
        file.close()     

# download file from domain that extracted from userID
def connect_host(domain, info_file, email, userID, password): # info_file stores full path of info file on client
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys(os.environ['HOME'] + '/.ssh/known_hosts')
    ssh.connect(domain)
    
    # temporary file to store from info file
    tmp_filename = '/tmp/tmp_file.info'
    try:
        ftp = ssh.open_sftp()
        # read file to temporary file on local
        filehandler = ftp.file(info_file, 'r')
        tmp_file = open(tmp_filename, 'w')
        for line in filehandler:
            tmp_file.write(line)
        filehandler.close()
        tmp_file.close()
        
        # search and modify in temporary file
        modify_file(tmp_filename, email, userID, password)
        
        # To write
        filehandler = ftp.file(info_file, 'w')
        tmp_file = open(tmp_filename, 'r')
        for line in tmp_file:
            filehandler.write(line)
        filehandler.close()
        tmp_file.close()
    finally:
        ssh.close()


if __name__ == '__main__':
    email, userID, password, domain = extract_input()
    
    # test
    #open_file('test.txt', 'w', 'http://localhost/')
    #print "%s %s %s" % (email, userID, password)
    
    connect_host(domain, info_file, email, userID, password)
