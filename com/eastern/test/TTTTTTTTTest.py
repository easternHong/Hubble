#!/usr/bin/python
# -*- coding: utf-8 -*-
import distutils
import glob
import os
import sys
import zipfile

from com.eastern.common import TreeSet

sys.path.append("/Users/eastern/PycharmProjects/SimpleTest/")

PROJECT_NAME = "SimpleTest"
APK_FILE = "/Users/eastern/Downloads/yymobile_client-7.10.3-881.apk"
DEBUG = False


def unzip_apk(path_to_zip_file, directory_to_extract_to):
    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()


def get_working_dir():
    current = os.getcwd()
    index = current.index(PROJECT_NAME)
    working_dir = current[:index + len(PROJECT_NAME)] + "/tmp"
    return working_dir


def check_dexdump():
    ret = distutils.spawn.find_executable("dexdump")
    return ret is not None and len(ret) > 0


def collect_all_classes_in_apk(file_apk, unzip_file):
    built_in_so_list = glob.glob(unzip_file + "/lib/armeabi-v7a/libcom_*")
    cmd = "dexdump '%s'|grep 'Class descriptor'" % file_apk
    print "collect class in %s" % file_apk
    clazz = os.popen(cmd).read()

    for apk in built_in_so_list:
        cmd = "dexdump '%s'|grep 'Class descriptor'" % apk
        print "collect class %s" % apk
        clazz += (os.popen(cmd).read())
    name_set = clazz.split("\n")
    # make a tree set
    tree = TreeSet(name_set)
    if DEBUG:
        for p in tree:
            print p

    print "类名总数:%s,%s" % (len(clazz), len(tree))
    return tree


def find_package(_clazz_tree):
    print "go"
    # package_tree = TreeSet(None)

    for p in _clazz_tree:
        print str(p)


if __name__ == "__main__":

    if not check_dexdump():
        print "找不到dexdump"
    else:
        apk_file = APK_FILE
        work_dir = get_working_dir()
        unzip_apk(apk_file, work_dir)
        clazz_tree = collect_all_classes_in_apk(apk_file, work_dir)
        find_package(clazz_tree)
