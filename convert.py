#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Etienne Glossi - etienne.glossi@gmail.com
# 16/12/2012
# Festival des Arcs

from optparse import OptionParser
from subprocess import Popen
import os, sys, random, time, shlex

# Configuration
FFMPEG_BIN = "/opt/ffmpeg/bin/ffmpeg"
# securise saisie des parametres
PARAMETERS = "-v quiet -i '%s' -vcodec prores -profile:v 0 -s hd1080 -acodec pcm_s16be -ar 48K -ac 2 -async 1 -copyts -y -threads 4 '%s'"
EXTENSIONS = ("MTS", "MOV")
FORK = 4

def get_param():
    parser = OptionParser()
    parser.add_option("-d", "--dest", dest="output_directory",
                      help="output files to DIRECTORY [%s]" % os.getcwd(), metavar="DIRECTORY", default=os.getcwd())
    return parser.parse_args()
    
def convert(path, output):
    cl = [FFMPEG_BIN + " " + PARAMETERS % (os.path.join(path, f), output + "/" + f[:-4] + ".MOV") for f in os.listdir(path) if f[-3:] in EXTENSIONS]
    print "Conversion de %d fichiers vidéo...\n" % len(cl)
    running_fork = {}
    try:
        for exe in cl:
            args = shlex.split(exe)
            child = Popen(args)
            print "+ (pid: %d) Start conversion: %s" % (child.pid, exe)
            running_fork[child] = args[-1]
            for c in running_fork:
                if c.returncode != None:
                    print "- (pid: %d) Successfully converted to %s" % (c.pid, running_fork[c])
                    del running_fork[c]
            if len(running_fork) >= FORK:
                c, f = running_fork.popitem()
                c.wait()
                print "- (pid: %d) Successfully converted to %s" % (c.pid, f)
        while len(running_fork) != 0:
            c, f = running_fork.popitem()
            c.wait()
            print "- (pid: %d) Successfully converted to %s" % (c.pid, f)
    except KeyboardInterrupt:
        for c in running_fork:
            c.kill()
        print "\nTerminated by user !"
        exit(2)
    
    
if "__main__" == __name__:
    (options, args) = get_param()
    if len(args) != 1:
        print "[Erreur] Pas de répertoire source spécifié."
        exit(1)
    source_dir = os.path.abspath(args[0])
    if not os.path.exists(source_dir):
        print "[Erreur] Répertoire spécifié introuvable."
    output_directory = os.path.abspath(options.output_directory)
    print "Répertoire destination: %s" % output_directory
    start = time.time()
    convert(source_dir, output_directory)
    exec_time = time.time() - start
    print "\nEnd. Temps d'execution: %d minutes %.2f !" % (exec_time/60, exec_time%60)
    
    