import argparse
import subprocess
import ntpath
import os
import sys

# Argument parsing

parser = argparse.ArgumentParser()
parser.add_argument("-file", help="Full path Location of .bak file", required=True)
parser.add_argument("-dbname", help="Name of the new database to make", required=True)
parser.add_argument("-password", help="Password of SA user", required=True)
parser.add_argument("--destination", help="Destination of database files", default="/mssql/")
parser.add_argument("--with-sqlcmd", help="Location of sqlcmd", default="sqlcmd")
args = parser.parse_args()

bakfile = args.file
destpath = args.destination
dbname = args.dbname
password = args.password

# Stage 1 - get the filelist to determine contents of files

output = subprocess.run([args.with_sqlcmd, "-U", "sa", "-P", password,
                        "-Q", "RESTORE FILELISTONLY FROM DISK='%s'" % bakfile,
                        "-s", "|", "-h", "-1"],
                        capture_output=True)

if output.returncode != 0:
    print("An unexpected error occured:", output.stderr.decode())
    sys.exit(-1)

if 'terminating abnormally' in output.stdout.decode():
    print("An error occured during stage 1:\n", output.stdout.decode())
    sys.exit(-1)

# Stage 2 - create the TSQL statement to move the files to a new location during restore

moves = []
try:
    for row in output.stdout.decode().split('\n')[:-3]:
        [name, movepath] = (row.split("|")[0:2])
        name = name.strip()
        movepath = ntpath.basename(movepath.strip())
        moves.append(" MOVE '%s' TO '%s'" % (name, os.path.join(destpath, movepath)))
except Exception as e:
    print("An error occured during stage 2:\n", e)
    print("Output of stage 1 was:\n", output.stdout.decode())
    sys.exit(-1)

# Stage 3 - restore the database

print("Restoring now!")
output = subprocess.run([args.with_sqlcmd, "-U", "sa", "-P", password,
                        "-Q", "RESTORE DATABASE [%s] FROM DISK='%s' WITH FILE=1, REPLACE, %s" % (dbname, bakfile, ','.join(moves))],
                        capture_output=True)

if output.returncode != 0:
    print("An unexpected error occured:", output.stderr.decode())
    sys.exit(-1)

if 'terminating abnormally' in output.stdout.decode():
    print("An error occured during restore:\n", output.stdout.decode())
    sys.exit(-1)

print(output.stdout.decode().split('\n')[-2])
