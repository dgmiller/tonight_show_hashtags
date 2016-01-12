##this file contains some helpful functions for io and other file manipulations
#its main purpose is to help us be threadsafe

import fcntl
import os

##this will ensure that the given directories exist, 
#if they do not already exist it will create them
#\param folder, the folder to create if it does not exist, if passed a list it will assume it is a list of folders to create
def create_folders(folder) :

    if not isinstance(folder, (list, tuple)) :
        folder = [folder]

    for f in folder :
        if not os.path.exists(f) :
            os.makedirs(f)

## thread safe writing of lines to a file
# will not return until written
# will always overwrite whatever is already there
# \param each line goes on a separate line, new lines will be added to the ended before written
def write_file(filename, lines) :

    f = open (filename, 'w')
    fcntl.lockf(f, fcntl.LOCK_EX) #get the lock for the file

    f.writelines([l + '\n' for l in lines])
    f.flush()

    fcntl.lockf(f, fcntl.LOCK_UN)
    f.close()

## thread safe appending of lines to a file
# will not return until written
# \param each line goes on a separate line, new lines will be added to the ended before written
def append_file(filename, lines) :

    f = open (filename, 'a')
    fcntl.lockf(f, fcntl.LOCK_EX) #get the lock for the file

    f.writelines([l + '\n' for l in lines])
    f.flush()

    fcntl.lockf(f, fcntl.LOCK_UN)
    f.close()

## this is just like read_file, except it also passes back a callback function
# once called the callback function will overwrite the result to the end of the file
# and then close the lock. Be sure to call it! and only call it once
def read_write(filename) :
    f = open(filename, 'r+')
    fcntl.lockf(f, fcntl.LOCK_EX)

    lines = f.readlines()

    def callback(to_write) :
        f.seek(0)
        f.truncate()
        f.writelines([l + '\n' for l in to_write])
        fcntl.lockf(f, fcntl.LOCK_UN)
        f.close()

    return ([l.strip() for l in lines], callback)

## thread safe reading of a file
# \return a list of strings, each string one line, whitespace will be stripped from either side
def read_file(filename) :

    f = open(filename)
    fcntl.lockf(f, fcntl.LOCK_SH)

    lines = f.readlines()

    fcntl.lockf(f, fcntl.LOCK_UN)
    f.close()

    return [l.strip() for l in lines]

