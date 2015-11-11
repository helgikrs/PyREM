"""host.py: Contains the class that controls a remote host.

This host object should be a simple wrapper around ssh/scp with a easy, simple
interface. Commands should be able to be executed synchronously or
asynchronously.
"""

__author__ = "Ellis Michael"
__email__ = "emichael@cs.washington.edu"


import platform

from pyrem.task import SubprocessTask, RemoteTask


class Host(object):

    def __init__(self, hostname):
        self.hostname = hostname

    def run(self, command, **kwargs):
        """Run a command on the remote host.

        This is just a wrapper around RemoteTask(...)

        Args:
            command (list): The command to execute on the remote host.
            quiet (bool): Whether or not to print process output.
        Return:
            A ``RemoteTask``.
        """
        return RemoteTask(self.hostname, command, **kwargs)

    def send_file(self, file_name, remote_destination=None, **kwargs):
        if not remote_destination:
            remote_destination = file_name

        return SubprocessTask(
            ['rsync', '-ut', file_name,
             '%s:%s' % (self.hostname, remote_destination)],
            **kwargs)

    def get_file(self, file_name, local_destination=None, **kwargs):
        if not local_destination:
            local_destination = file_name

        return SubprocessTask(
            ['rsync', '-ut', '%s:%s' % (self.hostname, file_name),
             local_destination],
            **kwargs)


class LocalHost(Host):
    def __init__(self):
        super(LocalHost, self).__init__(platform.node())

    def run(self, command, **kwargs):
        return SubprocessTask(command, **kwargs)

    # TODO: Figure out if this is the best way to do things (probably not)
    #       Maybe there should be a separate RemoteHost with send_file and
    #       get_file
    def send_file(self, *args, **kwargs):
        raise NotImplementedError

    def get_file(self, *args, **kwargs):
        raise NotImplementedError

    def move_file(self, file_name, destination, **kwargs):
        return SubprocessTask(['mv', file_name, destination], **kwargs)
