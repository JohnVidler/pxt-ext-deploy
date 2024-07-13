#!/usr/bin/env python3

# MIT License
# 
# Copyright (c) 2024 Dr John Vidler
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import os
import argparse
import subprocess
from pprint import pprint

if __name__ == "__main__":

    git_state = subprocess.run( ['git', 'status', '--porcelain'], stdout=subprocess.PIPE ).stdout.decode('utf-8')
    if len(git_state) > 0:
        print( "Git state appears to have changes pending. Please commit all changes first then run deploy.py again" )
        exit( -1 )
    
    git_branch = subprocess.run( ['git', 'branch', '--show-current'], stdout=subprocess.PIPE ).stdout.decode('utf-8')
    if git_branch not in [ 'main', 'master' ]:
        print( "WARNING: You're not on a main/master branch, so your tags may not work as you expect!" )

    pxt = None
    with open( 'pxt.json' ) as pxt_js:
        pxt = json.load(pxt_js)

    if pxt == None:
        print( "Cannot find or read pxt.json, cannot continue!" )
        exit( -3 )

    if not os.path.isdir( ".git" ):
        print( "This is not a git repository, cannot continue!" )
        exit( -4 )

    parser = argparse.ArgumentParser()
    parser.add_argument( '--major', default=False, action="store_true", help="Increment the MAJOR version number; version becomes X.0.0" )
    parser.add_argument( '--minor', default=False, action="store_true", help="Increment the MINOR version number; version becomes X.Y.0" )
    parser.add_argument( '--patch', default=False, action="store_true", help="Increment the PATCH version number only (this is the default)" )
    parser.add_argument( '-m', '--message', default="Incremented the package version", action="store", help="Sets a custom commit message for this deployment" )
    args = parser.parse_args()

    version = pxt['version'].split(".")

    if args.major and not args.minor and not args.patch:
        version[0] = str(int(version[0]) + 1)
        version[1] = "0"
        version[2] = "0"
    
    if args.minor and not args.major and not args.patch:
        version[1] = str(int(version[1]) + 1)
        version[2] = "0"
    
    if not args.minor and not args.major:
        version[2] = str(int(version[2]) + 1)

    pxt['version'] = '.'.join(version)

    print( f"Now at version: {pxt['version']}" )

    with open( 'pxt.json', 'w' ) as pxt_js:
        json.dump( pxt, pxt_js, indent=2 )
    
    subprocess.run( ["git", "add", "pxt.json"] )
    subprocess.run( ["git", "commit", "-m", f"'{args.message}'"] )
    subprocess.run( ["git", "tag", f"v{version[0]}.{version[1]}.{version[2]}"] )

    print( "Tagged locally, remember to run 'git push && git push --tags' to send the tags upstream" )

