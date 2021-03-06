'''
Eastwind Package Management Interface YUM Implementation
'''

import subprocess

class EastwindPkgMangerYUM:
    def update(self):
        handle = subprocess.Popen('sudo yum update',
                                  shell=True)
        stdout, stderr = handle.communicate('n\n')

    def upgrade(self):
        handle = subprocess.Popen('sudo yum upgrade',
                                  shell=True).wait()

    def install(self, pkgs):
        handle = subprocess.Popen('sudo yum install %s'
                                  % (" ".join(pkgs)),
                                  stdin=subprocess.PIPE,
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')

    def install_interactive(self, pkgs):
        handle = subprocess.Popen('sudo yum install %s' % (" ".join(pkgs)),
                                  shell=True).wait()

    def purge(self, pkgs):
        handle = subprocess.Popen('sudo yum remove %s'
                                  % (" ".join(pkgs)),
                                  stdin=subprocess.PIPE,
                                  shell=True)
        stdout, stderr = handle.communicate('y\n')

# TODO: /etc/yum.repos.d
#    def add_external_sources(self, sources):
#        for source in sources:
#            print 'Adding %s to system...' % source
#            handle = subprocess.Popen('sudo add-apt-repository %s' % source,
#                                      shell=True).wait()

