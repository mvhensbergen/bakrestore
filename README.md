bakrestore.py
=============

```bakrestore.py``` is a small utility I made to ease the recovery of MSSQL database backup files (.bak created on a Windows machine) in a Linux MSSQL environment. In my line of work I have often encountered backup files that needed to be restored, but without access to the original server. As I am more fluent in Linux than Windows environments, I wished to restore these under Linux but I quickly ran into a few problems when restoring.

The problem when restoring these databases is that MSSQL tries to create its ```.mdf``` and ```.ldf``` files in their original locations, e.g. ```C:\Program Files\MSSQL\Data\...```, which obviously don't exist. While some googling will show you the solution, namely using the ```MOVE``` clause while restoring the backup, it can be a chore to create that restore command each time; hence this script.

This python script wraps the ```sqlcmd``` commandline tool, and does the appropriate sequence of commands to get the job done. Since it depends on the ```sqlcmd``` tool, major changes of it might break this script.

Please note that this script comes WITHOUT WARRANTY and just provides some very RUDIMENTARY functionality, so your mileage may vary. Having said that, feedback or pull requests are always welcomed! It was made and tested on Ubuntu 20.04.

Note that the script requires
1. installation of a working [MSSQl server](https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-ubuntu?view=sql-server-ver15)
2. installation of [mssql-tools](https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-setup-tools?view=sql-server-ver15)
3. authentication is basic SA password
4. restoring to a MSSQL server running on the same machine as the script.

As a tool to explore MSSQL databases on Linux with a GUI, I recommend [DBeaver](https://dbeaver.io).

Usage
=====

```
usage: bakrestore.py [-h] -file FILE -dbname DBNAME -password PASSWORD [--destination DESTINATION] [--with-sqlcmd WITH_SQLCMD]

optional arguments:
  -h, --help            show this help message and exit
  -file FILE            Full path Location of .bak file
  -dbname DBNAME        Name of the new database to make
  -password PASSWORD    Password of SA user
  --destination DESTINATION
                        Destination of database files
  --with-sqlcmd WITH_SQLCMD
                        Location of sqlcmd
```

The most basic way to get about restoring your database is as follows:

```
python3 bakrestore.py -file </path/to/backupfile.bak> -dbname <databasename> -password <mssqlpassword>
```

Your output should look like this:
```
Restoring now!
RESTORE DATABASE successfully processed 59946 pages in 5.187 seconds (90.287 MB/sec).
```

If you get the error that ```sqlcmd``` is not found but you did install the package, you might want to add ```sqlcmd``` to your path, or specify its location using the ```--with-sqlcmd=/opt/mssql-tools/bin/sqlcmd``` flag.

**Important:** When supplying the backup file, always specify the full path!
