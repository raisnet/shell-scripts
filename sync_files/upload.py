from call_bash_func import run_cmd
import os
import sys

def upload_files(command, list_sync_dirs, uuid_recv_disk, logs_dir, test_mode):
    for i in list_sync_dirs:
        command[len(command) - 2] = i

        name_sync_dir = os.path.basename(os.path.dirname(i))    # get name sync folder from full path
                                                                # arg: /d/projects/bash-scripts/sync_files/
                                                                # result: sync_files
        if (test_mode):
            command[len(command) - 3] = '--log-file=' + logs_dir + '/' + uuid_recv_disk + '__TEST_MODE__' + name_sync_dir + '.txt'
        else:
            command[len(command) - 3] = '--log-file=' + logs_dir + '/' + uuid_recv_disk + '__' + name_sync_dir + '.txt'

        code = run_cmd(command)

        if (code.returncode != 0):
           sys.exit('Error\nCheck logs')