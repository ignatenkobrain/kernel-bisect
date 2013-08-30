#!/usr/bin/python

# Copyright 2013 Igor Gnatenko
# Author(s): Igor Gnatenko <i.gnatenko.brain AT gmail DOT com>
#            Bjorn Esser <bjoern.esser AT gmail DOT com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; version 2 of the License.
# See http://www.gnu.org/copyleft/gpl.html for the full text of the license.

import os
import sys
import argparse
import git
import sh

WORK_DIR = os.path.dirname(sys.argv[0])

repo = git.Repo(WORK_DIR)
assert repo.bare == False
repo.config_reader()  
head = repo.head
headcommit = head.commit

def out(line):
  sys.stdout.write(line)

def err(line):
  sys.stderr.write(line)

class Parser(argparse.ArgumentParser):
  def error(self, message):
    sys.stderr.write('error: %s\n' % message)
    self.print_help()
    sys.exit(2)

def set_args(parser):
  parser.add_argument('--start', action='store_true', help='start bisecting')
  parser.add_argument('--reset', action='store_true', help='reset bisecting')
  parser.add_argument('--good', action='store', metavar='SHA', help='good kernel')
  parser.add_argument('--bad', action='store', metavar='SHA', help='bad kernel')
  parser.add_argument('--skip', action='store', metavar='SHA', help='skip kernel')
  parser.add_argument('--log', action='store_true', help='show bisect log')

def archive():
  repo.archive(open("archive.tar.gz",'w'))

def print_commit():
  print "HEAD commit: " + headcommit.hexsha

def bisect(args):
  state = None
  commit = ''
  if args.start:
    state = 'start'
  elif args.reset:
    state = 'reset'
  elif args.skip:
    state = 'skip'
    commit = args.skip
  elif args.good:
    state = 'good'
    commit = args.good
  elif args.bad:
    state = 'bad'
    commit = args.bad
  elif args.log:
    state = 'log'
  else:
    err('Nothing to do. Use -h for help.' + '\n')
    sys.exit(1)

  try:
    sh.git.bisect(state, commit, _out=out, _err=err)
  except:
    pass

def main():
  parser = Parser(description='Bisect Linux kernel')
  set_args(parser)
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
  args = parser.parse_args()
  bisect(args)
  if head.commit != headcommit:
    print "commit was changed !"

if __name__ == "__main__":
  main()
