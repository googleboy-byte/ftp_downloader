import ftplib
import socket
import os
import ftputil

host = input("Host: ")
hostname = socket.getfqdn(str(host))
user = input("FTP Username: ")
passwd = input("FTP Password: ")
is_path = os.path.isdir(hostname)
if is_path == True:
    pass
else:
    os.mkdir(hostname)
ftp_conn1_util = ftputil.FTPHost(host, 'user', 'bodmas')
ftp_conn = ftplib.FTP(host, 'user', 'bodmas')
ftp_conn.encoding = "utf-8"
home = "/"
pwd = ftp_conn.pwd()
print("Reading files...\n")
#files = ftp_conn.dir()

def download_dir_files(directory):
    
    #files = ftp_conn.nlst(directory)
    #ftp_conn1_util.cwd(directory)
    files = ftp_conn.nlst()
    print("Files in directory: '" + ftp_conn.pwd() + "'")
    for file in files:
        if ftp_conn1_util.path.isdir(file):
            print(file + " (dir)")
        else:
            print(file)
    print("\nDownloading files from the above directory\n")
    for file in files:
        if ftp_conn1_util.path.isdir(file):
            pass
        else:
            #print(file)
            if str(ftp_conn.pwd()).endswith("/"):
                filename = hostname + str(ftp_conn.pwd()) + str(file)
            else:
                filename = hostname + str(ftp_conn.pwd()) + "/" + str(file)
            check_subdir_local(str(ftp_conn.pwd()))
            try:
                with open(filename, 'wb') as f:
                    ftp_conn.retrbinary(f"RETR {file}", f.write)
                f.close()
            except:
                print(f"The file {file} could not be downloaded")
    print("\nAll files downloaded from above directory\n")
    
def check_subdir_local(dir_to_check):
    if dir_to_check.startswith("/"):
        dir_2_check = hostname + dir_to_check
    else:
        dir_2_check = hostname  + "/" + dir_to_check
    is_path = os.path.isdir(dir_2_check)
    if is_path == True:
        pass
    else:
        os.mkdir(dir_2_check)
    return

def chk_4_subdirs(directory):
    subdir = []
    dircount = 0
    files = ftp_conn1_util.listdir(ftp_conn1_util.curdir)
    print("Files in directory: '" + directory + "'")
    for file in files:
        if ftp_conn1_util.path.isdir(file):
            subdir.append(str(file))
        else:
            pass
    for d in subdir:
        dircount = dircount + 1
    return dircount, subdir

def main(dir_2_dwnld):
    dircount, sdir_dic = chk_4_subdirs(dir_2_dwnld)
    if dircount > 0:
        download_dir_files(dir_2_dwnld)
        dircount = dircount - 1
        for d in sdir_dic:
            ftp_conn.cwd(d)
            download_dir_files(ftp_conn.pwd())
            ftp_conn.cwd('../')
    else:
        download_dir_files(dir_2_dwnld)
    
    
if __name__ == "__main__":
    main(pwd)
    