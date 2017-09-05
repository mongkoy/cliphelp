#!/usr/bin/python

from Tkinter import Tk
import pdb
import md5
import argparse
import sys
import pygtk
pygtk.require('2.0')
import gtk
import gobject
import glib
import hashlib
import threading
import time


clipboardfile =""

def callBack(*args):
    value =  clip.wait_for_text()
    global clipboardfile
    with open(clipboardfile,'w+') as afile:
        afile.write(value)


parser = argparse.ArgumentParser(description='process arguments for configuration')
parser.add_argument('-f', action="store",dest="filepath",help='filepath of the clipboard file')



class ClipBoardRunner(threading.Thread):

    def __init__(self, group=None, target=None, name=None,fileconfigpath="", kwargs=None, verbose=None):

        threading.Thread.__init__(self, group=group, target=target,name=name,verbose=verbose)
        self.filepath = fileconfigpath
        self.count = 0
        self.filehash = self.initializeHash()
        self.initialclipboard = ""
        self.tk = ""
        return

    def initializeHash(self):
        return self.getHash()

    def appendToClipboardfile(self,data):
        with open(self.filepath,'w+') as afile:
            afile.write(data)


    def run(self, *args):
        self.count +=1
        while(True):
            with open(self.filepath,'rb') as afile:
                buffer = afile.read()
                if self.isFileChanged():
                    self.filehash = self.getHash()
                    #print "clipboard file changed  "
                    appendtoClipboard(buffer)
            if is_clipboardchanged(self.initialclipboard):
                buffer = getClipboardData()
                if buffer == None:
                    buffer=""
                self.initialclipboard = buffer
                self.appendToClipboardfile(buffer)
            time.sleep(1)

    def isFileChanged(self):
        newHash =  self.getHash()
        if newHash != self.filehash:
            print newHash + " vs." + self.filehash
            return True
        return False

    def getHash(self):
        hash1 = hashlib.md5()
        with open(self.filepath,'rb') as afile:
            buffer = afile.read(8192)
            hash1.update(buffer)
            filehash = hash1.hexdigest()
        return filehash

def appendtoClipboard(data):
    clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
    clipboard.set_text(data)
    clipboard.store()


def getClipboardData():
    clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
    bufdata = clipboard.wait_for_text()
    return bufdata

def is_clipboardchanged(strtemp):
    clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)

    try:
        if strtemp != clipboard.wait_for_text():
           return True
    except:
        pass
    return False

if __name__ == "__main__":
    args = parser.parse_args()
    global clipboardfile
    clipboardfile = args.filepath
    myclipboard = ClipBoardRunner(fileconfigpath=clipboardfile)
    myclipboard.setDaemon(True)
    #thread = threading.Thread(myclipboard)

    myclipboard.initialclipboard=""
    myclipboard.start()
    myclipboard.join()


