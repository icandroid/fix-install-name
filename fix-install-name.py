#!/usr/bin/python
# -*- coding: utf8 -*-

'''
    fix-install-name:
    =====================================================================================
    a tool to fix install name of binaries in Mac OS.

    for knowledge of `install name`, please refer to
    https://www.mikeash.com/pyblog/friday-qa-2009-11-06-linking-and-install-names.html
    it gives concise understanding of `install name`.

    when we install some libraries via 'automake', or 'cmake', sometimes the installed dynamic libraries are
    not installed with effective install names.
    in here, ONLY ABSOLUTE PATH is supported in changing/updating the install names.
    if you feel necessary, you may extend the script to support '@rpath', '@loader_path', '@executable_path'.

    please keep in mind that it is your own risk to run the script.
    to run the script, type like:
        python fix-install-name.py lib_list_yours.dylib
'''

import  os.path, subprocess, sys, commands

def     get_dependencies(file_path):
    process     = subprocess.Popen(['otool', '-L', file_path], stdout= subprocess.PIPE)
    out, err    = process.communicate()
    lines   = out.splitlines()
    dylib_list = []
    for line in lines[1:]:
        dylib = line.lstrip().split(' ')[0]
        if dylib[:3] == 'lib':  # in general, dynamic libraries should begin with 'lib'.
            dylib_list.append(dylib)
    return dylib_list

def     check_if_relative(dylib_path):
    process     = subprocess.Popen(['otool', '-D', dylib_path], stdout=subprocess.PIPE)
    out,err     = process.communicate()
    lines       = out.splitlines()
    output  = lines[1].lstrip()
    return output[:3] == 'lib'

def     set_install_name(dylib_path, install_name):
    status, output = commands.getstatusoutput('install_name_tool -id ' + install_name + ' ' + dylib_path)
    return status == 0

def     change_install_name(bin_path, dylib_name, install_name):
    status, output = commands.getstatusoutput('install_name_tool -change ' + dylib_name + ' ' + install_name + ' ' + bin_path)
    return status == 0

def     check_fix_req(file_path):
    if os.path.islink(file_path):
        real_path = os.path.realpath(file_path)
    else:
        real_path = file_path
    real_path   = os.path.abspath( real_path)
    dir_prefix  = os.path.dirname( real_path)
    dylib_list  = get_dependencies( real_path)
    if real_path.endswith('.dylib') and check_if_relative(real_path):
        print "try to set install name for %s" % (file_path)
        if not set_install_name(real_path, real_path):
            print "ERROR: fail to set install name"
            return
    if len(dylib_list) > 0:
        for dylib in dylib_list:
            dylib_install = dir_prefix + '/' + dylib
            print "try to change dependent library %s to %s" % (dylib, dylib_install)
            if not os.path.exists(dylib_install):
                print "ERROR: fail to locate the dependent library %s" %(dylib)
                return
            if not change_install_name(real_path, dylib, dylib_install):
                print "ERROR: fail to change dependent library %s" % (dylib)
                return
        print "done"
    else:
        print "dependency ok"



if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "usage: %s [file_list]" %(sys.argv[0])
        sys.exit(0)
    for arg in sys.argv:
        check_fix_req(arg)
