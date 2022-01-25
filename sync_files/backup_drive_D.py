import sys
import argparse
from src import mnt, log, upl

def handler_cmd_arg(args, list_func):
    """
    Exec. script with different arguments.
    If [args] = a, start synchronization all folders, that located on source-partition.
    Otherwise, script starts synchronization all folders, w/o folder which contains VDI files
    :param args: argument execution script
    :param list_func: array of functions, which contains different arguments of execution Rsync
    """
    if args['a']:
        for item in list_func:
            item
    elif args['novdi']:
        for item in range(len(list_func)/2):
            list_func[item]


def prepare_sync_data():
    """
    Prepares all data for start synchronization:
    arrays with arguments execution for Rsync,
    checking if mounted partition-receiver,
    creating log file
    :return: list functions with different arguments for execution Rsync
    """
    uuid_src_drive = '01D7DEEE65713660'
    root_pth_src_drive = mnt.get_src_drive(uuid_src_drive)  # /cygdrive/d

    root_pth_dest_drive, name_model_recv_drive = mnt.get_recv_drive()  # /cygdrive/f, Hitachi
    full_path_dest_dir = root_pth_dest_drive + '/dell_inspiron_3576'

    path_logs_dir = log.get_logs_dir('drive_D')

    rsync_test_mode_wo_vdi = [
        'rsync',
        '--recursive',  # copy directories recursively
        '--links',  # copy symlinks as symlinks
        '--perms',  # preserve permissions
        '--times',  # preserve modification time
        '--group',  # preserve group
        '--owner',  # preserve owner (super-user only)
        '--devices',  # preserve device files (super-user only)
        '--specials',  # preserve special files
        '--human-readable',  # output numbers in a human-readable format
        '--dry-run',  # perform a trial run with no changes made
        '--stats',  # give some file-transfer stats
        '--progress',  # show progress during transfer
        '--del',  # receiver deletes during xfer, not before
        '--verbose',  # increase verbosity
        '--out-format="%t %f %''b"',
        '--exclude=games/',
        '--exclude=Snapshots/',
        '--exclude=Logs/',
        '''--exclude=*.vdi''',
        '',
        '',
        full_path_dest_dir
    ]

    rsync_wo_vdi = [
        'rsync',
        '--recursive',
        '--links',
        '--perms',
        '--times',
        '--group',
        '--owner',
        '--devices',
        '--specials',
        '--human-readable',
        '--stats',
        '--progress',
        '--del',
        '--verbose',
        '--out-format="%t %f %''b"',
        '--exclude=games/',
        '--exclude=Snapshots/',
        '--exclude=Logs/',
        '''--exclude=*.vdi''',
        '',
        '',
        full_path_dest_dir
    ]

    rsync_test_mode_crt_vdi = [
        'rsync',
        '--recursive', '--links', '--perms', '--times', '--group', '--owner', '--devices', '--specials',
        # archive mode; equals -rlptgoD or -a (--archive) (no -H,-A,-X)
        '--dry-run',
        '--out-format="%t %f %''b"',
        '--progress',
        '--stats',
        '--human-readable',
        '--del',
        '--sparse',      # handle sparse files
        '--copy-links',  # transform symlink into referent file/dir
        '',
        '',
        ''
    ]

    rsync_test_mode_upd_vdi = [
        'rsync',
        '--recursive', '--links', '--perms', '--times', '--group', '--owner', '--devices', '--specials',
        # archive mode; equals -rlptgoD or -a (--archive) (no -H,-A,-X)
        '--dry-run',
        '--out-format="%t %f %''b"',
        '--progress',
        '--stats',
        '--human-readable',
        '--del',
        '--no-whole-file',  # copy files whole (w/o delta-xfer algorithm)
        '--inplace',        # rsync writes the updated data directly to the destination file.
        '--copy-links',
        '',
        '',
        ''
    ]

    rsync_crt_vdi = [
        'rsync',
        '--recursive', '--links', '--perms', '--times', '--group', '--owner', '--devices', '--specials',
        '--out-format="%t %f %''b"',
        '--progress',
        '--stats',
        '--human-readable',
        '--del',
        '--sparse',
        '--copy-links',
        '',
        '',
        ''
    ]

    rsync_upd_vdi = [
        'rsync',
        '--recursive', '--links', '--perms', '--times', '--group', '--owner', '--devices', '--specials',
        '--out-format="%t %f %''b"',
        '--progress',
        '--stats',
        '--human-readable',
        '--del',
        '--no-whole-file',
        '--inplace',
        '--copy-links',
        '',
        '',
        ''
    ]

    list_sync_dirs = [
        'backups',
        'documents',
        'installers',
        'raisnet',
        'VirtualBox_VMs']

    # Append every element array with variable disk-source
    list_full_path_sync_dirs = [root_pth_src_drive + '/' + i for i in list_sync_dirs]

    on_test_mode = True
    off_test_mode = False

    list_rsync_func = [
        upl.upload_files(
            rsync_test_mode_wo_vdi,
            list_full_path_sync_dirs,
            name_model_recv_drive,
            path_logs_dir,
            on_test_mode),

        upl.upload_files(
            rsync_wo_vdi,
            list_full_path_sync_dirs,
            name_model_recv_drive,
            path_logs_dir,
            off_test_mode),

        upl.upload_vdi(
            rsync_test_mode_crt_vdi,
            rsync_test_mode_upd_vdi,
            list_full_path_sync_dirs[len(list_full_path_sync_dirs) - 1],
            root_pth_src_drive,
            full_path_dest_dir,
            name_model_recv_drive,
            path_logs_dir,
            on_test_mode
        ),

        upl.upload_vdi(
            rsync_crt_vdi,
            rsync_upd_vdi,
            list_full_path_sync_dirs[len(list_full_path_sync_dirs) - 1],
            root_pth_src_drive,
            full_path_dest_dir,
            name_model_recv_drive,
            path_logs_dir,
            off_test_mode
        )
    ]

    return list_rsync_func


def main():
    parser = argparse.ArgumentParser(description='Backuping drive D to external hdd')
    parser.add_argument("-a", action='store_true', help='Syncing all folders')
    parser.add_argument("--novdi", action='store_true', help='Syncing folders w/o files with extensions .vdi')

    args = vars(parser.parse_args())

    if len(sys.argv) == 1:
        sys.exit("Please, run script with argument. For more detail information use flag -h or --help")

    handler_cmd_arg(args, prepare_sync_data())

main()