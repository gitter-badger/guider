#!/usr/bin/python

__author__ = "Peace Lee"
__copyright__ = "Copyright 2015-2016, guider"
__module__ = "guider"
__credits__ = "Peace Lee"
__license__ = "GPLv2"
__version__ = "3.5.7"
__maintainer__ = "Peace Lee"
__email__ = "iipeace5@gmail.com"
__repository__ = "https://github.com/iipeace/guider"





try:
    import re
    import sys
    import signal
    import time
    import os
    import shutil
    import gc
    import imp
    import atexit
except ImportError:
    err = sys.exc_info()[1]
    print("[Error] Fail to import default packages: " + err.args[0])
    sys.exit(0)





class ConfigManager(object):
    """ Manager for configuration """

    # Define color #
    WARNING = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    SPECIAL = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


    # Define state of process #
    procStatList = {
        'R': 'running',
        'S': 'sleep',
        'D': 'disk',
        'Z': 'zombie',
        'T': 'traced',
        'W': 'paging'
        }

    # Define syscall for ARM #
    sysList_arm = [
        'sys_restart_syscall', 'sys_exit', 'sys_fork', 'sys_read', 'sys_write', 'sys_open',
        'sys_close', 'sys_sys_waitpid', 'sys_creat', 'sys_link', 'sys_unlink', #10#
        'sys_execve', 'sys_chdir', 'sys_time', 'sys_mknod', 'sys_chmod',
        'sys_lchown16', 'sys_break', 'sys_sys_stat', 'sys_lseek', 'sys_getpid', #20#
        'sys_mount', 'sys_oldumount', 'sys_setuid16', 'sys_getuid16', 'sys_stime',
        'sys_ptrace', 'sys_alarm', 'sys_fstat', 'sys_pause', 'sys_utime', #30#
        'sys_stty', 'sys_getty', 'sys_access', 'sys_nice', 'sys_ftime',
        'sys_sync', 'sys_kill', 'sys_rename', 'sys_mkdir', 'sys_rmdir', #40#
        'sys_dup', 'sys_pipe', 'sys_times', 'sys_prof', 'sys_brk',
        'sys_setgid16', 'sys_getgid16', 'sys_signal', 'sys_geteuid16', 'sys_getegid16', #50#
        'sys_acct', 'sys_umount', 'sys_lock', 'sys_ioctl', 'sys_fcntl',
        'sys_mpx', 'sys_setpgid', 'sys_ulimit', 'sys_olduname', 'sys_umask', #60#
        'sys_chroot', 'sys_ustat', 'sys_dup2', 'sys_getppid', 'sys_getpgrp',
        'sys_setsid', 'sys_sigaction', 'sys_sgetmask', 'sys_ssetmask', 'sys_setreuid16', #70#
        'sys_setregid16', 'sys_sigsuspend', 'sys_sigpending', 'sys_sethostname', 'sys_setrlimit',
        'sys_old_getrlimit', 'sys_getrusage', 'sys_gettimeofday', 'sys_settimeofday', 'sys_getgroups16', #80#
        'sys_setgroups16', 'sys_old_select', 'sys_symlink', 'sys_lstat', 'sys_readlink',
        'sys_uselib', 'sys_swapon', 'sys_reboot', 'sys_old_readdir', 'sys_old_mmap', #90#
        'sys_munmap', 'sys_truncate', 'sys_ftruncate', 'sys_fchmod', 'sys_fchown16',
        'sys_getpriority', 'sys_setpriority', 'sys_profil', 'sys_statfs', 'sys_fstatfs', #100#
        'sys_ioperm', 'sys_socketcall', 'sys_syslog', 'sys_setitimer', 'sys_getitimer',
        'sys_newstat', 'sys_newlstat', 'sys_newfstat', 'sys_uname', 'sys_iopl', #110#
        'sys_vhangup', 'sys_ni_syscall', 'sys_syscall', 'sys_wait4', 'sys_swapoff',
        'sys_sysinfo', 'sys_ipc', 'sys_fsync', 'sys_sigreturn_wrapper', 'sys_clone', #120#
        'sys_setdomainname', 'sys_newuname', 'sys_modify_ldt', 'sys_adjtimex', 'sys_mprotect',
        'sys_sigprocmask', 'sys_create_module', 'sys_init_module', 'sys_delete_module', 'sys_get_kernel_syms', #130#
        'sys_quotactl', 'sys_getpgid', 'sys_fchdir', 'sys_bdflush', 'sys_sysfs',
        'sys_personality', 'sys_afs_syscall', 'sys_setfsuid16', 'sys_setfsgid16', 'sys_llseek', #140#
        'sys_getdents', 'sys_select', 'sys_flock', 'sys_msync', 'sys_readv',
        'sys_writev', 'sys_getsid', 'sys_fdatasync', 'sys_sysctl', 'sys_mlock', #150#
        'sys_munlock', 'sys_mlockall', 'sys_munlockall', 'sys_sched_setparam', 'sys_sched_getparam',
        'sys_sched_setscheduler', 'sys_sched_getscheduler', 'sys_sched_yield', 'sys_sched_get_priority_max', #159#
        'sys_sched_get_priority_min', 'sys_sched_rr_get_interval', 'sys_nanosleep', 'sys_mremap',
        'sys_setresuid16', 'sys_getresuid16', 'sys_vm86', 'sys_query_module', 'sys_poll', 'sys_nfsservctl', #169#
        'sys_setresgid16', 'sys_getresgid16', 'sys_prctl', 'sys_rt_sigreturn_wrapper', 'sys_rt_sigaction',
        'sys_rt_sigprocmask', 'sys_rt_sigpending', 'sys_rt_sigtimedwait', 'sys_rt_sigqueueinfo', #178#
        'sys_rt_sigsuspend', 'sys_pread64', 'sys_pwrite64', 'sys_chown16', 'sys_getcwd', 'sys_capget',
        'sys_capset', 'sys_sigaltstack', 'sys_sendfile', 'sys_getpmsg', 'sys_putpmsg', 'sys_vfork', #190#
        'sys_getrlimit', 'sys_mmap2', 'sys_truncate64', 'sys_ftruncate64', 'sys_stat64', 'sys_lstat64',
        'sys_fstat64', 'sys_lchown', 'sys_getuid', 'sys_getgid', 'sys_geteuid', 'sys_getegid', #203#
        'sys_setreuid', 'sys_setregid', 'sys_getgroups', 'sys_setgroups', 'sys_fchown', 'sys_setresuid', #208#
        'sys_getresuid', 'sys_setresgid', 'sys_getresgid', 'sys_chown', 'sys_setuid', 'sys_setgid',
        'sys_setfsuid', 'sys_setfsgid', 'sys_getdents64', 'sys_pivot_root', 'sys_mincore', 'sys_madvise', #220#
        'sys_fcntl64', 'sys_TUX', 'sys_ni_syscall', 'sys_gettid', 'sys_readahead', 'sys_setxattr', 'sys_lsetxattr',
        'sys_fsetxattr', 'sys_getxattr', 'sys_lgetxattr', 'sys_fgetxattr', 'sys_listxattr', 'sys_llistxattr', #233#
        'sys_flistxattr', 'sys_removexattr', 'sys_lremovexattr', 'sys_fremovexattr', 'sys_tkill', 'sys_sendfile64',
        'sys_futex', 'sys_sched_setaffinity', 'sys_sched_getaffinity', 'sys_io_setup', 'sys_io_destroy',
        'sys_io_getevents', 'sys_io_submit', 'sys_io_cancel', 'sys_exit_group', 'sys_lookup_dcookie', #249#
        'sys_epoll_create', 'sys_epoll_ctl', 'sys_epoll_wait', 'sys_remap_file_pages', 'sys_set_thread_area',
        'sys_get_thread_area', 'sys_set_tid_address', 'sys_timer_create', 'sys_timer_settime', 'sys_timer_gettime',
        'sys_timer_getoverrun', 'sys_timer_delete', 'sys_clock_settime', 'sys_clock_gettime', 'sys_clock_getres',
        'sys_clock_nanosleep', 'sys_statfs64_wrapper', 'sys_fstatfs64_wrapper', 'sys_tgkill', 'sys_utimes', #269#
        'sys_arm_fadvise64_64', 'sys_pciconfig_iobase', 'sys_pciconfig_read', 'sys_pciconfig_write', 'sys_mq_open',
        'sys_mq_unlink', 'sys_mq_timedsend', 'sys_mq_timedreceive', 'sys_mq_notify', 'sys_mq_getsetattr', 'sys_waitid', #280#
        'sys_socket', 'sys_bind', 'sys_connect', 'sys_listen', 'sys_accept', 'sys_getsockname', 'sys_getpeername',
        'sys_socketpair', 'sys_send', 'sys_sendto', 'sys_recv', 'sys_recvfrom', 'sys_shutdown', 'sys_setsockopt',
        'sys_getsockopt', 'sys_sendmsg', 'sys_recvmsg', 'sys_semop', 'sys_semget', 'sys_semctl', #300#
        'sys_msgsnd', 'sys_msgrcv', 'sys_msgget', 'sys_msgctl', 'sys_shmat', 'sys_shmdt', 'sys_shmget', 'sys_shmctl',
        'sys_add_key', 'sys_request_key', 'sys_keyctl', 'sys_semtimedop', 'sys_vserver', 'sys_ioprio_set',
        'sys_ioprio_get', 'sys_inotify_init', 'sys_inotify_add_watch', 'sys_inotify_rm_watch', 'sys_mbind', #319#
        'sys_get_mempolicy', 'sys_set_mempolicy', 'sys_openat', 'sys_mkdirat', 'sys_mknodat', 'sys_fchownat',
        'sys_futimesat', 'sys_fstatat64', 'sys_unlinkat', 'sys_renameat', 'sys_linkat', #330#
        'sys_symlinkat', 'sys_readlinkat', 'sys_fchmodat', 'sys_faccessat', 'sys_pselect6', 'sys_ppoll',
        'sys_unshare', 'sys_set_robust_list', 'sys_get_robust_list', 'sys_splice', #340#
        'sys_sync_file_range2', 'sys_tee', 'sys_vmsplice', 'sys_move_pages', 'sys_getcpu', 'sys_epoll_pwait',
        'sys_kexec_load', 'sys_utimensat', 'sys_signalfd', 'sys_timerfd_create', 'sys_eventfd', 'sys_fallocate',
        'sys_timerfd_settime', 'sys_timerfd_gettime', 'sys_signalfd4', 'sys_eventfd2', 'sys_epoll_create1', #357#
        'sys_dup3', 'sys_pipe2', 'sys_inotify_init1', 'sys_preadv', 'sys_pwritev', 'sys_rt_tgsigqueueinfo',
        'sys_perf_event_open', 'sys_recvmmsg', 'sys_accept4', 'sys_fanotify_init', 'sys_fanotify_mark', #368#
        'sys_prlimit64', 'sys_name_to_handle_at', 'sys_open_by_handle_at', 'sys_clock_adjtime', 'sys_syncfs',
        'sys_sendmmsg', 'sys_setns', 'sys_process_vm_readv', 'sys_process_vm_writev', 'sys_kcmp', 'sys_finit_module',
        'sys_sched_setattr', 'sys_sched_getattr', 'sys_renameat2', 'sys_seccomp', 'sys_getrandom', 'sys_memfd_create',
        'sys_bpf', 'sys_execveat', 'sys_userfaultfd', 'sys_membarrier', 'sys_mlock2', 'sys_copy_file_range' #391#
        ]

    # Define syscall for x86_32 #
    sysList_x86 = [
        'sys_restart_syscall', 'sys_exit', 'sys_fork', 'sys_read', 'sys_write', 'sys_open', 'sys_close', 'sys_waitpid',
        'sys_creat', 'sys_link', 'sys_unlink', 'sys_execve', 'sys_chdir', 'sys_time', 'sys_mknod', 'sys_chmod',
        'sys_lchown', 'sys_break', 'sys_oldstat', 'sys_lseek', 'sys_getpid', 'sys_mount', 'sys_umount', 'sys_setuid',
        'sys_getuid', 'sys_stime', 'sys_ptrace', 'sys_alarm', 'sys_oldfstat', 'sys_pause', 'sys_utime', 'sys_stty',
        'sys_gtty', 'sys_access', 'sys_nice', 'sys_ftime', 'sys_sync', 'sys_kill', 'sys_rename', 'sys_mkdir',
        'sys_rmdir', 'sys_dup', 'sys_pipe', 'sys_times', 'sys_prof', 'sys_brk', 'sys_setgid', 'sys_getgid', 'sys_signal',
        'sys_geteuid', 'sys_getegid', 'sys_acct', 'sys_umount2', 'sys_lock', 'sys_ioctl', 'sys_fcntl', 'sys_mpx',
        'sys_setpgid', 'sys_ulimit', 'sys_oldolduname', 'sys_umask', 'sys_chroot', 'sys_ustat', 'sys_dup2',
        'sys_getppid', 'sys_getpgrp', 'sys_setsid', 'sys_sigaction', 'sys_sgetmask', 'sys_ssetmask', 'sys_setreuid',
        'sys_setregid', 'sys_sigsuspend', 'sys_sigpending', 'sys_sethostname', 'sys_setrlimit', 'sys_getrlimit',
        'sys_getrusage', 'sys_gettimeofday', 'sys_settimeofday', 'sys_getgroups', 'sys_setgroups', 'sys_select',
        'sys_symlink', 'sys_oldlstat', 'sys_readlink', 'sys_uselib', 'sys_swapon', 'sys_reboot', 'sys_readdir',
        'sys_mmap', 'sys_munmap', 'sys_truncate', 'sys_ftruncate', 'sys_fchmod', 'sys_fchown', 'sys_getpriority',
        'sys_setpriority', 'sys_profil', 'sys_statfs', 'sys_fstatfs', 'sys_ioperm', 'sys_socketcall', 'sys_syslog',
        'sys_setitimer', 'sys_getitimer', 'sys_stat', 'sys_lstat', 'sys_fstat', 'sys_olduname', 'sys_iopl',
        'sys_vhangup', 'sys_idle', 'sys_vm86old', 'sys_wait4', 'sys_swapoff', 'sys_sysinfo', 'sys_ipc', 'sys_fsync',
        'sys_sigreturn', 'sys_clone', 'sys_setdomainname', 'sys_uname', 'sys_modify_ldt', 'sys_adjtimex', 'sys_mprotect',
        'sys_sigprocmask', 'sys_create_module', 'sys_init_module', 'sys_delete_module', 'sys_get_kernel_syms',
        'sys_quotactl', 'sys_getpgid', 'sys_fchdir', 'sys_bdflush', 'sys_sysfs', 'sys_personality', 'sys_afs_syscall',
        'sys_setfsuid', 'sys_setfsgid', 'sys__llseek', 'sys_getdents', 'sys__newselect', 'sys_flock', 'sys_msync',
        'sys_readv', 'sys_writev', 'sys_getsid', 'sys_fdatasync', 'sys__sysctl', 'sys_mlock', 'sys_munlock',
        'sys_mlockall', 'sys_munlockall', 'sys_sched_setparam', 'sys_sched_getparam', 'sys_sched_setscheduler',
        'sys_sched_getscheduler', 'sys_sched_yield', 'sys_sched_get_priority_max', 'sys_sched_get_priority_min',
        'sys_sched_rr_get_interval', 'sys_nanosleep', 'sys_mremap', 'sys_setresuid', 'sys_getresuid', 'sys_vm86',
        'sys_query_module', 'sys_poll', 'sys_nfsservctl', 'sys_setresgid', 'sys_getresgid', 'sys_prctl',
        'sys_rt_sigreturn', 'sys_rt_sigaction', 'sys_rt_sigprocmask', 'sys_rt_sigpending', 'sys_rt_sigtimedwait',
        'sys_rt_sigqueueinfo', 'sys_rt_sigsuspend', 'sys_pread64', 'sys_pwrite64', 'sys_chown', 'sys_getcwd',
        'sys_capget', 'sys_capset', 'sys_sigaltstack', 'sys_sendfile', 'sys_getpmsg', 'sys_putpmsg', 'sys_vfork',
        'sys_ugetrlimit', 'sys_mmap2', 'sys_truncate64', 'sys_ftruncate64', 'sys_stat64', 'sys_lstat64', 'sys_fstat64',
        'sys_lchown32', 'sys_getuid32', 'sys_getgid32', 'sys_geteuid32', 'sys_getegid32', 'sys_setreuid32',
        'sys_setregid32', 'sys_getgroups32', 'sys_setgroups32', 'sys_fchown32', 'sys_setresuid32', 'sys_getresuid32',
        'sys_setresgid32', 'sys_getresgid32', 'sys_chown32', 'sys_setuid32', 'sys_setgid32', 'sys_setfsuid32',
        'sys_setfsgid32', 'sys_pivot_root', 'sys_mincore', 'sys_madvise', 'sys_getdents64', 'sys_fcntl64', 'N/A',
        'N/A', 'sys_gettid', 'sys_readahead', 'sys_setxattr', 'sys_lsetxattr', 'sys_fsetxattr', 'sys_getxattr',
        'sys_lgetxattr', 'sys_fgetxattr', 'sys_listxattr', 'sys_llistxattr', 'sys_flistxattr', 'sys_removexattr',
        'sys_lremovexattr', 'sys_fremovexattr', 'sys_tkill', 'sys_sendfile64', 'sys_futex', 'sys_sched_setaffinity',
        'sys_sched_getaffinity', 'sys_set_thread_area', 'sys_get_thread_area', 'sys_io_setup', 'sys_io_destroy',
        'sys_io_getevents', 'sys_io_submit', 'sys_io_cancel', 'sys_fadvise64', 'N/A', 'sys_exit_group',
        'sys_lookup_dcookie', 'sys_epoll_create', 'sys_epoll_ctl', 'sys_epoll_wait', 'sys_remap_file_pages',
        'sys_set_tid_address', 'sys_timer_create', 'sys_timer_settime', 'sys_timer_gettime', 'sys_timer_getoverrun',
        'sys_timer_delete', 'sys_clock_settime', 'sys_clock_gettime', 'sys_clock_getres', 'sys_clock_nanosleep',
        'sys_statfs64', 'sys_fstatfs64', 'sys_tgkill', 'sys_utimes', 'sys_fadvise64_64', 'sys_vserver', 'sys_mbind',
        'sys_get_mempolicy', 'sys_set_mempolicy', 'sys_mq_open', 'sys_mq_unlink', 'sys_mq_timedsend',
        'sys_mq_timedreceive', 'sys_mq_notify', 'sys_mq_getsetattr', 'sys_kexec_load', 'sys_waitid',
        'sys_setaltroot', 'sys_add_key', 'sys_request_key', 'sys_keyctl', 'sys_ioprio_set', 'sys_ioprio_get',
        'sys_inotify_init', 'sys_inotify_add_watch', 'sys_inotify_rm_watch', 'sys_migrate_pages', 'sys_openat',
        'sys_mkdirat', 'sys_mknodat', 'sys_fchownat', 'sys_futimesat', 'sys_fstatat64', 'sys_unlinkat', 'sys_renameat',
        'sys_linkat', 'sys_symlinkat', 'sys_readlinkat', 'sys_fchmodat', 'sys_faccessat', 'sys_pselect6', 'sys_ppoll',
        'sys_unshare', 'sys_set_robust_list', 'sys_get_robust_list', 'sys_splice', 'sys_sync_file_range', 'sys_tee',
        'sys_vmsplice', 'sys_move_pages', 'sys_getcpu', 'sys_epoll_pwait', 'sys_utimensat', 'sys_signalfd',
        'sys_timerfd_create', 'sys_eventfd', 'sys_fallocate', 'sys_timerfd_settime', 'sys_timerfd_gettime', 'sys_signalfd4',
        'sys_eventfd2', 'sys_epoll_create1', 'sys_dup3', 'sys_pipe2', 'sys_inotify_init1', 'sys_preadv', 'sys_pwritev',
        'sys_rt_tgsigqueueinfo', 'sys_perf_event_open', 'sys_recvmmsg', 'sys_fanotify_init', 'sys_fanotify_mark',
        'sys_prlimit64', 'sys_name_to_handle_at', 'sys_open_by_handle_at', 'sys_clock_adjtime', 'sys_syncfs',
        'sys_sendmmsg', 'sys_setns', 'sys_process_vm_readv', 'sys_process_vm_writev', 'sys_kcmp', 'sys_finit_module',
        'sys_sched_setattr', 'sys_sched_getattr', 'sys_renameat2', 'sys_seccomp', 'sys_getrandom', 'sys_memfd_create',
        'sys_bpf', 'sys_execveat', 'sys_socket', 'sys_socketpair', 'sys_bind', 'sys_connect', 'sys_listen', 'sys_accept4',
        'sys_getsockopt', 'sys_setsockopt', 'sys_getsockname', 'sys_getpeername', 'sys_sendto', 'sys_sendmsg',
        'sys_recvfrom', 'sys_recvmsg', 'sys_shutdown', 'sys_userfaultfd', 'sys_membarrier', 'sys_mlock2', 'sys_copy_file_range'
        ]

    # Define syscall for x86_64 #
    sysList_x64 = [
        'sys_read', 'sys_write', 'sys_open', 'sys_close', 'sys_stat', 'sys_fstat', 'sys_lstat', 'sys_poll', 'sys_lseek',
        'sys_mmap', 'sys_mprotect', 'sys_munmap', 'sys_brk', 'sys_rt_sigaction', 'sys_rt_sigprocmask', 'sys_rt_sigreturn',
        'sys_ioctl', 'sys_pread64', 'sys_pwrite64', 'sys_readv', 'sys_writev', 'sys_access', 'sys_pipe', 'sys_select',
        'sys_sched_yield', 'sys_mremap', 'sys_msync', 'sys_mincore', 'sys_madvise', 'sys_shmget', 'sys_shmat', 'sys_shmctl',
        'sys_dup', 'sys_dup2', 'sys_pause', 'sys_nanosleep', 'sys_getitimer', 'sys_alarm', 'sys_setitimer', 'sys_getpid',
        'sys_sendfile', 'sys_socket', 'sys_connect', 'sys_accept', 'sys_sendto', 'sys_recvfrom', 'sys_sendmsg', 'sys_recvmsg',
        'sys_shutdown', 'sys_bind', 'sys_listen', 'sys_getsockname', 'sys_getpeername', 'sys_socketpair', 'sys_setsockopt',
        'sys_getsockopt', 'sys_clone', 'sys_fork', 'sys_vfork', 'sys_execve', 'sys_exit', 'sys_wait4', 'sys_kill',
        'sys_uname', 'sys_semget', 'sys_semop', 'sys_semctl', 'sys_shmdt', 'sys_msgget', 'sys_msgsnd', 'sys_msgrcv',
        'sys_msgctl', 'sys_fcntl', 'sys_flock', 'sys_fsync', 'sys_fdatasync', 'sys_truncate', 'sys_ftruncate',
        'sys_getdents', 'sys_getcwd', 'sys_chdir', 'sys_fchdir', 'sys_rename', 'sys_mkdir', 'sys_rmdir', 'sys_creat',
        'sys_link', 'sys_unlink', 'sys_symlink', 'sys_readlink', 'sys_chmod', 'sys_fchmod', 'sys_chown', 'sys_fchown',
        'sys_lchown', 'sys_umask', 'sys_gettimeofday', 'sys_getrlimit', 'sys_getrusage', 'sys_sysinfo', 'sys_times',
        'sys_ptrace', 'sys_getuid', 'sys_syslog', 'sys_getgid', 'sys_setuid', 'sys_setgid', 'sys_geteuid', 'sys_getegid',
        'sys_setpgid', 'sys_getppid', 'sys_getpgrp', 'sys_setsid', 'sys_setreuid', 'sys_setregid', 'sys_getgroups',
        'sys_setgroups', 'sys_setresuid', 'sys_getresuid', 'sys_setresgid', 'sys_getresgid', 'sys_getpgid', 'sys_setfsuid',
        'sys_setfsgid', 'sys_getsid', 'sys_capget', 'sys_capset', 'sys_rt_sigpending', 'sys_rt_sigtimedwait',
        'sys_rt_sigqueueinfo', 'sys_rt_sigsuspend', 'sys_sigaltstack', 'sys_utime', 'sys_mknod', 'sys_uselib',
        'sys_personality', 'sys_ustat', 'sys_statfs', 'sys_fstatfs', 'sys_sysfs', 'sys_getpriority', 'sys_setpriority',
        'sys_sched_setparam', 'sys_sched_getparam', 'sys_sched_setscheduler', 'sys_sched_getscheduler',
        'sys_sched_get_priority_max', 'sys_sched_get_priority_min', 'sys_sched_rr_get_interval', 'sys_mlock',
        'sys_munlock', 'sys_mlockall', 'sys_munlockall', 'sys_vhangup', 'sys_modify_ldt', 'sys_pivot_root',
        'sys__sysctl', 'sys_prctl', 'sys_arch_prctl', 'sys_adjtimex', 'sys_setrlimit', 'sys_chroot', 'sys_sync',
        'sys_acct', 'sys_settimeofday', 'sys_mount', 'sys_umount2', 'sys_swapon', 'sys_swapoff', 'sys_reboot',
        'sys_sethostname', 'sys_setdomainname', 'sys_iopl', 'sys_ioperm', 'sys_create_module', 'sys_init_module',
        'sys_delete_module', 'sys_get_kernel_syms', 'sys_query_module', 'sys_quotactl', 'sys_nfsservctl', 'sys_getpmsg',
        'sys_putpmsg', 'sys_afs_syscall', 'sys_tuxcall', 'sys_security', 'sys_gettid', 'sys_readahead', 'sys_setxattr',
        'sys_lsetxattr', 'sys_fsetxattr', 'sys_getxattr', 'sys_lgetxattr', 'sys_fgetxattr', 'sys_listxattr',
        'sys_llistxattr', 'sys_flistxattr', 'sys_removexattr', 'sys_lremovexattr', 'sys_fremovexattr', 'sys_tkill',
        'sys_time', 'sys_futex', 'sys_sched_setaffinity', 'sys_sched_getaffinity', 'sys_set_thread_area', 'sys_io_setup',
        'sys_io_destroy', 'sys_io_getevents', 'sys_io_submit', 'sys_io_cancel', 'sys_get_thread_area', 'sys_lookup_dcookie',
        'sys_epoll_create', 'sys_epoll_ctl_old', 'sys_epoll_wait_old', 'sys_remap_file_pages', 'sys_getdents64',
        'sys_set_tid_address', 'sys_restart_syscall', 'sys_semtimedop', 'sys_fadvise64', 'sys_timer_create',
        'sys_timer_settime', 'sys_timer_gettime', 'sys_timer_getoverrun', 'sys_timer_delete', 'sys_clock_settime',
        'sys_clock_gettime', 'sys_clock_getres', 'sys_clock_nanosleep', 'sys_exit_group', 'sys_epoll_wait',
        'sys_epoll_ctl', 'sys_tgkill', 'sys_utimes', 'sys_vserver', 'sys_mbind', 'sys_set_mempolicy', 'sys_get_mempolicy',
        'sys_mq_open', 'sys_mq_unlink', 'sys_mq_timedsend', 'sys_mq_timedreceive', 'sys_mq_notify', 'sys_mq_getsetattr',
        'sys_kexec_load', 'sys_waitid', 'sys_add_key', 'sys_request_key', 'sys_keyctl', 'sys_ioprio_set', 'sys_ioprio_get',
        'sys_inotify_init', 'sys_inotify_add_watch', 'sys_inotify_rm_watch', 'sys_migrate_pages', 'sys_openat',
        'sys_mkdirat', 'sys_mknodat', 'sys_fchownat', 'sys_futimesat', 'sys_newfstatat', 'sys_unlinkat', 'sys_renameat',
        'sys_linkat', 'sys_symlinkat', 'sys_readlinkat', 'sys_fchmodat', 'sys_faccessat', 'sys_pselect6', 'sys_ppoll',
        'sys_unshare', 'sys_set_robust_list', 'sys_get_robust_list', 'sys_splice', 'sys_tee', 'sys_sync_file_range',
        'sys_vmsplice', 'sys_move_pages', 'sys_utimensat', 'sys_epoll_pwait', 'sys_signalfd', 'sys_timerfd_create',
        'sys_eventfd', 'sys_fallocate', 'sys_timerfd_settime', 'sys_timerfd_gettime', 'sys_accept4', 'sys_signalfd4',
        'sys_eventfd2', 'sys_epoll_create1', 'sys_dup3', 'sys_pipe2', 'sys_inotify_init1', 'sys_preadv', 'sys_pwritev',
        'sys_rt_tgsigqueueinfo', 'sys_perf_event_open', 'sys_recvmmsg', 'sys_fanotify_init', 'sys_fanotify_mark',
        'sys_prlimit64', 'sys_name_to_handle_at', 'sys_open_by_handle_at', 'sys_clock_adjtime', 'sys_syncfs',
        'sys_sendmmsg', 'sys_setns', 'sys_getcpu', 'sys_process_vm_readv', 'sys_process_vm_writev', 'sys_kcmp',
        'sys_finit_module', 'sys_sched_setattr', 'sys_sched_getattr', 'sys_renameat2', 'sys_seccomp', 'sys_getrandom',
        'sys_memfd_create', 'sys_kexec_file_load', 'sys_bpf', 'sys_execveat', 'sys_userfaultfd', 'sys_membarrier',
        'sys_mlock2', 'sys_copy_file_range'
        ]

    # Set default syscall table to arm #
    sysList = sysList_arm

    # Define signal #
    sigList = [
        'SIGHUP', 'SIGINT', 'SIGQUIT', 'SIGILL', 'SIGTRAP', 'SIGABRT', 'SIGIOT', 'SIGBUS', 'SIGFPE', 'SIGKILL', #9#
        'SIGUSR1', 'SIGSEGV', 'SIGUSR2', 'SIGPIPE', 'SIGALRM', 'SIGTERM', 'SIGSTKFLT', 'SIGCHLD', 'SIGCONT', #18#
        'SIGSTOP', 'SIGTSTP', 'SIGTTIN', 'SIGTTOU', 'SIGURG', 'SIGXCPU', 'SIGXFSZ', 'SIGVTALRM', 'SIGPROF', #27#
        'SIGWINCH', 'SIGIO', 'SIGPWR', 'SIGSYS' #31#
        ]

    # stat list from http://linux.die.net/man/5/proc #
    statList = [
        'PID', 'COMM', 'STATE', 'PPID', 'PGRP', 'SESSIONID', 'NRTTY', 'TPGID', 'FLAGS', 'MINFLT', 'CMINFLT', #10#
        'MAJFLT', 'CMAJFLT', 'UTIME', 'STIME', 'CUTIME', 'CSTIME', 'PRIORITY', 'NICE', 'NRTHREAD', 'ITERALVAL', #20#
        'STARTTIME', 'VSIZE', 'RSS', 'RSSLIM', 'STARTCODE', 'ENDCODE', 'STARTSTACK', 'SP', 'PC', 'SIGNAL', #30#
        'BLOCKED', 'SIGIGNORE', 'SIGCATCH', 'WCHEN', 'NSWAP', 'CNSWAP', 'EXITSIGNAL', 'PROCESSOR', 'RTPRIORITY', #39#
        'POLICY', 'DELAYBLKTICK', 'GUESTTIME', 'CGUESTTIME' # 43 #
        ]

    schedList = [
        'C', # 0: CFS #
        'F', # 1: FIFO #
        'R', # 2: RR #
        'B', # 3: BATCH #
        'N', # 4: NONE #
        'I', # 5: IDLE #
        ]

    taskChainEnable = None



    @staticmethod
    def readProcData(tid, file, num):
        file = '/proc/'+ tid + '/' + file

        try:
            f = open(file, 'r')
        except:
            SystemManager.printError("Fail to open %s" % (file))
            return None

        if num == 0:
            return f.readline().replace('\n', '')
        else:
            return f.readline().replace('\n', '').split(' ')[num - 1]



    @staticmethod
    def getMmapId():
        if SystemManager.arch == 'arm':
            return ConfigManager.sysList.index('sys_mmap2')
        else:
            return ConfigManager.sysList.index('sys_mmap')



    @staticmethod
    def openConfFile(file):
        file += '.tc'
        if os.path.isfile(file) is True:
            SystemManager.printWarning(\
                "%s already exist, make new one" % file)

        try:
            fd = open(file, 'w')
        except:
            SystemManager.printError("Fail to open %s" % (file))
            return None

        return fd




    @staticmethod
    def writeConfData(fd, line):
        if fd == None:
            SystemManager.printError("Fail to get file descriptor")
            return None

        fd.write(line)



    def __init__(self, mode):
        pass



    def __del__(self):
        pass



class NetworkManager(object):
    """ Manager for remote communication """

    def __init__(self, mode):
        try:
            from socket import socket, AF_INET, SOCK_DGRAM
        except ImportError:
            err = sys.exc_info()[1]
            print("[Error] Fail to import package: " + err.args[0])
            sys.exit(0)

        if mode is 'server':
            serverSocket = socket(AF_INET, SOCK_DGRAM)
            serverSocket.bind(('', 12000))

            while True:
                message, address = serverSocket.recvfrom(1024)
                message = message.upper()
                serverSocket.sendto(message, address)
        elif mode is 'client':
            clientSocket = socket(AF_INET, SOCK_DGRAM)
            clientSocket.settimeout(1)
            message = 'test'
            addr = ("127.0.0.1", 12000)

            clientSocket.sendto(message, addr)

            try:
                data, server = clientSocket.recvfrom(1024)
                print('%s %d' % (data, pings))
            except timeout:
                print('REQUEST TIMED OUT')



    def __del__(self):
        pass



class FunctionAnalyzer(object):
    """ Analyzer for function profiling """

    symStackIdxTable = [
        'CPU_TICK', 'STACK', 'PAGE_ALLOC', 'PAGE_FREE', 'BLK_READ', \
        'ARGUMENT', 'HEAP_EXPAND', 'HEAP_REDUCE', 'IGNORE', 'BLK_WRITE', 'CUSTOM'
        ]



    def __init__(self, logFile):
        self.cpuEnabled = False
        self.memEnabled = False
        self.heapEnabled = False
        self.breadEnabled = False
        self.bwriteEnabled = False
        self.sigEnabled = False

        self.sort = 'sym'

        self.startTime = '0'
        self.finishTime = '0'
        self.totalTime = 0
        self.totalTick = 0
        self.prevTime = '0'
        self.prevTid = '0'

        self.lastCore = None
        self.coreCtx = {}
        self.nowCtx = None
        self.nowEvent = None
        self.savedEvent = None
        self.nestedEvent = None
        self.nowCnt = 0
        self.savedCnt = 0
        self.nestedCnt = 0
        self.nowArg = 0
        self.savedArg = 0
        self.nestedArg = 0

        self.duplicatedPos = 0
        self.periodicEventCnt = 0
        self.periodicContEventCnt = 0
        self.periodicEventInterval = 0
        self.heapExpEventCnt = 0
        self.heapExpSize = 0
        self.heapRedEventCnt = 0
        self.heapRedSize = 0
        self.pageAllocEventCnt = 0
        self.pageAllocCnt = 0
        self.pageFreeEventCnt = 0
        self.pageFreeCnt = 0
        self.pageUnknownFreeCnt = 0
        self.pageUsageCnt = 0
        self.blockRdEventCnt = 0
        self.blockRdUsageCnt = 0
        self.blockWrEventCnt = 0
        self.blockWrUsageCnt = 0
        self.customCnt = 0
        self.customTotal = 0

        self.customEventTable = {}
        self.ignoreTable = {}
        self.mapData = []
        self.pageTable = {}
        self.oldPageTable = {}
        self.heapTable = {}
        self.oldHeapTable = {}
        self.posData = {}
        self.userSymData = {}
        self.kernelSymData = {}
        self.threadData = {}
        self.userCallData = []
        self.kernelCallData = []
        '''
        userCallData = kernelCallData = [pos, stack, event, eventCnt, eventArg]
        '''

        self.init_threadData = \
            {'comm': '', 'tgid': '-'*5, 'target': False, 'cpuTick': int(0), 'die': False, 'new': False, \
            'nrPages': int(0), 'userPages': int(0), 'cachePages': int(0), 'kernelPages': int(0), 'nrRdBlocks': int(0), \
            'heapSize': int(0), 'eventCnt': int(0), 'nrWrBlocks': int(0), 'nrUnknownFreePages': int(0), \
            'customCnt': int(0), 'customTotal': int(0)}

        self.init_posData = \
            {'symbol': '', 'binary': '', 'origBin': '', 'offset': hex(0), 'posCnt': int(0), 'unknownPageFreeCnt': int(0), \
            'userPageCnt': int(0), 'cachePageCnt': int(0), 'kernelPageCnt': int(0), 'totalCnt': int(0), 'src': '', \
            'blockRdCnt': int(0), 'blockWrCnt': int(0), 'pageCnt': int(0), 'heapSize': int(0), 'customCnt': int(0), \
            'customTotal': int(0)}

        self.init_symData = \
            {'pos': '', 'origBin': '', 'cnt': int(0), 'blockRdCnt': int(0), 'pageCnt': int(0), 'unknownPageFreeCnt': int(0), \
            'userPageCnt': int(0), 'cachePageCnt': int(0), 'kernelPageCnt': int(0), 'stack': None, 'symStack': None, \
            'heapSize': int(0), 'blockWrCnt': int(0), 'customCnt': int(0), 'customTotal': int(0)}

        self.init_ctxData = \
            {'nestedEvent': None, 'savedEvent': None, 'nowEvent': None, 'nested': int(0), 'recStat': bool(False), \
            'nestedCnt': int(0), 'savedCnt': int(0), 'nowCnt': int(0), 'nestedArg': None, 'savedArg': None, \
            'prevMode': None, 'curMode': None, 'userLastPos': '', 'userCallStack': None, 'kernelLastPos': '', \
            'kernelCallStack': None, 'bakKernelLastPos': '', 'bakKernelCallStack': None, 'nowArg': None, \
            'prevTid': None, 'prevTime': None}

        self.init_pageLinkData = \
            {'sym': '0', 'subStackAddr': int(0), 'kernelSym': '0', 'kernelSubStackAddr': int(0), \
            'type': '0', 'time': '0'}

        self.init_heapSegData = {'tid': '0', 'size': int(0), 'sym': '0', 'subStackAddr': int(0), \
            'kernelSym': '0', 'kernelSubStackAddr': int(0)}

        self.init_pageData = {'tid': '0', 'page': '0', 'flags': '0', 'type': '0', 'time': '0'}

        self.init_subStackPageInfo = [0, 0, 0]
        # subStackPageInfo = [userPageCnt, cachePageCnt, kernelPageCnt]

        # Open log file #
        try:
            logFd = open(logFile, 'r')
        except:
            SystemManager.printError("Fail to open %s to create callstack information" % logFile)
            sys.exit(0)

        SystemManager.printStatus('start analyzing data... [ STOP(ctrl + c) ]')

        # Get binary and offset info #
        lines = logFd.readlines()

        # Save data and exit if output file is set #
        SystemManager.saveDataAndExit(lines)

        # Check target thread setting #
        if len(SystemManager.showGroup) == 0:
            SystemManager.showGroup.insert(0, '')
            self.target = []
        else:
            for tid in SystemManager.showGroup:
                try:
                    int(tid)
                except:
                    SystemManager.printError(\
                        "Fail to use filter value %s, use -g option with number as thread id" % tid)
                    sys.exit(0)
            self.target = SystemManager.showGroup

        # Check root path #
        if SystemManager.rootPath is None:
            SystemManager.printError(\
                "Fail to recognize sysroot path for target, use also -r option with blank or path for user mode")
            sys.exit(0)

        # Register None pos #
        self.posData['0'] = dict(self.init_posData)

        # Parse logs #
        SystemManager.totalLine = len(lines)
        self.parseLogs(lines, SystemManager.showGroup)

        # Check whether data of target thread is collected or nothing #
        if len(self.userCallData) == 0 and len(self.kernelCallData) == 0 and len(self.target) > 0:
            SystemManager.printError("No collected data related to %s" % self.target)
            sys.exit(0)
        elif len(self.userCallData) == 1 and self.userCallData[0][0] == '0':
            SystemManager.printError("No user stack data related to %s, " % self.target + \
                "enable CONFIG_USER_STACKTRACE_SUPPORT option in kernel")
            sys.exit(0)

        # Get symbols from call address #
        SystemManager.printStatus('start resolving symbols... [ STOP(ctrl + c) ]')
        self.getSymbols()

        # Merge callstacks by symbol and address #
        SystemManager.printStatus('start summarizing functions... [ STOP(ctrl + c) ]')
        self.mergeStacks()



    def __del__(self):
        pass



    def handleHeapExpand(self, sym, kernelSym, stackAddr, kernelStackAddr, size, addr):
        self.userSymData[sym]['heapSize'] += size
        self.kernelSymData[kernelSym]['heapSize'] += size

        try:
            self.heapTable[addr]['size'] = size
        except:
            self.heapTable[addr] = dict(self.init_heapSegData)
            self.heapTable[addr]['size'] = size

        self.heapTable[addr]['sym'] = sym
        self.heapTable[addr]['kernelSym'] = kernelSym
        self.heapTable[addr]['subStackAddr'] = stackAddr
        self.heapTable[addr]['kernelSubStackAddr'] = kernelStackAddr

        # Set user target stack #
        if self.sort is 'sym':
            targetStack = self.userSymData[sym]['symStack']
        elif self.sort is 'pos':
            targetStack = self.userSymData[sym]['stack']



    def handleHeapReduce(self, size, addr):
        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        heapExpIndex = FunctionAnalyzer.symStackIdxTable.index('HEAP_EXPAND')

        try:
            sym = self.heapTable[addr]['sym']
            kernelSym = self.heapTable[addr]['kernelSym']
            stackAddr = self.heapTable[addr]['subStackAddr']
            kernelStackAddr= self.heapTable[addr]['kernelSubStackAddr']

            self.userSymData[sym]['heapSize'] -= size
            self.kernelSymData[kernelSym]['heapSize'] -= size
        except:
            SystemManager.printWarning("Fail to find heap segment to be freed")
            return

        # Set user target stack #
        if self.sort is 'sym':
            targetStack = self.userSymData[sym]['symStack']
        elif self.sort is 'pos':
            targetStack = self.userSymData[sym]['stack']

        # Find subStack of symbol allocated this segment #
        for val in targetStack:
            if id(val[subStackIndex]) == stackAddr:
                # Increase heap count of subStack #
                val[heapExpIndex] -= size
                break

        # Set kernel target stack #
        kernelTargetStack = self.kernelSymData[kernelSym]['stack']

        # Find subStack of symbol allocated this segment #
        for val in kernelTargetStack:
            if id(val[subStackIndex]) == kernelStackAddr:
                # Increase heap count of subStack #
                val[heapExpIndex] -= size
                break

        del self.heapTable[addr]
        self.heapTable[addr] = {}



    def handlePageFree(self, sym, kernelSym, stackAddr, kernelStackAddr, pageFreeCnt, pageType, pfn):
        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        pageAllocIndex = FunctionAnalyzer.symStackIdxTable.index('PAGE_ALLOC')
        pageFreeIndex = FunctionAnalyzer.symStackIdxTable.index('PAGE_FREE')
        argIndex = FunctionAnalyzer.symStackIdxTable.index('ARGUMENT')

        for cnt in range(0, pageFreeCnt):
            pfnv = pfn + cnt
            subStackPageInfoIdx = 0

            try:
                # Decrease page count of symbol allocated page  #
                # toDo: fix bug about wrong count of pos #
                allocSym = self.pageTable[pfnv]['sym']
                allocStackAddr = self.pageTable[pfnv]['subStackAddr']
                allocKernelSym = self.pageTable[pfnv]['kernelSym']
                allocKernelStackAddr = self.pageTable[pfnv]['kernelSubStackAddr']


                self.pageUsageCnt -= 1
                self.userSymData[allocSym]['pageCnt'] -= 1
                self.kernelSymData[allocKernelSym]['pageCnt'] -= 1

                if pageType is 'USER':
                    self.userSymData[allocSym]['userPageCnt'] -= 1
                    self.kernelSymData[allocKernelSym]['userPageCnt'] -= 1
                    subStackPageInfoIdx = 0
                elif pageType is 'CACHE':
                    self.userSymData[allocSym]['cachePageCnt'] -= 1
                    self.kernelSymData[allocKernelSym]['cachePageCnt'] -= 1
                    subStackPageInfoIdx = 1
                elif pageType is 'KERNEL':
                    self.userSymData[allocSym]['kernelPageCnt'] -= 1
                    self.kernelSymData[allocKernelSym]['kernelPageCnt'] -= 1
                    subStackPageInfoIdx = 2

                # Set user target stack #
                if self.sort is 'sym':
                    targetStack = self.userSymData[allocSym]['symStack']
                elif self.sort is 'pos':
                    targetStack = self.userSymData[allocSym]['stack']

                # Find subStack allocated this page #
                for val in targetStack:
                    if id(val[subStackIndex]) == allocStackAddr:
                        val[pageAllocIndex] -= 1
                        val[argIndex][subStackPageInfoIdx] -= 1
                        break

                # Set kernel target stack #
                kernelTargetStack = self.kernelSymData[allocKernelSym]['stack']

                # Find subStack allocated this page #
                for val in kernelTargetStack:
                    if id(val[subStackIndex]) == allocKernelStackAddr:
                        val[pageAllocIndex] -= 1
                        val[argIndex][subStackPageInfoIdx] -= 1
                        break

                del self.pageTable[pfnv]
                self.pageTable[pfnv] = None
            except:
                # this page is allocated before starting profile #

                self.pageUnknownFreeCnt += 1
                self.userSymData[sym]['unknownPageFreeCnt'] += 1
                self.kernelSymData[kernelSym]['unknownPageFreeCnt'] += 1

                # Set user target stack #
                if self.sort is 'sym':
                    targetStack = self.userSymData[sym]['symStack']
                elif self.sort is 'pos':
                    targetStack = self.userSymData[sym]['stack']

                # Find subStack allocated this page #
                for val in targetStack:
                    if id(val[subStackIndex]) == stackAddr:
                        val[pageFreeIndex] += 1
                        break

                # Set kernel target stack #
                kernelTargetStack = self.kernelSymData[kernelSym]['stack']

                # Find subStack allocated this page #
                for val in kernelTargetStack:
                    if id(val[subStackIndex]) == kernelStackAddr:
                        val[pageFreeIndex] += 1
                        break

                continue



    def handlePageAlloc(self, sym, kernelSym, stackAddr, kernelStackAddr, pageAllocCnt, pageType, pfn):
        subStackPageInfoIdx = 0

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        pageAllocIndex = FunctionAnalyzer.symStackIdxTable.index('PAGE_ALLOC')
        argIndex = FunctionAnalyzer.symStackIdxTable.index('ARGUMENT')

        # Increase counts of page to be allocated #
        self.userSymData[sym]['pageCnt'] += pageAllocCnt
        self.kernelSymData[kernelSym]['pageCnt'] += pageAllocCnt

        if pageType == 'USER':
            self.userSymData[sym]['userPageCnt'] += pageAllocCnt
            self.kernelSymData[kernelSym]['userPageCnt'] += pageAllocCnt
            subStackPageInfoIdx = 0
        elif pageType == 'CACHE':
            self.userSymData[sym]['cachePageCnt'] += pageAllocCnt
            self.kernelSymData[kernelSym]['cachePageCnt'] += pageAllocCnt
            subStackPageInfoIdx = 1
        elif pageType == 'KERNEL':
            self.userSymData[sym]['kernelPageCnt'] += pageAllocCnt
            self.kernelSymData[kernelSym]['kernelPageCnt'] += pageAllocCnt
            subStackPageInfoIdx = 2

        # Set user target stack #
        if self.sort is 'sym':
            targetStack = self.userSymData[sym]['symStack']
        elif self.sort is 'pos':
            targetStack = self.userSymData[sym]['stack']

        # Find subStack of symbol allocated this page #
        for val in targetStack:
            if id(val[subStackIndex]) == stackAddr:
                # Increase page count of subStack #
                val[argIndex][subStackPageInfoIdx] += pageAllocCnt
                break

        # Set kernel target stack #
        kernelTargetStack = self.kernelSymData[kernelSym]['stack']

        # Find subStack of symbol allocated this page #
        for val in kernelTargetStack:
            if id(val[subStackIndex]) == kernelStackAddr:
                # Increase page count of subStack #
                val[argIndex][subStackPageInfoIdx] += pageAllocCnt
                break

        # Make PTE in page table #
        for cnt in range(0, pageAllocCnt):
            pfnv = pfn + cnt
            subStackPageInfoIdx = 0

            try:
                # Check whether this page is already allocated #
                allocSym = self.pageTable[pfnv]['sym']

                allocStackAddr = self.pageTable[pfnv]['subStackAddr']
                allocKernelSym = self.pageTable[pfnv]['kernelSym']
                allocKernelStackAddr = self.pageTable[pfnv]['kernelSubStackAddr']

                # Decrease counts of page already allocated but no free log #
                self.pageUsageCnt -= 1
                self.userSymData[allocSym]['pageCnt'] -= 1
                self.kernelSymData[allocKernelSym]['pageCnt'] -= 1

                origPageType = self.pageTable[pfnv]['type']
                if origPageType == 'USER':
                    self.userSymData[allocSym]['userPageCnt'] -= 1
                    self.kernelSymData[allocKernelSym]['userPageCnt'] -= 1
                    subStackPageInfoIdx = 0
                elif origPageType == 'CACHE':
                    self.userSymData[allocSym]['cachePageCnt'] -= 1
                    self.kernelSymData[allocKernelSym]['cachePageCnt'] -= 1
                    subStackPageInfoIdx = 1
                elif origPageType == 'KERNEL':
                    self.userSymData[allocSym]['kernelPageCnt'] -= 1
                    self.kernelSymData[allocKernelSym]['kernelPageCnt'] -= 1
                    subStackPageInfoIdx = 2

                # Set user target stack #
                if self.sort is 'sym':
                    targetStack = self.userSymData[allocSym]['symStack']
                elif self.sort is 'pos':
                    targetStack = self.userSymData[allocSym]['stack']

                # Find user subStack of symbol allocated this page #
                for val in targetStack:
                    if id(val[subStackIndex]) == allocStackAddr:
                        # Decrease allocated page count of substack #
                        val[pageAllocIndex] -= 1
                        val[argIndex][subStackPageInfoIdx] -= 1
                        break

                # Set kernel target stack #
                kernelTargetStack = self.kernelSymData[allocKernelSym]['stack']

                # Find user subStack of symbol allocated this page #
                for val in kernelTargetStack:
                    if id(val[subStackIndex]) == allocKernelStackAddr:
                        # Decrease allocated page count of substack #
                        val[pageAllocIndex] -= 1
                        val[argIndex][subStackPageInfoIdx] -= 1
                        break
            except:
                self.pageTable[pfnv] = dict(self.init_pageLinkData)

            self.pageTable[pfnv]['sym'] = sym
            self.pageTable[pfnv]['kernelSym'] = kernelSym
            self.pageTable[pfnv]['type'] = pageType
            self.pageTable[pfnv]['subStackAddr'] = stackAddr
            self.pageTable[pfnv]['kernelSubStackAddr'] = kernelStackAddr



    def mergeStacks(self):
        sym = ''
        kernelSym = ''
        stackAddr = 0
        kernelStackAddr = 0
        lineCnt = -1
        lastIdx = len(self.userCallData)

        # Backup page table used previously and Initialize it #
        self.oldPageTable = self.pageTable
        self.pageTable = {}

        # Backup heap table used previously and Initialize it #
        self.oldHeapTable = self.heapTable
        self.heapTable = {}

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        argIndex = FunctionAnalyzer.symStackIdxTable.index('ARGUMENT')

        # Merge call data by symbol or address #
        for val in self.userCallData:
            lineCnt += 1
            SystemManager.printProgress(lineCnt, lastIdx)

            pos = val[0]
            stack = val[1]
            event = val[2]
            eventCnt = val[3]
            arg = val[4]

            # Do not merge PAGE_FREE count because it will be merged with unknownPageFreeCnt #
            if event == 'PAGE_FREE':
                savedEventCnt = eventCnt
                eventCnt = 0

            try:
                eventIndex = FunctionAnalyzer.symStackIdxTable.index(event)
            except:
                eventIndex = FunctionAnalyzer.symStackIdxTable.index('IGNORE')

            kernelPos = self.kernelCallData[lineCnt][0]
            kernelStack = self.kernelCallData[lineCnt][1]
            subStackPageInfo = list(self.init_subStackPageInfo)

            targetStack = []
            kernelTargetStack = []

            # Resolve user symbol #
            try:
                # No symbol related to last pos #
                if self.posData[pos]['symbol'] == '':
                    self.posData[pos]['symbol'] = pos
                    sym = pos
                else:
                    sym = self.posData[pos]['symbol']
            except:
                continue

            # Resolve kernel symbol #
            try:
                # No symbol related to last pos #
                if self.posData[kernelPos]['symbol'] == '':
                    self.posData[kernelPos]['symbol'] = kernelPos
                    kernelSym = kernelPos
                else:
                    kernelSym = self.posData[kernelPos]['symbol']
            except:
                continue

            # Make user symbol table of last pos in stack #
            try:
                self.userSymData[sym]
            except:
                self.userSymData[sym] = dict(self.init_symData)
                self.userSymData[sym]['stack'] = []
                self.userSymData[sym]['symStack'] = []
                self.userSymData[sym]['pos'] = pos
                self.userSymData[sym]['origBin'] = self.posData[pos]['origBin']

            # Make kenel symbol table of last pos in stack #
            try:
                self.kernelSymData[kernelSym]
            except:
                self.kernelSymData[kernelSym] = dict(self.init_symData)
                self.kernelSymData[kernelSym]['stack'] = []
                self.kernelSymData[kernelSym]['pos'] = kernelPos

            # Set target user stack #
            if self.sort is 'sym':
                tempSymStack = []
                # Make temporary symbol stack to merge stacks by symbol #
                for addr in stack:
                    tempSym = self.posData[addr]['symbol']

                    # Ignore this function if there is no symbol #
                    if SystemManager.showAll is False and \
                        self.posData[addr]['origBin'] == '??' and \
                        (tempSym == addr or tempSym == self.posData[addr]['offset']):
                        continue

                    # No symbol data #
                    if tempSym == '':
                        if self.posData[addr]['origBin'] == '??':
                            tempSym = '%x' % int(self.posData[addr]['pos'], 16)
                        else:
                            tempSym = '%x' % int(self.posData[addr]['offset'], 16)

                    try:
                        self.userSymData[tempSym]
                    except:
                        self.userSymData[tempSym] = dict(self.init_symData)
                        self.userSymData[tempSym]['stack'] = []
                        self.userSymData[tempSym]['symStack'] = []
                        self.userSymData[tempSym]['pos'] = addr
                        self.userSymData[tempSym]['origBin'] = self.posData[addr]['origBin']

                    tempSymStack.append(tempSym)

                # Switch input stack to symbol stack #
                stack = tempSymStack
                targetStack = self.userSymData[sym]['symStack']
            elif self.sort is 'pos':
                targetStack = self.userSymData[sym]['stack']

            # First user stack related to this symbol #
            if len(targetStack) == 0:
                tempList = [0] * len(FunctionAnalyzer.symStackIdxTable)
                tempList[eventIndex] = eventCnt
                tempList[subStackIndex] = stack
                tempList[argIndex] = list(subStackPageInfo)
                targetStack.append(tempList)

                stackAddr = id(stack)
            else:
                found = False

                # Find same stack by pos in stack list #
                for stackInfo in targetStack:
                    # Found same stack #
                    if len(list(set(stack) - set(stackInfo[subStackIndex]))) == 0 and \
                        len(list(set(stackInfo[subStackIndex]) - set(stack))) == 0:
                        found = True

                        stackInfo[eventIndex] += eventCnt
                        stackAddr = id(stackInfo[subStackIndex])

                        break

                # New stack related to this symbol #
                if found == False:
                    tempList = [0] * len(FunctionAnalyzer.symStackIdxTable)
                    tempList[eventIndex] = eventCnt
                    tempList[subStackIndex] = stack
                    tempList[argIndex] = list(subStackPageInfo)
                    targetStack.append(tempList)

                    stackAddr = id(stack)

            # Set target kernel stack #
            kernelTargetStack = self.kernelSymData[kernelSym]['stack']

            # First stack related to this symbol #
            if len(kernelTargetStack) == 0:
                tempList = [0] * len(FunctionAnalyzer.symStackIdxTable)
                tempList[eventIndex] = eventCnt
                tempList[subStackIndex] = kernelStack
                tempList[argIndex] = list(subStackPageInfo)
                kernelTargetStack.append(tempList)

                kernelStackAddr = id(kernelStack)
            else:
                found = False
                for stackInfo in kernelTargetStack:
                    # Found same stack  in stack list #
                    if len(list(set(kernelStack) - set(stackInfo[subStackIndex]))) == 0 and \
                        len(list(set(stackInfo[subStackIndex]) - set(kernelStack))) == 0:
                        found = True
                        stackInfo[eventIndex] += eventCnt
                        kernelStackAddr = id(stackInfo[subStackIndex])
                        break

                # New stack related to this symbol #
                if found == False:
                    tempList = [0] * len(FunctionAnalyzer.symStackIdxTable)
                    tempList[eventIndex] = eventCnt
                    tempList[subStackIndex] = kernelStack
                    tempList[argIndex] = list(subStackPageInfo)
                    kernelTargetStack.append(tempList)

                    kernelStackAddr = id(kernelStack)

            # Recover PAGE_FREE count to merge with unknownPageFreeCnt #
            if event == 'PAGE_FREE':
                eventCnt = savedEventCnt

            # memory allocation event #
            if event == 'PAGE_ALLOC':
                pageType = arg[0]
                pfn = arg[1]

                self.handlePageAlloc(sym, kernelSym, stackAddr, kernelStackAddr, eventCnt, pageType, pfn)

            # memory free event #
            elif event == 'PAGE_FREE':
                pageType = arg[0]
                pfn = arg[1]

                self.handlePageFree(sym, kernelSym, stackAddr, kernelStackAddr, eventCnt, pageType, pfn)

            # heap expand event #
            elif event == 'HEAP_EXPAND':
                addr = arg

                self.handleHeapExpand(sym, kernelSym, stackAddr, kernelStackAddr, eventCnt, addr)

            # heap expand event #
            elif event == 'HEAP_REDUCE':
                addr = arg

                self.handleHeapReduce(eventCnt, addr)

            # block read event #
            elif event == 'BLK_READ':
                self.userSymData[sym]['blockRdCnt'] += eventCnt
                self.kernelSymData[kernelSym]['blockRdCnt'] += eventCnt

            # block write event #
            elif event == 'BLK_WRITE':
                self.userSymData[sym]['blockWrCnt'] += eventCnt
                self.kernelSymData[kernelSym]['blockWrCnt'] += eventCnt

            # periodic event such as cpu tick #
            elif event == 'CPU_TICK':
                self.userSymData[sym]['cnt'] += 1
                self.kernelSymData[kernelSym]['cnt'] += 1

            # periodic event such as cpu tick #
            elif event == 'CUSTOM':
                if eventCnt > 0:
                    self.userSymData[sym]['customTotal'] += 1
                    self.kernelSymData[kernelSym]['customTotal'] += 1

                self.userSymData[sym]['customCnt'] += eventCnt
                self.kernelSymData[kernelSym]['customCnt'] += eventCnt

            # etc event #
            elif event is 'IGNORE':
                try:
                    self.ignoreTable[arg]['cnt'] += 1
                except:
                    self.ignoreTable[arg] = {'cnt': int(1)}

            else:
                SystemManager.printWarning("Fail to recognize event %s" % event)

        # Print summary about ignored events #
        self.printIgnoreEvents()



    def printIgnoreEvents(self):
        for idx, value in self.ignoreTable.items():
            SystemManager.printWarning("Ignore %s event %d times" % (idx, value['cnt']))



    def getSymbols(self):
        binPath = ''
        offsetList = []
        curIdx = 0
        lastIdx = len(self.posData)

        # Set alarm handler to handle hanged addr2line #
        signal.signal(signal.SIGALRM, SystemManager.timerHandler)

        # Get symbols and source pos #
        for idx, value in sorted(self.posData.items(), key=lambda e: e[1]['binary'], reverse=True):
            curIdx += 1
            SystemManager.printProgress(curIdx, lastIdx)

            if value['binary'] == '':
                # user pos without offset #
                if value['symbol'] == '' or value['symbol'] == '??':
                    # toDo: find binary and symbol of pos #
                    value['binary'] = '??'
                    value['origBin'] = '??'
                    value['symbol'] = idx
                continue

            # Handle thumbcode #
            if idx == '00c0ffee':
                value['binary'] = '??'
                value['origBin'] = '??'
                value['symbol'] = 'ThumbCode'
                continue

            # Get symbols from address list of previous binary #
            if binPath != value['binary']:
                if binPath != '':
                    # Get symbols #
                    self.getSymbolInfo(binPath, offsetList)
                    offsetList = []

                if value['offset'] == hex(0):
                    offsetList.append(idx)
                else:
                    offsetList.append(value['offset'])

                # Set new binPath to find symbol from address #
                binPath = value['binary']
            # add address to offsetList #
            else:
                # not relocatable binary #
                if value['offset'] == hex(0):
                    offsetList.append(idx)
                # relocatable binary #
                else:
                    offsetList.append(value['offset'])

        # Get symbols and source path from last binary #
        if binPath != '':
            self.getSymbolInfo(binPath, offsetList)



    def getSymbolInfo(self, binPath, offsetList):
        try:
            import subprocess
        except ImportError:
            err = sys.exc_info()[1]
            SystemManager.printError("Fail to import package: " + err.args[0])
            sys.exit(0)

        # Recognize binary type #
        relocated = SystemManager.isRelocatableFile(binPath)

        # No file exist #
        if os.path.isfile(binPath) == False:
            SystemManager.printWarning("Fail to find %s" % binPath)

            for addr in offsetList:
                try:
                    if relocated is False:
                        self.posData[addr]['symbol'] = 'NoFile'
                        self.posData[addr]['src'] = 'NoFile'
                    else:
                        for idx, value in sorted(self.posData.items(), key=lambda e: e[1]['binary'], reverse=True):
                            if value['binary'] == binPath and value['offset'] == hex(int(addr, 16)):
                                self.posData[idx]['symbol'] = 'NoFile'
                                self.posData[idx]['src'] = 'NoFile'
                                break
                except:
                    SystemManager.printWarning("Fail to find address %s" % addr)
            return

        # Check addr2line path #
        if SystemManager.addr2linePath is None:
            SystemManager.printError(\
                "Fail to find addr2line, use also -l option with addr2line path for user mode")
            sys.exit(0)
        else:
            for path in SystemManager.addr2linePath:
                if os.path.isfile(path) is False:
                    SystemManager.printError(\
                        "Fail to find addr2line, use also -l option with addr2line path for user mode")
                    sys.exit(0)

        for path in SystemManager.addr2linePath:
            # Set addr2line command #
            args = [path, "-C", "-f", "-a", "-e", binPath]

            # Limit line number of arguments to pass becuase of ARG_MAX as $(getconf PAGE_SIZE)*32 = 131072 #
            listLen = len(offsetList)
            maxArgLine = 256
            offset = 0
            timeout = 10

            # Get symbol by address of every maxArgLine elements in list #
            while offset < listLen:
                # Launch addr2line #
                proc = subprocess.Popen(args + offsetList[offset:offset+maxArgLine-1], \
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # Increase offset count in address list #
                offset += maxArgLine

                try:
                    # Set alarm to handle hanged addr2line #
                    signal.alarm(timeout)

                    # Wait for addr2line to finish its job #
                    proc.wait()

                    # Cancel alarm after addr2line respond #
                    signal.alarm(0)
                except:
                    SystemManager.printWarning('No response of addr2line for %s' % binPath)
                    continue

                while True:
                    # Get return of addr2line #
                    addr = proc.stdout.readline().replace('\n', '')[2:]
                    symbol = proc.stdout.readline().replace('\n', '')
                    src = proc.stdout.readline().replace('\n', '')

                    err = proc.stderr.readline().replace('\n', '')
                    if len(err) > 0:
                        SystemManager.printWarning(err[err.find(':') + 2:])

                    if not addr:
                        # End of return #
                        break
                    elif symbol == '??':
                        symbol = addr

                    # Check whether the file is relocatable or not #
                    if relocated is False:
                        try:
                            savedSymbol = self.posData[addr]['symbol']
                        except:
                            continue

                        # Check whether saved symbol found by previous addr2line is right #
                        if savedSymbol == None or savedSymbol == '' or \
                            savedSymbol == addr or savedSymbol[0] == '$':
                            self.posData[addr]['symbol'] = symbol

                            if SystemManager.showAll is True:
                                self.posData[addr]['src'] = src
                            else:
                                fileIdx = src.rfind('/')
                                if fileIdx >= 0:
                                    self.posData[addr]['src'] = src[fileIdx + 1:]
                    else:
                        inBinArea = False

                        for idx, value in sorted(self.posData.items(), \
                            key=lambda e: e[1]['binary'], reverse=True):
                            if value['binary'] == binPath:
                                inBinArea = True

                                if value['offset'] == hex(int(addr, 16)):
                                    savedSymbol = self.posData[idx]['symbol']

                                    if savedSymbol == None or savedSymbol == '' or \
                                        savedSymbol == addr or savedSymbol[0] == '$':
                                        self.posData[idx]['symbol'] = symbol

                                        if SystemManager.showAll is True:
                                            self.posData[idx]['src'] = src
                                        else:
                                            fileIdx = src.rfind('/')
                                            if fileIdx >= 0:
                                                self.posData[idx]['src'] = src[fileIdx + 1:]

                                        break
                            elif inBinArea is True:
                                break



    def initStacks(self):
        self.nowCtx['userLastPos'] = '0'
        self.nowCtx['userCallStack'] = []
        self.nowCtx['kernelLastPos'] = '0'
        self.nowCtx['kernelCallStack'] = []



    def swapEvents(self):
        tempEvent = self.nowCtx['nowEvent']
        self.nowCtx['nowEvent'] = self.nowCtx['savedEvent']
        self.nowCtx['savedEvent'] = tempEvent

        tempCnt = self.nowCtx['nowCnt']
        self.nowCtx['nowCnt'] = self.nowCtx['savedCnt']
        self.nowCtx['savedCnt'] = tempCnt

        tempArg = self.nowCtx['nowArg']
        self.nowCtx['nowArg'] = self.nowCtx['savedArg']
        self.nowCtx['savedArg'] = tempArg



    def saveFullStack(self, kernelPos, kernelStack, userPos, userStack, targetEvent, targetCnt, targetArg):

        self.userCallData.append([userPos, userStack, targetEvent, targetCnt, targetArg])

        self.kernelCallData.append([kernelPos, kernelStack, targetEvent, targetCnt, targetArg])



    def saveEventStack(self, targetEvent, targetCnt, targetArg):
        if targetEvent == 'CPU_TICK':
            self.periodicEventCnt += 1

        elif targetEvent == 'PAGE_ALLOC':
            self.pageAllocEventCnt += 1
            self.pageAllocCnt += targetCnt
            self.pageUsageCnt += targetCnt
            self.posData[self.nowCtx['kernelLastPos']]['pageCnt'] += targetCnt
            self.posData[self.nowCtx['userLastPos']]['pageCnt'] += targetCnt

            pageType = targetArg[0]
            pfn = targetArg[1]
            targetArg = [pageType, pfn]

        elif targetEvent == 'PAGE_FREE':
            self.pageFreeEventCnt += 1
            self.pageFreeCnt += targetCnt

            pageType = targetArg[0]
            pfn = targetArg[1]
            targetArg = [pageType, pfn]

        elif targetEvent == 'BLK_READ':
            self.blockRdEventCnt += 1
            self.blockRdUsageCnt += targetCnt
            self.posData[self.nowCtx['kernelLastPos']]['blockRdCnt'] += targetCnt
            self.posData[self.nowCtx['userLastPos']]['blockRdCnt'] += targetCnt

        elif targetEvent == 'BLK_WRITE':
            self.blockWrEventCnt += 1
            self.blockWrUsageCnt += targetCnt
            self.posData[self.nowCtx['kernelLastPos']]['blockWrCnt'] += targetCnt
            self.posData[self.nowCtx['userLastPos']]['blockWrCnt'] += targetCnt

        elif targetEvent == 'HEAP_EXPAND':
            self.heapExpEventCnt += 1
            self.heapExpSize += targetCnt
            self.posData[self.nowCtx['kernelLastPos']]['heapSize'] += targetCnt
            self.posData[self.nowCtx['userLastPos']]['heapSize'] += targetCnt

        elif targetEvent == 'HEAP_REDUCE':
            self.posData[self.nowCtx['kernelLastPos']]['heapSize'] += targetCnt
            self.posData[self.nowCtx['userLastPos']]['heapSize'] += targetCnt

        elif targetEvent == 'CUSTOM':
            if targetCnt > 0:
                self.customTotal += 1
                self.customCnt += targetCnt

                self.posData[self.nowCtx['kernelLastPos']]['customTotal'] += 1
                self.posData[self.nowCtx['userLastPos']]['customTotal'] += 1

                self.posData[self.nowCtx['kernelLastPos']]['customCnt'] += targetCnt
                self.posData[self.nowCtx['userLastPos']]['customCnt'] += targetCnt

        else:
            pass

        self.saveFullStack(self.nowCtx['kernelLastPos'], self.nowCtx['kernelCallStack'], \
            self.nowCtx['userLastPos'], self.nowCtx['userCallStack'], \
            targetEvent, targetCnt, targetArg)



    def saveCallStack(self):
        # stack of kernel thread #
        if self.nowCtx['prevMode'] != self.nowCtx['curMode'] == 'kernel':
            if len(self.nowCtx['userCallStack']) == 0 and \
                len(self.nowCtx['kernelCallStack']) > 0:
                    # Set userLastPos to None #
                self.nowCtx['userLastPos'] = '0'
                self.nowCtx['userCallStack'].append('0')
            if len(self.nowCtx['kernelCallStack']) == 0 and \
                len(self.nowCtx['userCallStack']) > 0:
                # Set kernelLastPos to None #
                self.nowCtx['kernelLastPos'] = '0'
                self.nowCtx['kernelCallStack'].append('0')

        # complicated situation ;( #
        elif self.nowCtx['prevMode'] == self.nowCtx['curMode']:
            # previous user stack loss or nested interval #
            if self.nowCtx['curMode'] is 'kernel':
                # nested interval #
                if self.nowCtx['nowEvent'] is 'CPU_TICK':
                # Backup kernel stack #
                    self.nowCtx['bakKernelLastPos'] = self.nowCtx['kernelLastPos']
                    self.nowCtx['bakKernelCallStack'] = self.nowCtx['kernelCallStack']

                    # Initialize both stacks #
                    self.initStacks()
                # previous user stack loss #
                else:
                    # Set userLastPos to None #
                    self.nowCtx['userLastPos'] = '0'
                    self.nowCtx['userCallStack'].append('0')
            # nested interval #
            elif self.nowCtx['curMode'] is 'user':
                '''
                CORE/0 EVENT0
                CORE/0 <kernel>
                CORE/0 <user>

                CORE/0 EVENT1
                CORE/0 <kernel>
                    CORE/0 EVENT2
                    CORE/0 <kernel>
                    CORE/0 <user>
                CORE/0 <user>
                '''
                # Swap nowEvent and savedEvent #
                self.swapEvents()

        # Save both stacks of previous event before starting to record new kernel stack #
        if (len(self.nowCtx['userCallStack']) > 0 and self.nowCtx['userLastPos'] != '') and \
            (len(self.nowCtx['kernelCallStack']) > 0 and self.nowCtx['kernelLastPos'] != ''):
                # Remove pc in each stacks #
            del self.nowCtx['kernelCallStack'][0], \
                self.nowCtx['userCallStack'][0]

            # Check whether there is nested event or not #
            if self.nowCtx['nested'] > 0:
                '''
                CORE/0 EVENT0
                CORE/0 <kernel>
                CORE/0 <user>

                CORE/0 EVENT1
                    CORE/0 EVENT2
                    CORE/0 <kernel>
                    CORE/0 <user>
                CORE/0 <kernel>
                CORE/0 <user>
                '''
                targetEvent = self.nowCtx['nestedEvent']
                targetCnt = self.nowCtx['nestedCnt']
                targetArg = self.nowCtx['nestedArg']

                # Swap nowEvent and savedEvent #
                self.swapEvents()
            else:
                targetEvent = self.nowCtx['savedEvent']
                targetCnt = self.nowCtx['savedCnt']
                targetArg = self.nowCtx['savedArg']

            # Save full stack of previous event #
            self.saveEventStack(targetEvent, targetCnt, targetArg)

            # Recover previous kernel stack after handling nested event #
            if self.nowCtx['prevMode'] == self.nowCtx['curMode'] == 'user' and \
                self.nowCtx['bakKernelLastPos'] != '0':
                self.nowCtx['kernelLastPos'] = self.nowCtx['bakKernelLastPos']
                self.nowCtx['kernelCallStack'] = self.nowCtx['bakKernelCallStack']
                self.nowCtx['bakKernelLastPos'] = '0'
                self.nowCtx['bakKernelCallStack'] = []
            else:
                self.nowCtx['kernelLastPos'] = ''
                self.nowCtx['kernelCallStack'] = []

            # Initialize user stack #
            self.nowCtx['userLastPos'] = ''
            self.nowCtx['userCallStack'] = []
            self.nowCtx['nestedEvent'] = ''
            self.nowCtx['nestedCnt'] = 0

        # On stack recording switch #
        self.nowCtx['recStat'] = True



    def savePosData(self, pos, path, offset):
        if self.nowCtx['nested'] > 0:
            targetEvent = self.nowCtx['savedEvent']
        else:
            targetEvent = self.nowCtx['nowEvent']

        # Register pos #
        try:
            self.posData[pos]
            if path is not None and path[0] == '/' and path != self.posData[pos]['origBin']:
                self.duplicatedPos += 1
                '''
                SystemManager.printWarning("duplicated address %s in both '%s' and '%s'" % \
                    (pos, path, self.posData[pos]['origBin']))
                '''
        except:
            self.posData[pos] = dict(self.init_posData)

        # user mode #
        if self.nowCtx['curMode'] is 'user':
            # Set path #
            if path is not None:
                self.posData[pos]['origBin'] = path
                self.posData[pos]['binary'] = SystemManager.rootPath + path
                self.posData[pos]['binary'] = self.posData[pos]['binary'].replace('//', '/')

                # Set offset #
                if offset is not None:
                    if SystemManager.isRelocatableFile(path) is True:
                        self.posData[pos]['offset'] = offset

            # Save pos #
            if len(self.nowCtx['userCallStack']) == 0:
                self.nowCtx['userLastPos'] = pos

                if targetEvent == 'CPU_TICK':
                    self.posData[pos]['posCnt'] += 1

            self.nowCtx['userCallStack'].append(pos)
        # kernel mode #
        elif self.nowCtx['curMode'] is 'kernel':
            # Save pos #
            if len(self.nowCtx['kernelCallStack']) == 0:
                self.nowCtx['kernelLastPos'] = pos

                if targetEvent == 'CPU_TICK':
                    self.posData[pos]['posCnt'] += 1

            self.posData[pos]['symbol'] = path

            self.nowCtx['kernelCallStack'].append(pos)

        # wrong mode #
        else:
            SystemManager.printWarning('wrong current mode %s' % self.nowCtx['curMode'])

        # Increase total call count #
        if self.nowEvent == 'CPU_TICK':
            self.posData[pos]['totalCnt'] += 1



    def allocHeapSeg(self, tid, size):
        try:
            self.heapTable[tid + '-ready']['size'] = size
            self.heapTable[tid + '-ready']['tid'] = tid
            self.threadData[thread]['heapSize'] -= size
            SystemManager.printWarning('Overwrite heap segment of %s(%s) at %s' % \
                (self.threadData[tid]['comm'], tid, SystemManager.dbgEventLine))
        except:
            self.heapTable[tid + '-ready'] = dict(self.init_heapSegData)
            self.heapTable[tid + '-ready']['size'] = size
            self.heapTable[tid + '-ready']['tid'] = tid



    def freeHeapSeg(self, addr):
        try:
            self.heapRedEventCnt += 1
            self.heapRedSize += self.heapTable[addr]['size']

            self.threadData[self.heapTable[addr]['tid']]['heapSize'] -= \
                self.heapTable[addr]['size']

            del self.heapTable[addr]
        except:
            SystemManager.printWarning('Fail to free heap segment %s of %s(%s) at %s' % \
                (addr, self.threadData[tid]['comm'], tid, SystemManager.dbgEventLine))



    def setHeapSegAddr(self, tid, addr):
        try:
            self.heapTable[addr] = dict(self.heapTable[tid + '-ready'])
            del self.heapTable[tid + '-ready']
        except:
            SystemManager.printWarning('Fail to set address of heap segment %s of %s(%s) at %s' % \
                (addr, self.threadData[tid]['comm'], tid, SystemManager.dbgEventLine))



    def parseLogs(self, lines, desc):
        curIdx = 0
        lastIdx = len(lines)

        # make custom event table #
        if SystemManager.customCmd is not None:
            for cmd in SystemManager.customCmd:
                cmd = cmd.split(':')

                if len(cmd) > 1:
                    self.customEventTable[cmd[0]] = cmd[1]
                else:
                    self.customEventTable[cmd[0]] = None

        # start to parse logs #
        for liter in lines:
            curIdx += 1
            SystemManager.logSize += len(liter)
            SystemManager.curLine += 1
            SystemManager.dbgEventLine += 1

            ret = self.parseEventLog(liter, desc)
            SystemManager.printProgress(curIdx, lastIdx)

            # Skip lines before first meaningful event #
            if self.lastCore is None:
                continue

            # Set context of current core #
            self.nowCtx = self.coreCtx[self.lastCore]

            # Save full stack to callData table #
            if ret is True:
                self.saveCallStack()

            # Ignore this log because its not event or stack info related to target thread #
            elif ret is False:
                self.nowCtx['recStat'] = False
                continue

            # Save pos into target stack #
            elif self.nowCtx['recStat'] is True:
                # decode return value #
                (pos, path, offset) = ret

                self.savePosData(pos, path, offset)

        # Save stack of last events per core #
        for idx in self.coreCtx.keys():
            self.lastCore = idx
            self.nowCtx = self.coreCtx[idx]

            # Recover previous mode #
            if SystemManager.userEnable is True:
                self.nowCtx['prevMode'] = 'user'
            self.nowCtx['curMode'] = 'kernel'

            self.saveEventParam('IGNORE', 0, 0)
            self.nowCtx['nested'] -= 1
            self.saveCallStack()

        if self.duplicatedPos > 0:
            SystemManager.printWarning("Found %d addresses duplicated" % self.duplicatedPos)



    def getCustomEventValue(self, func, args, cond):
        if cond is None:
            return 1

        # set condition #
        if cond.find('>') >= 0:
            condVal = cond[cond.find('>') + 1:]
            condOp = '>'
            condStr = cond[:cond.find('>')]
        elif cond.find('<') >= 0:
            condVal = cond[cond.find('<') + 1:]
            condOp = '<'
            condStr = cond[:cond.find('<')]
        elif cond.find('==') >= 0:
            condVal = cond[cond.find('==') + 2:]
            condOp = '=='
            condStr = cond[:cond.find('==')]
        else:
            condStr = cond
            condOp = None
            condVal = None

        m = re.match(r'^.+%s=(?P<value>\S+)' % condStr, args)
        if m is not None:
            d = m.groupdict()

            value = d['value']

            if condOp is None and value is not None:
                try:
                    return int(value)
                except:
                    return 0
            elif condOp is '>':
                try:
                    if int(value) > int(condVal):
                        return int(value)
                except:
                    pass

                return 0
            elif condOp is '<':
                try:
                    if int(value) < int(condVal):
                        return int(value)
                except:
                    pass

                return 0
            elif condOp is '==':
                if value == condVal:
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            return 0



    def saveEventParam(self, event, count, arg):
        self.nowCtx['nestedEvent'] = self.nowCtx['savedEvent']
        self.nowCtx['savedEvent'] = self.nowCtx['nowEvent']
        self.nowCtx['nowEvent'] = event

        self.nowCtx['nestedCnt'] = self.nowCtx['savedCnt']
        self.nowCtx['savedCnt'] = self.nowCtx['nowCnt']
        self.nowCtx['nowCnt'] = count

        self.nowCtx['nestedArg'] = self.nowCtx['savedArg']
        self.nowCtx['savedArg'] = self.nowCtx['nowArg']
        self.nowCtx['nowArg'] = arg

        self.nowCtx['nested'] += 1

        if self.nowCtx['nested'] > 2:
            #self.printDbgInfo()
            SystemManager.printError(\
                "Fail to analyze because of corrupted data (over) at %s" % SystemManager.dbgEventLine)
            sys.exit(0)


    def printDbgInfo(self):
        data = self.nowCtx

        print('[%s]' % self.lastCore, \
            '(now) %s/%s/%s' %(data['nowEvent'], data['nowCnt'], data['nowArg']), \
            '(saved) %s/%s/%s' %(data['savedEvent'], data['savedCnt'], data['savedArg']), \
            '(nested) %s/%s/%s' %(data['nestedEvent'], data['nestedCnt'], data['nestedArg']), \
            '(user) %s/%s' % (data['userLastPos'], len(data['userCallStack'])), \
            '(kernel) %s/%s' % (data['kernelLastPos'], len(data['kernelCallStack'])), \
            '(backup) %s/%s' % (data['bakKernelLastPos'], len(data['bakKernelCallStack'])), \
            'at %s' % SystemManager.dbgEventLine)



    def parseEventInfo(self, tid, func, args):
        # cpu tick event #
        # toDo: find shorter periodic event for sampling #
        if func == "hrtimer_start:" and args.rfind('tick_sched_timer') > -1:
            self.cpuEnabled = True

            self.saveEventParam('CPU_TICK', 1, 0)

            return False

        # memory allocation event #
        elif func == "mm_page_alloc:":
            m = re.match(r'^\s*page=\s*(?P<page>\S+)\s+pfn=(?P<pfn>[0-9]+)\s+order=(?P<order>[0-9]+)\s+' + \
                r'migratetype=(?P<mt>[0-9]+)\s+gfp_flags=(?P<flags>\S+)', args)
            if m is not None:
                d = m.groupdict()

                # check whether it is huge page #
                if d['page'] == '(null)':
                    page = 'huge'
                else:
                    page = d['page']

                pfn = int(d['pfn'])
                flags = d['flags']
                pageCnt = pow(2, int(d['order']))

                # Increase page count of thread #
                self.threadData[tid]['nrPages'] += pageCnt

                # Increase page counts of thread #
                pageType = None
                if flags.find('NOFS') >= 0 or flags.find('GFP_WRITE') >= 0 or flags.find('0x1000000') >= 0:
                    pageType = 'CACHE'
                    self.threadData[tid]['cachePages'] += pageCnt
                elif flags.find('USER') >= 0:
                    pageType = 'USER'
                    self.threadData[tid]['userPages'] += pageCnt
                else:
                    pageType = 'KERNEL'
                    self.threadData[tid]['kernelPages'] += pageCnt

                # Make PTE in page table #
                for cnt in range(0, pageCnt):
                    pfnv = pfn + cnt

                    try:
                        '''
                        Decrease page count of it's owner \
                        becuase this page was already allocated but no free log
                        '''

                        ownerTid = self.pageTable[pfnv]['tid']
                        self.threadData[ownerTid]['nrPages'] -= 1

                        origPageType = self.pageTable[pfnv]['type']
                        if origPageType == 'USER':
                            self.threadData[ownerTid]['userPages'] -= 1
                        elif origPageType == 'CACHE':
                            self.threadData[ownerTid]['cachePages'] -= 1
                        elif origPageType == 'KERNEL':
                            self.threadData[ownerTid]['kernelPages'] -= 1
                    except:
                        self.pageTable[pfnv] = dict(self.init_pageData)

                    self.pageTable[pfnv]['tid'] = tid 
                    self.pageTable[pfnv]['page'] = page
                    self.pageTable[pfnv]['flags'] = flags
                    self.pageTable[pfnv]['type'] = pageType
                    self.pageTable[pfnv]['time'] = time

                self.memEnabled = True

                self.saveEventParam('PAGE_ALLOC', pageCnt, [pageType, pfn])
            else:
                self.saveEventParam('IGNORE', 0, func[:-1])

                SystemManager.printWarning("Fail to recognize event %s at %d" % \
                        (func[:-1], SystemManager.dbgEventLine))

            return False

        # memory free event #
        elif func == "mm_page_free:":
            m = re.match(r'^\s*page=(?P<page>\S+)\s+pfn=(?P<pfn>[0-9]+)\s+' + \
                r'order=(?P<order>[0-9]+)', args)
            if m is not None:
                d = m.groupdict()

                page = d['page']
                pfn = int(d['pfn'])
                pageCnt = pow(2, int(d['order']))

                # Update page table #
                origPageType = None
                for cnt in range(0, pageCnt):
                    pfnv = pfn + cnt

                    try:
                        origPageType = self.pageTable[pfnv]['type']
                        self.threadData[self.pageTable[pfnv]['tid']]['nrPages'] -= 1

                        if origPageType is 'CACHE':
                            self.threadData[self.pageTable[pfnv]['tid']]['cachePages'] -= 1
                        elif origPageType is 'USER':
                            self.threadData[self.pageTable[pfnv]['tid']]['userPages'] -= 1
                        elif origPageType is 'KERNEL':
                            self.threadData[self.pageTable[pfnv]['tid']]['kernelPages'] -= 1

                        del self.pageTable[pfnv]
                        self.pageTable[pfnv] = None
                    except:
                        # this page was allocated before starting profile #

                        self.threadData[tid]['nrUnknownFreePages'] += 1
                        continue

                self.memEnabled = True

                self.saveEventParam('PAGE_FREE', pageCnt, [origPageType, pfn])

                return False

            SystemManager.printWarning("Fail to recognize event %s at %d" % \
                    (func[:-1], SystemManager.dbgEventLine))

            self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        # heap increase start event #
        elif func == "sys_enter:":
            m = re.match(r'^\s*NR (?P<nr>[0-9]+) (?P<args>.+)', args)
            if m is not None:
                b = m.groupdict()

                if int(b['nr']) == ConfigManager.sysList.index('sys_brk') or \
                    int(b['nr']) == ConfigManager.getMmapId():
                    self.heapEnabled = True

                    try:
                        size = int(b['args'].split(',')[1], 16)

                        # just brk call to check data segment address #
                        if size == 0:
                            pass

                        self.threadData[tid]['heapSize'] += size
                    except:
                        self.saveEventParam('IGNORE', 0, func[:-1])

                        return False

                    # make heap segment tid-ready #
                    self.allocHeapSeg(tid, size)

                    self.saveEventParam('IGNORE', 0, func[:-1])

                    return False

                elif int(b['nr']) == ConfigManager.sysList.index('sys_munmap'):
                    self.heapEnabled = True

                    try:
                        addr = int(b['args'][1:].split(',')[0], 16)
                        size = self.heapTable[addr]['size']

                        # remove heap segment #
                        self.freeHeapSeg(addr)

                        self.saveEventParam('HEAP_REDUCE', size, addr)

                        return False
                    except:
                        pass

                else:
                    SystemManager.printWarning("Fail to recognize event %s at %d" % \
                            (func[:-1], SystemManager.dbgEventLine))

            self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        # heap increase return event #
        elif func == "sys_exit:":
            m = re.match(r'^\s*NR (?P<nr>[0-9]+) = (?P<ret>.+)', args)
            if m is not None:
                b = m.groupdict()

                if int(b['nr']) == ConfigManager.sysList.index('sys_brk') or \
                    int(b['nr']) == ConfigManager.getMmapId():
                    self.heapEnabled = True

                    addr = int(b['ret'])

                    # rename heap segment from tid-ready to addr #
                    self.setHeapSegAddr(tid, addr)

                    try:
                        size = self.heapTable[addr]['size']

                        self.saveEventParam('HEAP_EXPAND', size, addr)

                        return False
                    except:
                        pass

            SystemManager.printWarning("Fail to recognize event %s at %d" % \
                    (func[:-1], SystemManager.dbgEventLine))

            self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        # block read request event #
        elif func == "block_bio_remap:":
            m = re.match(r'^\s*(?P<major>[0-9]+),(?P<minor>[0-9]+)\s*(?P<operation>\S+)\s*' + \
                r'(?P<address>\S+)\s+\+\s+(?P<size>[0-9]+)', args)
            if m is not None:
                b = m.groupdict()

                if b['operation'][0] == 'R':
                    self.breadEnabled = True

                    blockRdCnt = int(b['size'])
                    self.threadData[tid]['nrRdBlocks'] += blockRdCnt

                    self.saveEventParam('BLK_READ', blockRdCnt, 0)

                    return False

            SystemManager.printWarning("Fail to recognize event %s at %d" % \
                    (func[:-1], SystemManager.dbgEventLine))

            self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        # block write request event #
        elif func == "writeback_dirty_page:":
            m = re.match(r'^\s*bdi\s+(?P<major>[0-9]+):(?P<minor>[0-9]+):\s*' + \
                r'ino=(?P<ino>\S+)\s+index=(?P<index>\S+)', args)
            if m is not None:
                b = m.groupdict()
                self.bwriteEnabled = True

                self.threadData[tid]['nrWrBlocks'] += 1

                self.saveEventParam('BLK_WRITE', 1, 0)

                return False

            self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        # block write request event #
        elif func == "wbc_writepage:":
            m = re.match(r'^\s*bdi\s+(?P<major>[0-9]+):(?P<minor>[0-9]+):\s*' + \
                r'towrt=(?P<towrt>\S+)\s+skip=(?P<skip>\S+)', args)
            if m is not None:
                d = m.groupdict()

                if d['skip'] == '0':
                    self.bwriteEnabled = True

                    self.threadData[tid]['nrWrBlocks'] += 1

                    self.saveEventParam('BLK_WRITE', 1, 0)

                    return False

            self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        # segmentation fault generation event #
        elif func == "signal_generate:":
            m = re.match(r'^\s*sig=(?P<sig>[0-9]+) errno=(?P<err>[0-9]+) ' + \
                r'code=(?P<code>.*) comm=(?P<comm>.*) pid=(?P<pid>[0-9]+)', args)
            if m is not None:
                b = m.groupdict()

                if b['sig'] == str(ConfigManager.sigList.index('SIGSEGV')):
                    self.sigEnabled = True

                    self.saveEventParam('SIGSEGV_GEN', 0, 0)

                    return False

            SystemManager.printWarning("Fail to recognize event %s at %d" % \
                    (func[:-1], SystemManager.dbgEventLine))

            self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        elif func == "signal_deliver:":
            m = re.match(r'^\s*sig=(?P<sig>[0-9]+) errno=(?P<err>[0-9]+) code=(?P<code>.*) ' + \
                r'sa_handler=(?P<handler>.*) sa_flags=(?P<flags>.*)', args)
            if m is not None:
                b = m.groupdict()

                if b['sig'] == str(ConfigManager.sigList.index('SIGSEGV')):
                    self.sigEnabled = True

                    self.saveEventParam('SIGSEGV_DLV', 0, 0)
                else:
                    self.saveEventParam('IGNORE', 0, func[:-1])
            else:
                self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        # Start to record user stack #
        elif func == "<user":
            self.nowCtx['prevMode'] = self.nowCtx['curMode']
            self.nowCtx['curMode'] = 'user'

            return True

        # Start to record kernel stack #
        elif func == "<stack":
            self.nowCtx['prevMode'] = self.nowCtx['curMode']
            self.nowCtx['curMode'] = 'kernel'
            self.nowCtx['nested'] -= 1

            if self.nowCtx['nested'] < 0:
                #self.printDbgInfo()
                SystemManager.printError(\
                    "Fail to analyze data because of corrupted data (under) at %s" % \
                    SystemManager.dbgEventLine)
                sys.exit(0)

            return True

        # custom event #
        elif self.customEventTable != {}:
            try:
                cond = self.customEventTable[func[:-1]]

                customCnt = self.getCustomEventValue(func, args, cond)

                if customCnt > 0:
                    self.threadData[tid]['customTotal'] += customCnt

                self.saveEventParam('CUSTOM', customCnt, func[:-1])
            except:
                self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        # Ignore event #
        else:
            self.saveEventParam('IGNORE', 0, func[:-1])

            return False



    def parseEventLog(self, string, desc):
        # Filter for event #
        if SystemManager.tgidEnable is True:
            m = re.match(r'^\s*(?P<comm>.+)-(?P<thread>[0-9]+)\s+\(\s*(?P<tgid>\S+)\)\s+' + \
                r'\[(?P<core>[0-9]+)\]\s+(?P<time>\S+):\s+(?P<func>\S+)(?P<etc>.+)', string)
        else:
            m = re.match(r'^\s*(?P<comm>.+)-(?P<thread>[0-9]+)\s+\[(?P<core>[0-9]+)\]\s+' + \
                r'(?P<time>\S+):\s+(?P<func>\S+)(?P<etc>.+)', string)

        if m is not None:
            d = m.groupdict()

            # Set time #
            if self.startTime == '0':
                self.startTime = d['time']
            else:
                self.finishTime = d['time']

            # Make thread entity #
            thread = d['thread']
            try:
                self.threadData[thread]['comm'] = d['comm']
            except:
                self.threadData[thread] = dict(self.init_threadData)
                self.threadData[thread]['comm'] = d['comm']

            # increase event count #
            self.threadData[thread]['eventCnt'] += 1

            # set current core #
            self.lastCore = d['core']

            # Make core entity #
            try:
                self.coreCtx[self.lastCore]
            except:
                self.coreCtx[self.lastCore] = dict(self.init_ctxData)
                self.coreCtx[self.lastCore]['userCallStack'] = []
                self.coreCtx[self.lastCore]['kernelCallStack'] = []
                self.coreCtx[self.lastCore]['bakKernelCallStack'] = []

            # set context of current core #
            self.nowCtx = self.coreCtx[self.lastCore]

            # Calculate a total of cpu usage #
            if d['func'] == "hrtimer_start:" and d['etc'].rfind('tick_sched_timer') > -1:
                self.totalTick += 1
                self.threadData[thread]['cpuTick'] += 1

                # Set global interval #
                if self.nowCtx['prevTid'] is not None:
                    diff = float(d['time']) - float(self.nowCtx['prevTime'])
                    self.periodicEventInterval += diff
                    self.periodicContEventCnt += 1

                self.nowCtx['prevTid'] = thread
                self.nowCtx['prevTime'] = d['time']

                # Set max core to calculate cpu usage of thread #
                if SystemManager.maxCore < int(d['core']):
                    SystemManager.maxCore = int(d['core'])

            # Mark die flag of thread that is not able to be profiled #
            elif d['func'] == "sched_process_exit:":
                m = re.match(r'^\s*comm=(?P<comm>.*)\s+pid=(?P<pid>[0-9]+)', d['etc'])
                if m is not None:
                    p = m.groupdict()

                    pid = p['pid']

                    try:
                        self.threadData[pid]
                    except:
                        self.threadData[pid] = dict(self.init_threadData)
                        self.threadData[pid]['comm'] = p['comm']

                    self.threadData[pid]['die'] = True

            # Make thread name #
            elif d['func'] == "task_newtask:":
                m = re.match(r'^\s*pid=(?P<pid>[0-9]+)\s+comm=(?P<comm>\S+)', d['etc'])
                if m is not None:
                    p = m.groupdict()

                    pid = p['pid']

                    try:
                        self.threadData[pid]
                    except:
                        self.threadData[pid] = dict(self.init_threadData)
                        self.threadData[pid]['comm'] = p['comm']

                    self.threadData[pid]['new'] = True

            # Save tgid(pid) #
            if SystemManager.tgidEnable is True:
                self.threadData[thread]['tgid'] = d['tgid']

            # tid filter #
            found = False
            for val in desc:
                if val == d['thread'] or val == '':
                    self.threadData[thread]['target'] = True
                    found = True
                    break
            if found is False:
                return False

            return self.parseEventInfo(thread, d['func'], d['etc'])

        # Parse call stack #
        else:
            pos = string.find('=>  <')
            m = re.match(r' => (?P<path>.+)\[\+0x(?P<offset>.\S*)\] \<(?P<pos>.\S+)\>', string)

            # exist path, offset, pos #
            if m is not None:
                d = m.groupdict()
                return (d['pos'], d['path'], hex(int(d['offset'], 16)))

            # exist only pos #
            elif pos > -1:
                return (string[pos+5:len(string)-2], None, None)

            # exist nothing #
            elif string.find('??') > -1:
                return ('0', None, None)

            else:
                m = re.match(r' => (?P<symbol>.+) \<(?P<pos>.\S+)\>', string)

                # exist symbol, pos #
                if m is not None:
                    d = m.groupdict()
                    return (d['pos'], d['symbol'], None)

                # garbage log #
                else:
                    return False



    def parseMapLine(self, string):
        m = re.match(r'^(?P<startAddr>.\S+)-(?P<endAddr>.\S+) (?P<permission>.\S+) ' + \
            r'(?P<offset>.\S+) (?P<devid>.\S+) (?P<inode>.\S+)\s*(?P<binName>.\S+)', string)
        if m is not None:
            d = m.groupdict()
            self.mapData.append(\
                {'startAddr': d['startAddr'], 'endAddr': d['endAddr'], 'binName': d['binName']})



    def getBinInfo(self, addr):
        if SystemManager.rootPath is None:
            SystemManager.printError(\
                "Fail to recognize sysroot path for target, use also -r option with it for user mode or blank")
            sys.exit(0)

        for data in self.mapData:
            if int(data['startAddr'], 16) <= int(addr, 16) and \
                int(data['endAddr'], 16) >= int(addr, 16):
                if SystemManager.isRelocatableFile(data['binName']) is True:
                        # Return full path and offset about address in mapping table
                    return SystemManager.rootPath + data['binName'], \
                        hex(int(addr, 16) - int(data['startAddr'], 16))
                else:
                    return SystemManager.rootPath + data['binName'], \
                        hex(int(addr, 16))
        SystemManager.printWarning("Fail to get the binary info of %s in mapping table" % addr)



    def printUsage(self):
        targetCnt = 0
        self.totalTime = float(self.finishTime) - float(self.startTime)

        # Print title #
        SystemManager.printTitle()

        # print system information #
        SystemManager.printInfoBuffer()

        # Print profiled thread list #
        SystemManager.pipePrint(\
            "[%s] [ %s: %0.3f ] [ Threads: %d ] [ LogSize: %d KB ] [ Keys: Foward/Back/Save/Quit ]" % \
            ('Function Thread Info', 'Elapsed time', round(self.totalTime, 7), \
             len(self.threadData), SystemManager.logSize / 1024))
        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint(\
            ("{0:_^16}|{1:_^7}|{2:_^7}|{3:_^10}|{4:_^7}|" + \
            "{5:_^7}({6:_^7}/{7:_^7}/{8:_^7})|{9:_^7}|{10:_^8}|" + \
            "{11:_^8}|{12:_^8}|{13:_^8}|{14:_^5}|{15:_^5}|").\
            format("Name", "Tid", "Pid", "Target", "CPU", \
            "MEM", "USER", "BUF", "KERN", "UFREE", "HEAP", \
            "BLK_RD", "BLK_WR", "CUSTOM", "DIE", "NEW"))
        SystemManager.pipePrint(twoLine)

        # set sort value #
        if SystemManager.sort == 'm':
            sortedThreadData = sorted(self.threadData.items(), \
                key=lambda e: e[1]['nrPages'], reverse=True)
        elif SystemManager.sort == 'b':
            sortedThreadData = sorted(self.threadData.items(), \
                key=lambda e: e[1]['nrRdBlocks'], reverse=True)
        else:
            # set cpu usage as default #
            sortedThreadData = sorted(self.threadData.items(), \
                key=lambda e: e[1]['cpuTick'], reverse=True)

        for idx, value in sortedThreadData:
            targetMark = ''
            dieMark = ''
            newMark = ''

            # skip no event count thread #
            if value['eventCnt'] == 0:
                continue

            # check target thread #
            if value['target'] is True:
                targetCnt += 1
                if targetCnt == 2:
                    SystemManager.printWarning("Multiple target threads are selected")
                targetMark = '*'

            # get cpu usage #
            if self.totalTick > 0:
                cpuPer = float(value['cpuTick']) / float(self.totalTick) * 100
            else:
                cpuPer = 0

            # set break condition #
            if SystemManager.sort == 'm':
                breakCond = value['nrPages']
            elif SystemManager.sort == 'b':
                breakCond = value['nrRdBlocks']
            else:
                breakCond = cpuPer

            if breakCond < 1 and SystemManager.showAll is False:
                pass

            if value['die'] is True:
                dieMark = 'v'

            if value['new'] is True:
                newMark = 'v'

            SystemManager.pipePrint(\
                ("{0:16}|{1:^7}|{2:^7}|{3:^10}|{4:6.1f}%|" + \
                "{5:6}k({6:6}k/{7:6}k/{8:6}k)|{9:6}k|{10:7}k|" + \
                "{11:7}k|{12:7}k|{13:8}|{14:^5}|{15:^5}|").\
                format(value['comm'], idx, value['tgid'], targetMark, cpuPer, \
                value['nrPages'] * 4, value['userPages'] * 4, value['cachePages'] * 4, \
                value['kernelPages'] * 4, value['nrUnknownFreePages'] * 4, value['heapSize'] / 1024, \
                int(value['nrRdBlocks'] * 0.5), int(value['nrWrBlocks'] * 4), \
                value['customTotal'], dieMark, newMark))

        SystemManager.pipePrint(oneLine + '\n\n\n')

        # Exit because of no target #
        if len(self.target) == 0:
            SystemManager.printWarning("No specific thread targeted, input tid with -g option")

        # Print resource usage of functions #
        self.printCpuUsage()
        self.printMemUsage()
        self.printHeapUsage()
        self.printBlockRdUsage()
        self.printBlockWrUsage()
        self.printCustomUsage()



    def printCustomUsage(self):
        # no effective custom event #
        if self.customTotal == 0:
            return

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        eventIndex = FunctionAnalyzer.symStackIdxTable.index('CUSTOM')

        # Make custom event list #
        customList = ', '.join(self.customEventTable.keys())

        if SystemManager.userEnable is True:
            # Print custom usage in user space #
            SystemManager.clearPrint()
            SystemManager.pipePrint('[Function %s Info] [Cnt: %d] [Total: %d] (USER)' % \
                (customList, self.customTotal, self.customCnt))

            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
                format("Usage", "Function", "Binary", "Source"))
            SystemManager.pipePrint(twoLine)

            for idx, value in sorted(self.userSymData.items(), key=lambda e: e[1]['customCnt'], reverse=True):
                if value['customCnt'] == 0:
                    break

                SystemManager.pipePrint("{0:7}  |{1:^47}|{2:48}|{3:37}".format(value['customCnt'], idx, \
                    self.posData[value['pos']]['origBin'], self.posData[value['pos']]['src']))

                # Set target stack #
                targetStack = []
                if self.sort is 'sym':
                    targetStack = value['symStack']
                elif self.sort is 'pos':
                    targetStack = value['stack']

                # Sort by usage #
                targetStack.sort(reverse=True)

                # Merge and Print symbols in stack #
                for stack in targetStack:
                    eventCnt = stack[eventIndex]
                    subStack = list(stack[subStackIndex])

                    if eventCnt == 0:
                        break

                    if len(subStack) == 0:
                        continue
                    else:
                        # Make stack info by symbol for print #
                        symbolStack = ''
                        stackIdx = 0
                        indentLen = len("\t" * 4 * 4)
                        appliedIndentLen = indentLen

                        if self.sort is 'sym':
                            for sym in subStack:
                                if sym is None:
                                    symbolSet = ' <- None'
                                else:
                                    symbolSet = ' <- ' + sym + \
                                        ' [' + self.userSymData[sym]['origBin'] + ']'

                                if appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet) > SystemManager.lineLength:
                                    stackIdx = len(symbolStack)
                                    symbolStack += '\n' + ' ' * indentLen
                                    appliedIndentLen = 0

                                symbolStack += symbolSet
                        elif self.sort is 'pos':
                            for pos in subStack:
                                if pos is None:
                                    symbolStack += ' <- None'
                                # No symbol so that just print pos #
                                elif self.posData[pos]['symbol'] == '':
                                    symbolStack += ' <- ' + hex(int(pos, 16)) + \
                                        ' [' + self.posData[pos]['origBin'] + ']'
                                # Print symbol #
                                else:
                                    symbolStack += ' <- ' + self.posData[pos]['symbol'] + \
                                        ' [' + self.posData[pos]['origBin'] + ']'

                    SystemManager.pipePrint("\t\t +{0:7} |{1:32}".format(eventCnt, symbolStack))

                SystemManager.pipePrint(oneLine)

            SystemManager.pipePrint('')

        # Print custom usage in kernel space #
        SystemManager.clearPrint()
        SystemManager.pipePrint('[Function %s Info] [Cnt: %d] [Total: %d] (KERNEL)' % \
            (customList, self.customTotal, self.customCnt))

        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^9}|{1:_^144}".format("Usage", "Function"))
        SystemManager.pipePrint(twoLine)

        # Print custom usage of stacks #
        for idx, value in sorted(self.kernelSymData.items(), key=lambda e: e[1]['customCnt'], reverse=True):
            if value['customCnt'] == 0:
                break

            SystemManager.pipePrint("{0:7}  |{1:^134}".format(value['customCnt'], idx))

            # Sort stacks by usage #
            value['stack'].sort(reverse=True)

            # Print stacks by symbol #
            for stack in value['stack']:
                eventCnt = stack[eventIndex]
                subStack = list(stack[subStackIndex])

                if eventCnt == 0:
                    break

                if len(subStack) == 0:
                    continue
                elif len(subStack) == 1 and SystemManager.showAll is False and \
                    (self.posData[subStack[0]]['symbol'] is None or self.posData[subStack[0]]['symbol'] == 'NoFile'):
                    # Pass unmeaningful part #
                    continue
                else:
                    # Make stack info by symbol for print #
                    symbolStack = ''
                    stackIdx = 0
                    indentLen = len("\t" * 4 * 4)
                    appliedIndentLen = indentLen

                    try:
                        for pos in subStack:
                            if self.posData[pos]['symbol'] == '':
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            else:
                                symbolSet = ' <- ' + str(self.posData[pos]['symbol'])

                            if appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet) > SystemManager.lineLength:
                                stackIdx = len(symbolStack)
                                symbolStack += '\n' + ' ' * indentLen
                                appliedIndentLen = 0

                            symbolStack += symbolSet
                    except:
                        continue

                SystemManager.pipePrint("\t\t +{0:7} |{1:32}".format(eventCnt, symbolStack))

            SystemManager.pipePrint(oneLine)

        SystemManager.pipePrint('\n\n')



    def printCpuUsage(self):
        # no cpu event #
        if self.cpuEnabled is False or self.periodicContEventCnt == 0:
            return

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        cpuTickIndex = FunctionAnalyzer.symStackIdxTable.index('CPU_TICK')

        # average tick interval #
        self.periodicEventInterval /= self.periodicContEventCnt

        if SystemManager.userEnable is True:
            # Print cpu usage in user space #
            SystemManager.clearPrint()
            SystemManager.pipePrint('[Function CPU Info] [Cnt: %d] [Interval: %dms] (USER)' % \
                (self.periodicEventCnt, self.periodicEventInterval * 1000))

            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
                format("Usage", "Function", "Binary", "Source"))
            SystemManager.pipePrint(twoLine)

            for idx, value in sorted(self.userSymData.items(), key=lambda e: e[1]['cnt'], reverse=True):
                if value['cnt'] == 0:
                    break

                cpuPer = round(float(value['cnt']) / float(self.periodicEventCnt) * 100, 1)
                if cpuPer < 1 and SystemManager.showAll is False:
                    break

                SystemManager.pipePrint("{0:7}% |{1:^47}|{2:48}|{3:37}".format(cpuPer, idx, \
                    self.posData[value['pos']]['origBin'], self.posData[value['pos']]['src']))

                # Set target stack #
                targetStack = []
                if self.sort is 'sym':
                    targetStack = value['symStack']
                elif self.sort is 'pos':
                    targetStack = value['stack']

                # Sort by usage #
                targetStack.sort(reverse=True)

                # Merge and Print symbols in stack #
                for stack in targetStack:
                    cpuCnt = stack[cpuTickIndex]
                    subStack = list(stack[subStackIndex])

                    if cpuCnt == 0:
                        break

                    if len(subStack) == 0:
                        continue
                    else:
                        cpuPer = round(float(cpuCnt) / float(value['cnt']) * 100, 1)
                        if cpuPer < 1 and SystemManager.showAll is False:
                            break

                        # Make stack info by symbol for print #
                        symbolStack = ''
                        stackIdx = 0
                        indentLen = len("\t" * 4 * 4)
                        appliedIndentLen = indentLen

                        if self.sort is 'sym':
                            for sym in subStack:
                                if sym is None:
                                    symbolSet = ' <- None'
                                else:
                                    symbolSet = ' <- ' + sym + \
                                        ' [' + self.userSymData[sym]['origBin'] + ']'

                                if appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet) > SystemManager.lineLength:
                                    stackIdx = len(symbolStack)
                                    symbolStack += '\n' + ' ' * indentLen
                                    appliedIndentLen = 0

                                symbolStack += symbolSet
                        elif self.sort is 'pos':
                            for pos in subStack:
                                if pos is None:
                                    symbolStack += ' <- None'
                                # No symbol so that just print pos #
                                elif self.posData[pos]['symbol'] == '':
                                    symbolStack += ' <- ' + hex(int(pos, 16)) + \
                                        ' [' + self.posData[pos]['origBin'] + ']'
                                # Print symbol #
                                else:
                                    symbolStack += ' <- ' + self.posData[pos]['symbol'] + \
                                        ' [' + self.posData[pos]['origBin'] + ']'

                    SystemManager.pipePrint("\t +{0:7}% |{1:32}".format(cpuPer, symbolStack))

                SystemManager.pipePrint(oneLine)

            SystemManager.pipePrint('')

        # Print cpu usage in kernel space #
        SystemManager.clearPrint()
        SystemManager.pipePrint('[Function CPU Info] [Cnt: %d] [Interval: %dms] (KERNEL)' % \
            (self.periodicEventCnt, self.periodicEventInterval * 1000))

        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^9}|{1:_^144}".format("Usage", "Function"))
        SystemManager.pipePrint(twoLine)

        # Make exception list to remove a redundant part of stack #
        exceptList = {}
        if SystemManager.showAll is False:
            for pos, value in self.posData.items():
                if value['symbol'] == '__irq_usr' or \
                    value['symbol'] == '__irq_svc' or \
                    value['symbol'] == '__hrtimer_start_range_ns' or \
                    value['symbol'] == 'hrtimer_start_range_ns' or \
                    value['symbol'] == 'apic_timer_interrupt':
                    try:
                        exceptList[pos]
                    except:
                        exceptList[pos] = dict()

        # Print cpu usage of stacks #
        for idx, value in sorted(self.kernelSymData.items(), key=lambda e: e[1]['cnt'], reverse=True):
            if value['cnt'] == 0:
                break

            cpuPer = round(float(value['cnt']) / float(self.periodicEventCnt) * 100, 1)
            if cpuPer < 1 and SystemManager.showAll is False:
                break

            SystemManager.pipePrint("{0:7}% |{1:^134}".format(cpuPer, idx))

            # Sort stacks by usage #
            value['stack'].sort(reverse=True)

            # Print stacks by symbol #
            for stack in value['stack']:
                cpuCnt = stack[cpuTickIndex]
                subStack = list(stack[subStackIndex])

                if cpuCnt == 0:
                    break
                else:
                    cpuPer = round(float(cpuCnt) / float(value['cnt']) * 100, 1)
                    if cpuPer < 1 and SystemManager.showAll is False:
                        break

                    # Remove a redundant part #
                    for pos, val in exceptList.items():
                        try:
                            del subStack[0:subStack.index(pos)+1]
                        except:
                            continue

                if len(subStack) == 0:
                    continue
                elif len(subStack) == 1 and SystemManager.showAll is False and \
                    (self.posData[subStack[0]]['symbol'] is None or self.posData[subStack[0]]['symbol'] == 'NoFile'):
                    # Pass unmeaningful part #
                    continue
                else:
                    # Make stack info by symbol for print #
                    symbolStack = ''
                    stackIdx = 0
                    indentLen = len("\t" * 4 * 4)
                    appliedIndentLen = indentLen

                    try:
                        for pos in subStack:
                            if self.posData[pos]['symbol'] == '':
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            else:
                                symbolSet = ' <- ' + str(self.posData[pos]['symbol'])

                            if appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet) > SystemManager.lineLength:
                                stackIdx = len(symbolStack)
                                symbolStack += '\n' + ' ' * indentLen
                                appliedIndentLen = 0

                            symbolStack += symbolSet
                    except:
                        continue

                SystemManager.pipePrint("\t +{0:7}% |{1:32}".format(cpuPer, symbolStack))

            SystemManager.pipePrint(oneLine)

        SystemManager.pipePrint('\n\n')



    def printUnknownMemFree(self):
        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        pageFreeIndex = FunctionAnalyzer.symStackIdxTable.index('PAGE_FREE')

        # Print unknown memory free info in user space #
        SystemManager.clearPrint()
        SystemManager.pipePrint('[Function Unknown Memory Free Info] [Size: %dKB] (USER)' % \
            (self.pageUnknownFreeCnt * 4))

        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
            format("Free", "Function", "Binary", "Source"))
        SystemManager.pipePrint(twoLine)

        for idx, value in sorted(self.userSymData.items(), key=lambda e: e[1]['unknownPageFreeCnt'], reverse=True):
            if value['unknownPageFreeCnt'] == 0:
                break

            SystemManager.pipePrint("{0:7}K |{1:^47}|{2:48}|{3:37}".\
                format(int(value['unknownPageFreeCnt'] * 4), idx, \
                self.posData[value['pos']]['origBin'], self.posData[value['pos']]['src']))

            # Set target stack #
            targetStack = []
            if self.sort is 'sym':
                targetStack = value['symStack']
            elif self.sort is 'pos':
                targetStack = value['stack']

            # Sort by usage #
            targetStack = sorted(targetStack, key=lambda x: x[pageFreeIndex], reverse=True)

            # Merge and Print symbols in stack #
            for stack in targetStack:
                pageFreeCnt = stack[pageFreeIndex]
                subStack = list(stack[subStackIndex])

                if pageFreeCnt == 0:
                    break

                if len(subStack) == 0:
                    continue
                else:
                    # Make stack info by symbol for print #
                    symbolStack = ''
                    stackIdx = 0
                    indentLen = len("\t" * 4 * 4)
                    appliedIndentLen = indentLen

                    if self.sort is 'sym':
                        for sym in subStack:
                            if sym is None:
                                symbolSet = ' <- None'
                            else:
                                symbolSet = ' <- ' + sym + \
                                    ' [' + self.userSymData[sym]['origBin'] + ']'

                            if appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet) > SystemManager.lineLength:
                                stackIdx = len(symbolStack)
                                symbolStack += '\n' + ' ' * indentLen
                                appliedIndentLen = 0

                            symbolStack += symbolSet
                    elif self.sort is 'pos':
                        for pos in subStack:
                            if pos is None:
                                symbolStack += ' <- None'
                            # No symbol so that just print pos #
                            elif self.posData[pos]['symbol'] == '':
                                symbolStack += ' <- ' + hex(int(pos, 16)) + \
                                    ' [' + self.posData[pos]['origBin'] + ']'
                            # Print symbol #
                            else:
                                symbolStack += ' <- ' + self.posData[pos]['symbol'] + \
                                    ' [' + self.posData[pos]['origBin'] + ']'

                SystemManager.pipePrint("\t+ {0:7}K |{1:32}".format(int(pageFreeCnt * 4), symbolStack))

            SystemManager.pipePrint(oneLine)

        SystemManager.pipePrint('')

        # Print unknown memory free info in kernel space #
        SystemManager.clearPrint()
        SystemManager.pipePrint('[Function Unknown Memory Free Info] [Size: %dKB] (KERNEL)' % \
            (self.pageUnknownFreeCnt * 4))

        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
            format("FREE", "Function", "Binary", "Source"))
        SystemManager.pipePrint(twoLine)

        # Make exception list to remove a redundant part of stack #
        '''
        exceptList = {}
        for pos, value in self.posData.items():
            if value['symbol'] == 'None':
                try:
                    exceptList[pos]
                except:
                    exceptList[pos] = dict()
        '''

        # Print block write usage of stacks #
        for idx, value in sorted(self.kernelSymData.items(), key=lambda e: e[1]['unknownPageFreeCnt'], reverse=True):
            if value['unknownPageFreeCnt'] == 0:
                break

            SystemManager.pipePrint("{0:7}K |{1:^47}|{2:48}|{3:37}".\
                format(int(value['unknownPageFreeCnt'] * 4), idx, '', ''))

            # Sort stacks by usage #
            value['stack'] = sorted(value['stack'], key=lambda x: x[pageFreeIndex], reverse=True)

            # Print stacks by symbol #
            for stack in value['stack']:
                pageFreeCnt = stack[pageFreeIndex]
                subStack = list(stack[subStackIndex])

                if pageFreeCnt == 0:
                    continue

                if len(subStack) == 0:
                    symbolStack = '\tNone'
                else:
                    # Make stack info by symbol for print #
                    symbolStack = ''
                    stackIdx = 0
                    indentLen = len("\t" * 4 * 4)
                    appliedIndentLen = indentLen

                    try:
                        for pos in subStack:
                            if self.posData[pos]['symbol'] == '':
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            else:
                                symbolSet = ' <- ' + str(self.posData[pos]['symbol'])

                            if appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet) > SystemManager.lineLength:
                                stackIdx = len(symbolStack)
                                symbolStack += '\n' + ' ' * indentLen
                                appliedIndentLen = 0

                            symbolStack += symbolSet
                    except:
                        continue

                SystemManager.pipePrint("\t+ {0:7}K |{1:32}".format(int(pageFreeCnt * 4), symbolStack))

            SystemManager.pipePrint(oneLine)

        SystemManager.pipePrint('\n\n')



    def printMemUsage(self):
        # check memory event #
        if self.memEnabled is False:
            return

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        pageAllocIndex = FunctionAnalyzer.symStackIdxTable.index('PAGE_ALLOC')
        argIndex = FunctionAnalyzer.symStackIdxTable.index('ARGUMENT')

        if SystemManager.userEnable is True:
            # Print mem usage in user space #
            SystemManager.clearPrint()
            SystemManager.pipePrint(\
                '[Function Memory Info] [Total: %dKB] [Alloc: %dKB(%d)] [Free: %dKB(%d)] (USER)' % \
                (self.pageUsageCnt * 4, self.pageAllocCnt * 4, self.pageAllocEventCnt, \
                self.pageFreeCnt * 4, self.pageFreeEventCnt))

            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("{0:^7}({1:^6}/{2:^6}/{3:^6})|{4:_^47}|{5:_^48}|{6:_^27}".\
                format("Usage", "Usr", "Buf", "Ker", "Function", "Binary", "Source"))
            SystemManager.pipePrint(twoLine)

            for idx, value in sorted(self.userSymData.items(), key=lambda e: e[1]['pageCnt'], reverse=True):
                if value['pageCnt'] == 0:
                    break

                SystemManager.pipePrint(\
                    "{0:6}K({1:6}/{2:6}/{3:6})|{4:^47}|{5:48}|{6:27}".format(value['pageCnt'] * 4, \
                    value['userPageCnt'] * 4, value['cachePageCnt'] * 4, value['kernelPageCnt'] * 4, idx, \
                    self.posData[value['pos']]['origBin'], self.posData[value['pos']]['src']))

                # Set target stack #
                targetStack = []
                if self.sort is 'sym':
                    targetStack = value['symStack']
                elif self.sort is 'pos':
                    targetStack = value['stack']

                # Sort by usage #
                targetStack = sorted(targetStack, key=lambda x: x[pageAllocIndex], reverse=True)

                # Merge and Print symbols in stack #
                for stack in targetStack:
                    subStack = list(stack[subStackIndex])
                    pageCnt = stack[pageAllocIndex]
                    userPageCnt = stack[argIndex][0]
                    cachePageCnt = stack[argIndex][1]
                    kernelPageCnt = stack[argIndex][2]

                    if pageCnt == 0:
                        break

                    if len(subStack) == 0:
                        continue
                    else:
                        # Make stack info by symbol for print #
                        symbolStack = ''
                        stackIdx = 0
                        indentLen = len("\t" * 4 * 9)
                        appliedIndentLen = indentLen

                        if self.sort is 'sym':
                            for sym in subStack:
                                if sym is None:
                                    symbolSet = ' <- None'
                                else:
                                    symbolSet = ' <- ' + sym + \
                                        ' [' + self.userSymData[sym]['origBin'] + ']'

                                if appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet) > SystemManager.lineLength:
                                    stackIdx = len(symbolStack)
                                    symbolStack += '\n' + ' ' * indentLen
                                    appliedIndentLen = 0

                                symbolStack += symbolSet
                        elif self.sort is 'pos':
                            for pos in subStack:
                                if pos is None:
                                    symbolStack += ' <- None'
                                # No symbol so that just print pos #
                                elif self.posData[pos]['symbol'] == '':
                                    symbolStack += ' <- ' + hex(int(pos, 16)) + \
                                        ' [' + self.posData[pos]['origBin'] + ']'
                                # Print symbol #
                                else:
                                    symbolStack += ' <- ' + self.posData[pos]['symbol'] + \
                                        ' [' + self.posData[pos]['origBin'] + ']'

                    SystemManager.pipePrint("\t+ {0:6}K({1:6}/{2:6}/{3:6})|{4:32}".format(pageCnt * 4, \
                        userPageCnt * 4, cachePageCnt * 4, kernelPageCnt * 4, symbolStack))

                SystemManager.pipePrint(oneLine)

            SystemManager.pipePrint('')

        # Print mem usage in kernel space #
        SystemManager.clearPrint()
        SystemManager.pipePrint(\
            '[Function Memory Info] [Total: %dKB] [Alloc: %dKB(%d)] [Free: %dKB(%d)] (KERNEL)' % \
            (self.pageUsageCnt * 4, self.pageAllocCnt * 4, self.pageAllocEventCnt, \
            self.pageFreeCnt * 4, self.pageFreeEventCnt))

        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:^7}({1:^6}/{2:^6}/{3:^6})|{4:_^124}".\
            format("Usage", "Usr", "Buf", "Ker", "Function"))
        SystemManager.pipePrint(twoLine)

        # Make exception list to remove a redundant part of stack #
        '''
        exceptList = {}
        for pos, value in self.posData.items():
            if value['symbol'] == 'None':
                try:
                    exceptList[pos]
                except:
                    exceptList[pos] = dict()
        '''

        # Print mem usage of stacks #
        for idx, value in sorted(self.kernelSymData.items(), key=lambda e: e[1]['pageCnt'], reverse=True):
            if value['pageCnt'] == 0:
                break

            SystemManager.pipePrint("{0:6}K({1:6}/{2:6}/{3:6})|{4:^32}".format(value['pageCnt'] * 4, \
                value['userPageCnt'] * 4, value['cachePageCnt'] * 4, value['kernelPageCnt'] * 4, idx))

            # Sort stacks by usage #
            value['stack'] = sorted(value['stack'], key=lambda x: x[pageAllocIndex], reverse=True)

            # Print stacks by symbol #
            for stack in value['stack']:
                subStack = list(stack[subStackIndex])
                pageCnt = stack[pageAllocIndex]
                userPageCnt = stack[argIndex][0]
                cachePageCnt = stack[argIndex][1]
                kernelPageCnt = stack[argIndex][2]

                if pageCnt == 0:
                    continue

                if len(subStack) == 0:
                    continue
                else:
                    # Make stack info by symbol for print #
                    symbolStack = ''
                    stackIdx = 0
                    indentLen = len("\t" * 4 * 9)
                    appliedIndentLen = indentLen

                    try:
                        for pos in subStack:
                            if self.posData[pos]['symbol'] == '':
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            else:
                                symbolSet = ' <- ' + str(self.posData[pos]['symbol'])

                            if appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet) > SystemManager.lineLength:
                                stackIdx = len(symbolStack)
                                symbolStack += '\n' + ' ' * indentLen
                                appliedIndentLen = 0

                            symbolStack += symbolSet
                    except:
                        continue

                SystemManager.pipePrint("\t+ {0:6}K({1:6}/{2:6}/{3:6})|{4:32}".format(pageCnt * 4, \
                    userPageCnt * 4, cachePageCnt * 4, kernelPageCnt * 4, symbolStack))

            SystemManager.pipePrint(oneLine)

        SystemManager.pipePrint('')

        self.printUnknownMemFree()



    def printHeapUsage(self):
        # check heap memory event #
        if self.heapEnabled is False or SystemManager.userEnable is False:
            return

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        heapExpIndex = FunctionAnalyzer.symStackIdxTable.index('HEAP_EXPAND')

        # Print heap usage in user space #
        SystemManager.clearPrint()
        SystemManager.pipePrint(\
            '[Function Heap Info] [Total: %dKB] [Alloc: %dKB(%d)] [Free: %dKB(%d)] (USER)' % \
            ((self.heapExpSize - self.heapRedSize) / 1024, \
            self.heapExpSize / 1024, self.heapExpEventCnt, \
            self.heapRedSize / 1024, self.heapRedEventCnt))

        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
            format("Usage", "Function", "Binary", "Source"))
        SystemManager.pipePrint(twoLine)

        for idx, value in sorted(self.userSymData.items(), key=lambda e: e[1]['heapSize'], reverse=True):
            if value['heapSize'] == 0:
                break

            SystemManager.pipePrint("{0:7}K |{1:^47}|{2:48}|{3:37}".\
                format(int(value['heapSize'] / 1024), idx, \
                self.posData[value['pos']]['origBin'], self.posData[value['pos']]['src']))

            if idx == value['pos']:
                SystemManager.pipePrint(oneLine)
                continue

            # Set target stack #
            targetStack = []
            if self.sort is 'sym':
                targetStack = value['symStack']
            elif self.sort is 'pos':
                targetStack = value['stack']

            # Sort by usage #
            targetStack = sorted(targetStack, key=lambda x: x[heapExpIndex], reverse=True)

            # Merge and Print symbols in stack #
            for stack in targetStack:
                heapSize = stack[heapExpIndex]
                subStack = list(stack[subStackIndex])

                if heapSize == 0:
                    break

                if len(subStack) == 0:
                    continue
                else:
                    # Make stack info by symbol for print #
                    symbolStack = ''
                    stackIdx = 0
                    indentLen = len("\t" * 4 * 4)
                    appliedIndentLen = indentLen

                    if self.sort is 'sym':
                        for sym in subStack:
                            if sym is None:
                                symbolSet = ' <- None'
                            else:
                                symbolSet = ' <- ' + sym + \
                                    ' [' + self.userSymData[sym]['origBin'] + ']'

                            if appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet) > SystemManager.lineLength:
                                stackIdx = len(symbolStack)
                                symbolStack += '\n' + ' ' * indentLen
                                appliedIndentLen = 0

                            symbolStack += symbolSet
                    elif self.sort is 'pos':
                        for pos in subStack:
                            if pos is None:
                                symbolStack += ' <- None'
                            # No symbol so that just print pos #
                            elif self.posData[pos]['symbol'] == '':
                                symbolStack += ' <- ' + hex(int(pos, 16)) + \
                                    ' [' + self.posData[pos]['origBin'] + ']'
                            # Print symbol #
                            else:
                                symbolStack += ' <- ' + self.posData[pos]['symbol'] + \
                                    ' [' + self.posData[pos]['origBin'] + ']'

                SystemManager.pipePrint("\t+ {0:7}K |{1:32}".format(int(heapSize/ 1024), symbolStack))

            SystemManager.pipePrint(oneLine)

        SystemManager.pipePrint('\n\n')



    def printBlockWrUsage(self):
        # no block event #
        if self.bwriteEnabled is False:
            return

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        blkWrIndex = FunctionAnalyzer.symStackIdxTable.index('BLK_WRITE')

        if SystemManager.userEnable is True:
            # Print block write usage in user space #
            SystemManager.clearPrint()
            SystemManager.pipePrint('[Function BLK_WR Info] [Size: %dKB] [Cnt: %d] (USER)' % \
                (self.blockWrUsageCnt * 4, self.blockWrEventCnt))

            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
                format("Usage", "Function", "Binary", "Source"))
            SystemManager.pipePrint(twoLine)

            for idx, value in sorted(self.userSymData.items(), key=lambda e: e[1]['blockWrCnt'], reverse=True):
                if value['blockWrCnt'] == 0:
                    break

                SystemManager.pipePrint("{0:7}K |{1:^47}|{2:48}|{3:37}".\
                    format(int(value['blockWrCnt'] * 4), idx, \
                    self.posData[value['pos']]['origBin'], self.posData[value['pos']]['src']))

                # Set target stack #
                targetStack = []
                if self.sort is 'sym':
                    targetStack = value['symStack']
                elif self.sort is 'pos':
                    targetStack = value['stack']

                # Sort by usage #
                targetStack = sorted(targetStack, key=lambda x: x[blkWrIndex], reverse=True)

                # Merge and Print symbols in stack #
                for stack in targetStack:
                    blockWrCnt = stack[blkWrIndex]
                    subStack = list(stack[subStackIndex])

                    if blockWrCnt == 0:
                        break

                    if len(subStack) == 0:
                        continue
                    else:
                        # Make stack info by symbol for print #
                        symbolStack = ''
                        stackIdx = 0
                        indentLen = len("\t" * 4 * 4)
                        appliedIndentLen = indentLen

                        if self.sort is 'sym':
                            for sym in subStack:
                                if sym is None:
                                    symbolSet = ' <- None'
                                else:
                                    symbolSet = ' <- ' + sym + \
                                        ' [' + self.userSymData[sym]['origBin'] + ']'

                                if appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet) > SystemManager.lineLength:
                                    stackIdx = len(symbolStack)
                                    symbolStack += '\n' + ' ' * indentLen
                                    appliedIndentLen = 0

                                symbolStack += symbolSet
                        elif self.sort is 'pos':
                            for pos in subStack:
                                if pos is None:
                                    symbolStack += ' <- None'
                                # No symbol so that just print pos #
                                elif self.posData[pos]['symbol'] == '':
                                    symbolStack += ' <- ' + hex(int(pos, 16)) + \
                                        ' [' + self.posData[pos]['origBin'] + ']'
                                # Print symbol #
                                else:
                                    symbolStack += ' <- ' + self.posData[pos]['symbol'] + \
                                        ' [' + self.posData[pos]['origBin'] + ']'

                    SystemManager.pipePrint("\t+ {0:7}K |{1:32}".format(int(blockWrCnt * 4), symbolStack))

                SystemManager.pipePrint(oneLine)

            SystemManager.pipePrint('')

        # Print block write usage in kernel space #
        SystemManager.clearPrint()
        SystemManager.pipePrint('[Function BLK_WR Info] [Size: %dKB] [Cnt: %d] (KERNEL)' % \
            (self.blockWrUsageCnt * 4, self.blockWrEventCnt))

        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
            format("Usage", "Function", "Binary", "Source"))
        SystemManager.pipePrint(twoLine)

        # Make exception list to remove a redundant part of stack #
        '''
        exceptList = {}
        for pos, value in self.posData.items():
            if value['symbol'] == 'None':
                try:
                    exceptList[pos]
                except:
                    exceptList[pos] = dict()
        '''

        # Print block write usage of stacks #
        for idx, value in sorted(self.kernelSymData.items(), key=lambda e: e[1]['blockWrCnt'], reverse=True):
            if value['blockWrCnt'] == 0:
                break

            SystemManager.pipePrint("{0:7}K |{1:^47}|{2:48}|{3:37}".\
                format(int(value['blockWrCnt'] * 4), idx, '', ''))

            # Sort stacks by usage #
            value['stack'] = sorted(value['stack'], key=lambda x: x[blkWrIndex], reverse=True)

            # Print stacks by symbol #
            for stack in value['stack']:
                blockWrCnt = stack[blkWrIndex]
                subStack = list(stack[subStackIndex])

                if blockWrCnt == 0:
                    continue

                if len(subStack) == 0:
                    symbolStack = '\tNone'
                else:
                    # Make stack info by symbol for print #
                    symbolStack = ''
                    stackIdx = 0
                    indentLen = len("\t" * 4 * 4)
                    appliedIndentLen = indentLen

                    try:
                        for pos in subStack:
                            if self.posData[pos]['symbol'] == '':
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            else:
                                symbolSet = ' <- ' + str(self.posData[pos]['symbol'])

                            if appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet) > SystemManager.lineLength:
                                stackIdx = len(symbolStack)
                                symbolStack += '\n' + ' ' * indentLen
                                appliedIndentLen = 0

                            symbolStack += symbolSet
                    except:
                        continue

                SystemManager.pipePrint("\t+ {0:7}K |{1:32}".format(int(blockWrCnt * 4), symbolStack))

            SystemManager.pipePrint(oneLine)

        SystemManager.pipePrint('\n\n')



    def printBlockRdUsage(self):
        # no block event #
        if self.breadEnabled is False:
            return

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        blkRdIndex = FunctionAnalyzer.symStackIdxTable.index('BLK_READ')

        if SystemManager.userEnable is True:
            # Print block read usage in user space #
            SystemManager.clearPrint()
            SystemManager.pipePrint('[Function BLK_RD Info] [Size: %dKB] [Cnt: %d] (USER)' % \
                (self.blockRdUsageCnt * 0.5, self.blockRdEventCnt))

            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
                format("Usage", "Function", "Binary", "Source"))
            SystemManager.pipePrint(twoLine)

            for idx, value in sorted(self.userSymData.items(), key=lambda e: e[1]['blockRdCnt'], reverse=True):
                if value['blockRdCnt'] == 0:
                    break

                SystemManager.pipePrint("{0:7}K |{1:^47}|{2:48}|{3:37}".\
                    format(int(value['blockRdCnt'] * 0.5), idx, \
                    self.posData[value['pos']]['origBin'], self.posData[value['pos']]['src']))

                # Set target stack #
                targetStack = []
                if self.sort is 'sym':
                    targetStack = value['symStack']
                elif self.sort is 'pos':
                    targetStack = value['stack']

                # Sort by usage #
                targetStack = sorted(targetStack, key=lambda x: x[blkRdIndex], reverse=True)

                # Merge and Print symbols in stack #
                for stack in targetStack:
                    blockRdCnt = stack[blkRdIndex]
                    subStack = list(stack[subStackIndex])

                    if blockRdCnt == 0:
                        break

                    if len(subStack) == 0:
                        continue
                    else:
                        # Make stack info by symbol for print #
                        symbolStack = ''
                        stackIdx = 0
                        indentLen = len("\t" * 4 * 4)
                        appliedIndentLen = indentLen

                        if self.sort is 'sym':
                            for sym in subStack:
                                if sym is None:
                                    symbolSet = ' <- None'
                                else:
                                    symbolSet = ' <- ' + sym + \
                                        ' [' + self.userSymData[sym]['origBin'] + ']'

                                if appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet) > SystemManager.lineLength:
                                    stackIdx = len(symbolStack)
                                    symbolStack += '\n' + ' ' * indentLen
                                    appliedIndentLen = 0

                                symbolStack += symbolSet
                        elif self.sort is 'pos':
                            for pos in subStack:
                                if pos is None:
                                    symbolStack += ' <- None'
                                # No symbol so that just print pos #
                                elif self.posData[pos]['symbol'] == '':
                                    symbolStack += ' <- ' + hex(int(pos, 16)) + \
                                        ' [' + self.posData[pos]['origBin'] + ']'
                                # Print symbol #
                                else:
                                    symbolStack += ' <- ' + self.posData[pos]['symbol'] + \
                                        ' [' + self.posData[pos]['origBin'] + ']'

                    SystemManager.pipePrint("\t+ {0:7}K |{1:32}".format(int(blockRdCnt * 0.5), symbolStack))

                SystemManager.pipePrint(oneLine)

            SystemManager.pipePrint('')

        # Print block read usage in kernel space #
        SystemManager.clearPrint()
        SystemManager.pipePrint('[Function BLK_RD Info] [Size: %dKB] [Cnt: %d] (KERNEL)' % \
            (self.blockRdUsageCnt * 0.5, self.blockRdEventCnt))

        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
            format("Usage", "Function", "Binary", "Source"))
        SystemManager.pipePrint(twoLine)

        # Make exception list to remove a redundant part of stack #
        '''
        exceptList = {}
        for pos, value in self.posData.items():
            if value['symbol'] == 'None':
                try:
                    exceptList[pos]
                except:
                    exceptList[pos] = dict()
        '''

        # Print block read usage of stacks #
        for idx, value in sorted(self.kernelSymData.items(), key=lambda e: e[1]['blockRdCnt'], reverse=True):
            if value['blockRdCnt'] == 0:
                break

            SystemManager.pipePrint("{0:7}K |{1:^47}|{2:48}|{3:37}".\
                format(int(value['blockRdCnt'] * 0.5), idx, '', ''))

            # Sort stacks by usage #
            value['stack'] = sorted(value['stack'], key=lambda x: x[blkRdIndex], reverse=True)

            # Print stacks by symbol #
            for stack in value['stack']:
                blockRdCnt = stack[blkRdIndex]
                subStack = list(stack[subStackIndex])

                if blockRdCnt == 0:
                    continue

                if len(subStack) == 0:
                    symbolStack = '\tNone'
                else:
                    # Make stack info by symbol for print #
                    symbolStack = ''
                    stackIdx = 0
                    indentLen = len("\t" * 4 * 4)
                    appliedIndentLen = indentLen

                    try:
                        for pos in subStack:
                            if self.posData[pos]['symbol'] == '':
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            else:
                                symbolSet = ' <- ' + str(self.posData[pos]['symbol'])

                            if appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet) > SystemManager.lineLength:
                                stackIdx = len(symbolStack)
                                symbolStack += '\n' + ' ' * indentLen
                                appliedIndentLen = 0

                            symbolStack += symbolSet
                    except:
                        continue

                SystemManager.pipePrint("\t+ {0:7}K |{1:32}".format(int(blockRdCnt * 0.5), symbolStack))

            SystemManager.pipePrint(oneLine)

        SystemManager.pipePrint('\n\n')





class FileAnalyzer(object):
    """ Analyzer for file profiling """

    def __init__(self):
        self.libguider = None
        self.libguiderPath = 'libguider.so'

        self.startTime = None
        self.profSuccessCnt = 0
        self.profFailedCnt = 0
        self.procData = {}
        self.fileData = {}

        self.procList = {}
        self.fileList = {}

        self.intervalProcData = []
        self.intervalFileData = []

        self.init_procData = {'tids': None, 'pageCnt': int(0), 'procMap': None}
        self.init_threadData = {'comm': ''}
        self.init_mapData = {'offset': int(0), 'size': int(0), 'pageCnt': int(0), 'fd': None, \
            'totalSize': int(0), 'fileMap': None}

        try:
            import ctypes
            from ctypes import cdll, POINTER
        except ImportError:
            err = sys.exc_info()[1]
            SystemManager.printError("Fail to import package: " + err.args[0])
            sys.exit(0)

        # handle no target case #
        if len(SystemManager.showGroup) == 0:
            SystemManager.showGroup.insert(0, '')

        try:
            imp.find_module('ctypes')
        except:
            SystemManager.printError('Fail to find ctypes package')
            sys.exit(0)

        try:
            # load the library #
            self.libguider = cdll.LoadLibrary(self.libguiderPath)
        except:
            SystemManager.printError('Fail to open %s, use LD_LIBRARY_PATH if it exist' % self.libguiderPath)
            sys.exit(0)

        # set the argument type #
        self.libguider.get_filePageMap.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        # set the return type #
        self.libguider.get_filePageMap.restype = POINTER(ctypes.c_ubyte)

        try:
            import resource
            SystemManager.maxFd = resource.getrlimit(getattr(resource, 'RLIMIT_NOFILE'))[0]
        except:
            SystemManager.printWarning(\
                "Fail to get maxFd because of no resource package, default %d" % SystemManager.maxFd)

        self.startTime = time.time()

        while True:
            # scan proc directory and save map information of processes #
            self.scanProcs()

            # merge maps of processes into a integrated file map #
            self.mergeFileMapInfo()

            # get file map info on memory #
            self.getFilePageMaps()

            # fill file map of each processes #
            self.fillFileMaps()

            if SystemManager.intervalEnable > 0:
                # save previous file usage and initialize variables #
                self.intervalProcData.append(self.procData)
                self.intervalFileData.append(self.fileData)
                self.procData = {}
                self.fileData = {}
                self.profSuccessCnt = 0
                self.profFailedCnt = 0

                # check exit condition for interval profile #
                if SystemManager.condExit is False:
                    signal.pause()
                else:
                    break
            else:
                break



    def __del__(self):
        pass



    def printUsage(self):
        if len(self.procData) == 0:
            SystemManager.printError('No process profiled')
            sys.exit(0)
        if len(self.fileData) == 0:
            SystemManager.printError('No file profiled')
            sys.exit(0)

        # Print title #
        SystemManager.printTitle()

        # print system information #
        SystemManager.printInfoBuffer()

        # Print proccess list #
        SystemManager.pipePrint(\
            "[%s] [ Process : %d ] [ Keys: Foward/Back/Save/Quit ] [ Capture: Ctrl+| ]" % \
            ('File Process Info', len(self.procData)))
        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^7}|{1:_^10}|{2:_^16}({3:_^7})".\
            format("Pid", "Size(KB)", "ThreadName", "Tid"))
        SystemManager.pipePrint(twoLine)

        for pid, val in sorted(self.procData.items(), key=lambda e: int(e[1]['pageCnt']), reverse=True):
            printMsg = "{0:^7}|{1:9} ".format(pid, val['pageCnt'] * SystemManager.pageSize / 1024)
            for tid, threadVal in sorted(val['tids'].items(), reverse=True):
                printMsg += "|{0:^16}({1:^7})".format(threadVal['comm'], tid)
                SystemManager.pipePrint(printMsg)
                printMsg = "{0:^7}{1:^11}".format('', '')

        SystemManager.pipePrint(oneLine + '\n')

        # Print file list #
        SystemManager.pipePrint("[%s] [ File: %d ] [ Keys: Foward/Back/Save/Quit ]" % \
            ('File Usage Info', len(self.fileData)))
        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^12}|{1:_^10}|{2:_^5}|{3:_^123}|".\
            format("Memory(KB)", "File(KB)", "%", "Path"))
        SystemManager.pipePrint(twoLine)

        for fileName, val in sorted(self.fileData.items(), key=lambda e: int(e[1]['pageCnt']), reverse=True):
            memSize = val['pageCnt'] * SystemManager.pageSize / 1024
            fileSize = ((val['totalSize'] + SystemManager.pageSize - 1) / \
                SystemManager.pageSize) * SystemManager.pageSize / 1024
            per = 0

            if fileSize != 0:
                per = int(int(memSize) / float(fileSize) * 100)

            SystemManager.pipePrint("{0:11} |{1:9} |{2:5}|{3:123}|".\
                format(memSize, fileSize, per, fileName))

        SystemManager.pipePrint(oneLine + '\n\n\n')



    def printIntervalInfo(self):
        # Merge proccess info into a global list #
        for procData in self.intervalProcData:
            for pid, procInfo in procData.items():
                try:
                    if self.procList[pid]['pageCnt'] < procInfo['pageCnt']:
                        self.procList[pid]['pageCnt'] = procInfo['pageCnt']
                except:
                    self.procList[pid] = dict(self.init_procData)
                    self.procList[pid]['tids'] = {}
                    self.procList[pid]['pageCnt'] = procInfo['pageCnt']

                for tid, val in procInfo['tids'].items():
                    try:
                        self.procList[pid]['tids'][tid]
                    except:
                        self.procList[pid]['tids'][tid] = dict(self.init_threadData)
                        self.procList[pid]['tids'][tid]['comm'] = val['comm']

        if len(self.procList) == 0:
            SystemManager.printError('No process profiled')
            sys.exit(0)

        # Merge file info into a global list #
        for fileData in self.intervalFileData:
            for fileName, fileStat in fileData.items():
                try:
                    if self.fileList[fileName]['pageCnt'] < fileStat['pageCnt']:
                        self.fileList[fileName]['pageCnt'] = fileStat['pageCnt']
                except:
                    self.fileList[fileName] = dict(self.init_mapData)
                    self.fileList[fileName]['pageCnt'] = fileStat['pageCnt']
                    self.fileList[fileName]['totalSize'] = fileStat['totalSize']

        if len(self.fileList) == 0:
            SystemManager.printError('No file profiled')
            sys.exit(0)

        # Print title #
        SystemManager.printTitle()

        # print system information #
        SystemManager.printInfoBuffer()

        # Print proccess list #
        SystemManager.pipePrint("[%s] [ Process : %d ] [ Keys: Foward/Back/Save/Quit ]" % \
            ('File Process Info', len(self.procList)))
        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^7}|{1:_^13}|{2:_^16}({3:_^7})".\
            format("Pid", "MaxSize(KB)", "ThreadName", "Tid"))
        SystemManager.pipePrint(twoLine)

        for pid, val in sorted(self.procList.items(), key=lambda e: int(e[1]['pageCnt']), reverse=True):
            printMsg = "{0:^7}|{1:12} ".format(pid, val['pageCnt'] * SystemManager.pageSize / 1024)

            for tid, threadVal in sorted(val['tids'].items(), reverse=True):
                printMsg += "|{0:>16}({1:>7})".format(threadVal['comm'], tid)
                SystemManager.pipePrint(printMsg)
                printMsg = "{0:^7}{1:^14}".format('', '')

        SystemManager.pipePrint(oneLine + '\n')

        # Print file list #
        SystemManager.pipePrint("[%s] [ File: %d ] [ Keys: Foward/Back/Save/Quit ]" % \
            ('File Usage Info', len(self.fileList)))
        SystemManager.pipePrint(twoLine)

        printMsg = "{0:_^13}|{1:_^10}|{2:_^5}|".format("InitMem(KB)", "File(KB)", "%")

        if len(self.intervalFileData) > 1:
            for idx in range(1, len(self.intervalFileData)):
                printMsg += "{0:_^15}|".format(str(idx))

        printMsg += "{0:_^13}|{1:_^5}|{2:_^60}|".format("LastMem(KB)", "%", "Path")

        SystemManager.pipePrint(printMsg)

        SystemManager.pipePrint(twoLine)

        for fileName, val in sorted(self.fileList.items(), key=lambda e: int(e[1]['pageCnt']), reverse=True):
            try:
                memSize = self.intervalFileData[0][fileName]['pageCnt'] * SystemManager.pageSize / 1024
            except:
                memSize = 0
            try:
                fileSize = ((val['totalSize'] + SystemManager.pageSize - 1) / \
                    SystemManager.pageSize) * SystemManager.pageSize / 1024
            except:
                fileSize = 0

            per = 0

            if fileSize != 0:
                per = int(int(memSize) / float(fileSize) * 100)

            printMsg = "{0:12} |{1:9} |{2:5}|".format(memSize, fileSize, per)
            if len(self.intervalFileData) > 1:
                for idx in range(1, len(self.intervalFileData)):
                    diffNew = 0
                    diffDel = 0

                    try:
                        nowFileMap = self.intervalFileData[idx][fileName]['fileMap']
                    except:
                        nowFileMap = None
                    try:
                        prevFileMap = self.intervalFileData[idx - 1][fileName]['fileMap']
                    except:
                        prevFileMap = None

                    if nowFileMap is None:
                        if prevFileMap is not None:
                            diffDel = self.intervalFileData[idx - 1][fileName]['pageCnt']
                    else:
                        if prevFileMap is None:
                            diffNew = self.intervalFileData[idx][fileName]['pageCnt']
                        else:
                            if len(nowFileMap) == len(prevFileMap):
                                for i in range(len(nowFileMap)):
                                    if nowFileMap[i] > prevFileMap[i]:
                                        diffNew += 1
                                    elif nowFileMap[i] < prevFileMap[i]:
                                        diffDel += 1

                    diffNew = diffNew * SystemManager.pageSize / 1024
                    diffDel = diffDel * SystemManager.pageSize / 1024
                    printMsg += "+%6d/-%6d|" % (diffNew, diffDel)

            totalMemSize = val['pageCnt'] * SystemManager.pageSize / 1024

            if fileSize != 0:
                per = int(int(totalMemSize) / float(fileSize) * 100)
            else:
                per = 0
            printMsg += "{0:13}|{1:5}|{2:60}|".format(totalMemSize, per, fileName)

            SystemManager.pipePrint(printMsg)

        SystemManager.pipePrint(oneLine + '\n\n\n')



    def makeReadaheadList(self):
        pass



    def scanProcs(self):
        # get process list in proc directory #
        try:
            pids = os.listdir(SystemManager.procPath)
        except:
            SystemManager.printError('Fail to open %s' % (SystemManager.procPath))
            sys.exit(0)

        # scan comms include words in SystemManager.showGroup #
        for pid in pids:
            try:
                int(pid)
            except:
                continue

            # make path of tid #
            procPath = os.path.join(SystemManager.procPath, pid)
            taskPath = os.path.join(procPath, 'task')

            try:
                tids = os.listdir(taskPath)
            except:
                SystemManager.printWarning('Fail to open %s' % (taskPath))
                continue

            for tid in tids:
                try:
                    int(tid)
                except:
                    continue

                # make path of comm #
                threadPath = os.path.join(taskPath, tid)
                commPath = os.path.join(threadPath, 'comm')

                try:
                    fd = open(commPath, 'r')
                    comm = fd.readline()
                    comm = comm[0:len(comm) - 1]
                    fd.close()
                except:
                    SystemManager.printWarning('Fail to open %s' % (commPath))
                    continue

                # save process info #
                for val in SystemManager.showGroup:
                    if comm.rfind(val) > -1 or tid == val:
                        # access procData #
                        try:
                            self.procData[pid]
                        except:
                            self.procData[pid] = dict(self.init_procData)
                            self.procData[pid]['tids'] = {}
                            self.procData[pid]['procMap'] = {}

                            # make or update mapInfo per process #
                            self.makeProcMapInfo(pid, threadPath + '/maps')

                        # access threadData #
                        try:
                            self.procData[pid]['tids'][tid]
                        except:
                            self.procData[pid]['tids'][tid] = dict(self.init_threadData)
                            self.procData[pid]['tids'][tid]['comm'] = comm



    def fillFileMaps(self):
        for fileName, val in self.fileData.items():
            if val['fileMap'] is not None:
                val['pageCnt'] = val['fileMap'].count(1)

        for pid, val in self.procData.items():
            for fileName, mapInfo in val['procMap'].items():
                if self.fileData[fileName]['fileMap'] is None or mapInfo is None:
                    continue

                # convert address and size to index in mapping table #
                offset = mapInfo['offset'] - self.fileData[fileName]['offset']
                offset = (offset + SystemManager.pageSize - 1) / SystemManager.pageSize
                size = (mapInfo['size'] + SystemManager.pageSize - 1) / SystemManager.pageSize

                mapInfo['fileMap'] = list(self.fileData[fileName]['fileMap'][offset:size])
                mapInfo['pageCnt'] = mapInfo['fileMap'].count(1)
                val['pageCnt'] += mapInfo['pageCnt']



    def makeProcMapInfo(self, pid, path):
        # open maps #
        try:
            fd = open(path, 'r')
        except:
            SystemManager.printWarning('Fail to open %s' % (path))
            return

        # read maps #
        mapBuf = fd.readlines()

        # parse and merge lines in maps #
        for val in mapBuf:
            self.mergeMapLine(val, self.procData[pid]['procMap'])



    def mergeFileMapInfo(self):
        for idx, val in self.procData.items():
            for fileName, scope in val['procMap'].items():
                newOffset = scope['offset']
                newSize = scope['size']
                newEnd = newOffset + newSize

                # access fileData #
                try:
                    savedOffset = self.fileData[fileName]['offset']
                    savedSize = self.fileData[fileName]['size']
                    savedEnd = savedOffset + savedSize

                    # bigger start address then saved one #
                    if savedOffset <= newOffset:
                        # merge bigger end address then saved one #
                        if savedEnd < newEnd:
                            self.fileData[fileName]['size'] += (newEnd - savedOffset - savedSize)
                        # ignore smaller end address then saved one #
                        else:
                            pass
                    # smaller start address then saved one #
                    else:
                        if savedEnd >= newEnd:
                            self.fileData[fileName]['size'] += (savedOffset - newOffset)
                        else:
                            self.fileData[fileName]['size'] = newSize

                        self.fileData[fileName]['offset'] = newOffset
                except:
                    self.fileData[fileName] = dict(self.init_mapData)
                    self.fileData[fileName]['offset'] = newOffset
                    self.fileData[fileName]['size'] = newSize



    def mergeMapLine(self, string, procMap):
        m = re.match(r'^(?P<startAddr>.\S+)-(?P<endAddr>.\S+) (?P<permission>.\S+) ' + \
            r'(?P<offset>.\S+) (?P<devid>.\S+) (?P<inode>.\S+)\s*(?P<binName>.+)', string)
        if m is not None:
            d = m.groupdict()

            fileName = d['binName']
            startAddr = int(d['startAddr'], 16)
            endAddr = int(d['endAddr'], 16)

            newOffset = int(d['offset'], 16)
            newSize = endAddr - startAddr
            newEnd = newOffset + newSize

            try:
                savedOffset = procMap[fileName]['offset']
                savedSize = procMap[fileName]['size']
                savedEnd = savedOffset + savedSize

                # bigger start address then saved one #
                if savedOffset <= newOffset:
                    # merge bigger end address then saved one #
                    if savedEnd < newEnd:
                        procMap[fileName]['size'] += (newEnd - savedOffset - savedSize)
                    # ignore smaller end address then saved one #
                    else:
                        pass
                # smaller start address then saved one #
                else:
                    if savedEnd >= newEnd:
                        procMap[fileName]['size'] += (savedOffset - newOffset)
                    else:
                        procMap[fileName]['size'] = newSize

                    procMap[fileName]['offset'] = newOffset
            except:
                procMap[fileName] = dict(self.init_mapData)
                procMap[fileName]['offset'] = newOffset
                procMap[fileName]['size'] = newSize



    def getFilePageMaps(self):
        self.profSuccessCnt = 0
        self.profFailedCnt = 0

        for fileName, val in self.fileData.items():
            if SystemManager.intervalEnable > 0:
                # use file descriptor already saved as possible #
                try:
                    val['fd'] = \
                        self.intervalFileData[len(self.intervalFileData) - 1][fileName]['fd']
                    val['totalSize'] = \
                        self.intervalFileData[len(self.intervalFileData) - 1][fileName]['totalSize']
                except:
                    pass

            if val['fd'] is None:
                try:
                    # open binary file to check page whether it is on memory or not #
                    fd = open(fileName, "r")
                    size = os.stat(fileName).st_size

                    val['fd'] = fd
                    val['totalSize'] = size
                except:
                    self.profFailedCnt += 1
                    if SystemManager.showAll is True:
                        SystemManager.printWarning('Fail to open %s' % fileName)
                    continue

            # check file size whether it is readable or not #
            if val['totalSize'] <= 0:
                self.profFailedCnt += 1
                if SystemManager.showAll is True:
                    SystemManager.printWarning('Fail to mmap %s' % fileName)
                continue

            # prepare variables for mincore systemcall #
            fd = val['fd'].fileno()
            offset = val['offset']
            size = val['size']

            # call mincore systemcall #
            pagemap = self.libguider.get_filePageMap(fd, offset, size)

            # save the array of ctype into list #
            if pagemap is not None:
                try:
                    val['fileMap'] = \
                        [pagemap[i] for i in range(size / SystemManager.pageSize)]
                    self.profSuccessCnt += 1

                    # fd resource is about to run out #
                    if SystemManager.maxFd - 16 < fd:
                        try:
                            val['fd'].close()
                        except:
                            pass
                        val['fd'] = None
                except:
                    SystemManager.printWarning('Fail to access %s' % fileName)
                    val['fileMap'] = None
                    self.profFailedCnt += 1
            else:
                try:
                    val['fd'].close()
                except:
                    pass
                val['fd'] = None

        if len(self.fileData) > 0:
            SystemManager.printGood('Profiled a total of %d files' % self.profSuccessCnt)
        else:
            SystemManager.printWarning('Profiled a total of %d files' % self.profSuccessCnt)

        if self.profFailedCnt > 0:
            SystemManager.printWarning('Failed to open a total of %d files' % self.profFailedCnt)





class SystemManager(object):
    """ Manager for system setting """

    pageSize = 4096
    blockSize = 512
    bufferSize = '40960'
    ttyRows = '50'
    ttyCols = '156'
    magicString = '@@@@@'
    procPath = '/proc'
    launchBuffer = None
    maxFd = 1024
    lineLength = 154

    #HZ = 250 # 4ms tick #
    TICK = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
    """
    tick value for top profiler
        TICK = int((1 / float(HZ)) * 1000)
    """

    arch = 'arm'
    mountPath = None
    addr2linePath = None
    rootPath = None
    pipeForPrint = None
    fileForPrint = None
    inputFile = None
    outputFile = None
    printFile = None
    optionList = None
    customCmd = None

    tgidEnable = True
    binEnable = False
    processEnable = True

    maxCore = 0
    logSize = 0
    curLine = 0
    totalLine = 0
    dbgEventLine = 0
    uptime = 0
    prevUptime = 0
    uptimeDiff = 0

    graphEnable = False
    graphLabels = []
    procBuffer = []
    procBufferSize = 0
    bufferString = ''
    bufferRows = 0
    systemInfoBuffer = ''
    kerSymTable = {}

    eventLogFile = None
    eventLogFD = None

    showAll = False
    selectMenu = None
    intervalNow = 0
    recordStatus = False
    condExit = False
    sort = None

    statFd = None
    vmstatFd = None
    swapFd = None
    uptimeFd = None

    irqEnable = False
    cpuEnable = True
    memEnable = False
    heapEnable = False
    diskEnable = False
    blockEnable = False
    userEnable = True
    futexEnable = False
    pipeEnable = False
    depEnable = False
    sysEnable = False
    waitEnable = False
    backgroundEnable = False
    resetEnable = False
    warningEnable = False
    intervalEnable = 0

    functionEnable = False
    systemEnable = False
    fileEnable = False
    threadEnable = False

    repeatInterval = 0
    repeatCount = 0
    progressCnt = 0
    progressChar = {
            0: '|',
            1: '/',
            2: '-',
            3: '\\',
    }

    cmdList = {}
    preemptGroup = []
    showGroup = []
    syscallList = []



    def __init__(self):
        self.memInfo = {}
        self.diskInfo = {}
        self.mountInfo = {}
        self.SystemManager = {}

        self.cpuData = None
        self.memBeforeData = None
        self.memAfterData = None
        self.diskBeforeData = None
        self.diskAfterData = None
        self.mountData = None
        self.uptimeData = None
        self.loadData = None
        self.cmdlineData = None
        self.osData = None
        self.devData = None

        self.cpuInfo = dict()
        self.memInfo['before'] = dict()
        self.memInfo['after'] = dict()
        self.diskInfo['before'] = dict()
        self.diskInfo['after'] = dict()
        self.SystemManager = dict()

        SystemManager.eventLogFile = \
            str(self.getMountPath()) + '/tracing/trace_marker'

        # Save storage info first #
        self.saveMemInfo()
        self.saveDiskInfo()



    def __del__(self):
        pass



    @staticmethod
    def setComm():
        if sys.platform == 'linux2':
            try:
                import ctypes
                from ctypes import cdll, POINTER
            except ImportError:
                err = sys.exc_info()[1]
                print("[Warning] Fail to import package: " + err.args[0])

            try:
                libc = cdll.LoadLibrary('libc.so.6')
                libc.prctl(15, __module__, 0, 0, 0)
            except:
                print('[Warning] Fail to set comm becuase of prctl in libc')
        else:
            print('[Warning] Fail to set comm becuase this platform is not linux')



    @staticmethod
    def printOptions():
        if len(sys.argv) <= 1 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
            cmd = sys.argv[0]

            if cmd.find('.pyc') >= 0:
                cmd = cmd[:cmd.find('.pyc')]

            print('\n[ g.u.i.d.e.r \t%s ]\n\n' % __version__)

            print('Usage:')
            print('\t# %s record [options]' % cmd)
            print('\t$ %s <file> [options]\n' % cmd)
            print('\t# %s top [options]' % cmd)
            print('\t# %s start' % cmd)
            print('\t# %s stop' % cmd)
            print('\t# %s send' % cmd)

            print('Example:')
            print('\t# %s record -s /var/log -e mi -g comm, 1243' % cmd)
            print('\t$ %s guider.dat -o /var/log -a -i' % cmd)
            print('\t$ %s top\n' % cmd)

            print('Options:')
            print('\t[mode]')
            print('\t\t    [thread]')
            print('\t\ttop [top]')
            print('\t\t-y  [system]')
            print('\t\t-f  [function]')
            print('\t\t-F  [file]')
            print('\t[record|top]')
            print('\t\t-e  [enable_optionsPerMode:bellowCharacters]')
            print('\t\t\t  [top] {t(hread)|d(isk)}')
            print('\t\t\t  [function] {m(em)|b(lock)|h(eap)|p(ipe)}')
            print('\t\t\t  [thread] {m(em)|b(lock)|i(rq)|p(ipe)|r(eset)|g(raph)|f(utex)}')
            print('\t\t-d  [disable_optionsPerMode:bellowCharacters]')
            print('\t\t\t  [function] {c(pu)|u(user)}')
            print('\t\t-s  [save_traceData:dir/file]')
            print('\t\t-S  [sort_output:c(pu)/m(em)/b(lock)/w(fc)]')
            print('\t\t-u  [run_inBackground]')
            print('\t\t-W  [wait_forSignal]')
            print('\t\t-R  [record_repeatedly:interval,count]')
            print('\t\t-b  [set_bufferSize:kb]')
            print('\t\t-D  [trace_threadDependency]')
            print('\t\t-t  [trace_syscall:syscalls]')
            print('\t[analysis]')
            print('\t\t-o  [save_outputData:dir]')
            print('\t\t-a  [show_allInfo]')
            print('\t\t-i  [set_interval:sec]')
            print('\t\t-p  [show_preemptInfo:tids]')
            print('\t\t-l  [input_addr2linePath:file]')
            print('\t\t-r  [input_targetRootPath:dir]')
            print('\t\t-q  [make_taskchain]')
            print('\t[common]')
            print('\t\t-g  [filter_specificGroup:comms|tids]')
            print('\t\t-A  [set_arch:arm|x86|x64]')
            print('\t\t-c  [set_customEvent:event:filter]')
            print('\t\t-v  [verbose]')

            print("\nAuthor: \n\t%s(%s)" % (__author__, __email__))
            print("\nReporting bugs: \n\t%s or %s" % (__email__, __repository__))
            print("\nCopyright: ")
            print("\t%s." % (__copyright__))
            print("\tLicense %s." % (__license__))
            print("\tThis is free software.\n")

            sys.exit(0)



    @staticmethod
    def setArch(arch):
        if len(arch) == 0:
            return

        SystemManager.arch = arch
        SystemManager.removeEmptyValue(SystemManager.arch)

        if arch == 'arm':
            ConfigManager.sysList = ConfigManager.sysList_arm
        elif arch == 'x86':
            ConfigManager.sysList = ConfigManager.sysList_x86
        elif arch == 'x64':
            ConfigManager.sysList = ConfigManager.sysList_x64
        else:
            SystemManager.printError('Fail to set archtecture to %s, only support arm / x86 / x64' % arch)
            SystemManager.arch = 'arm'



    @staticmethod
    def writeCustomCmd():
        effectiveCmd = []

        if SystemManager.customCmd is None:
            return

        for cmd in SystemManager.customCmd:
            cmdFormat = cmd.split(':')

            if cmdFormat[0] == '':
                SystemManager.printError("wrong event '%s'" % cmdFormat[0])
                sys.exit(0)

            if len(cmdFormat) == 1:
                cmdFormat.append("common_pid != 0")
            else:
                cmdFormat[1] = "common_pid != 0 && " + cmdFormat[1]

            if SystemManager.writeCmd(cmdFormat[0] + '/filter', cmdFormat[1]) < 0:
                SystemManager.printError("wrong filter '%s' for '%s' event" % (cmdFormat[1], cmdFormat[0]))

            if SystemManager.writeCmd(cmdFormat[0] + '/enable', '1') < 0:
                SystemManager.printError("wrong event '%s'" % cmdFormat[0])
                SystemManager.customCmd.pop(SystemManager.customCmd.index(cmd))
                sys.exit(0)
            else:
                effectiveCmd.append(cmdFormat[0])

        if len(effectiveCmd) > 0:
            SystemManager.printInfo("enabled custom events [ %s ]" % ', '.join(effectiveCmd))



    @staticmethod
    def printAnalOption():
        enableStat = ''
        disableStat = ''

        if SystemManager.isRecordMode() is False and SystemManager.isTopMode() is False:
            # common options #
            enableStat += SystemManager.arch.upper() + ' '
            if SystemManager.warningEnable is True:
                enableStat += 'WARNING '

        if SystemManager.showAll is True:
            enableStat += 'ALL '

        if SystemManager.intervalEnable > 0:
            enableStat += 'INTERVAL '

        if SystemManager.depEnable is True:
            enableStat += 'DEPENDENCY '

        if len(SystemManager.preemptGroup) > 0:
            enableStat += 'PREEMPT '

        # print options #
        if enableStat != '':
            SystemManager.printInfo("enabled analysis options [ %s]" % enableStat)

        if disableStat != '':
            SystemManager.printInfo("disabled analysis options [ %s]" % disableStat)



    @staticmethod
    def printRecordOption():
        enableStat = ''
        disableStat = ''

        # common options #
        enableStat += SystemManager.arch.upper() + ' '
        if SystemManager.warningEnable is True:
            enableStat += 'WARNING '
        if SystemManager.pipeEnable is True:
            enableStat += 'PIPE '

        # check current mode #
        if SystemManager.isFunctionMode() is True:
            SystemManager.printInfo("FUNCTION MODE")

            if SystemManager.cpuEnable is False:
                disableStat += 'CPU '
            else:
                enableStat += 'CPU '

            if SystemManager.memEnable is False:
                disableStat += 'MEMORY '
            else:
                enableStat += 'MEMORY '

            if SystemManager.heapEnable is False:
                disableStat += 'HEAP '
            else:
                enableStat += 'HEAP '

            if SystemManager.blockEnable is False:
                disableStat += 'BLOCK '
            else:
                enableStat += 'BLOCK '

            if SystemManager.userEnable is False:
                disableStat += 'USER '
            else:
                enableStat += 'USER '

        elif SystemManager.isFileMode() is True:
            SystemManager.printInfo("FILE MODE")

        elif SystemManager.isSystemMode() is True:
            SystemManager.printInfo("SYSTEM MODE")
            SystemManager.waitEnable = True

        elif SystemManager.isTopMode() is True:
            SystemManager.printInfo("TOP MODE")
            enableStat += 'CPU MEMORY '

            if SystemManager.diskEnable is True:
                enableStat += 'DISK '
            else:
                disableStat += 'DISK '
            if SystemManager.processEnable is False:
                enableStat += 'THREAD '
            else:
                disableStat += 'THREAD '

        else:
            SystemManager.printInfo("THREAD MODE")
            SystemManager.threadEnable = True
            enableStat += 'CPU '

            if SystemManager.memEnable is True:
                enableStat += 'MEMORY '
            else:
                disableStat += 'MEMORY '
            if SystemManager.blockEnable is True:
                enableStat += 'BLOCK '
            else:
                disableStat += 'BLOCK '
            if SystemManager.irqEnable is True:
                enableStat += 'IRQ '
            else:
                disableStat += 'IRQ '
            if SystemManager.repeatCount > 0:
                enableStat += 'REPEAT '
            else:
                disableStat += 'REPEAT '
            if SystemManager.depEnable is True:
                enableStat += 'DEPENDENCY '
            else:
                disableStat += 'DEPENDENCY '
            if SystemManager.sysEnable is True:
                enableStat += 'SYSCALL '
            else:
                disableStat += 'SYSCALL '
            if SystemManager.graphEnable is True:
                enableStat += 'GRAPH '
            else:
                disableStat += 'GRAPH '
            if SystemManager.futexEnable is True:
                enableStat += 'FUTEX '
            else:
                disableStat += 'FUTEX '
            if SystemManager.resetEnable is True:
                enableStat += 'RESET '
            else:
                disableStat += 'RESET '

        # print options #
        if enableStat != '':
            SystemManager.printInfo("enabled recording options [ %s]" % enableStat)

        if disableStat != '':
            SystemManager.printInfo("disabled recording options [ %s]" % disableStat)



    @staticmethod
    def isThreadMode():
        return SystemManager.threadEnable



    @staticmethod
    def isFunctionMode():
        return SystemManager.functionEnable



    @staticmethod
    def isFileMode():
        return SystemManager.fileEnable



    @staticmethod
    def isSystemMode():
        return SystemManager.systemEnable



    @staticmethod
    def defaultHandler(signum, frame):
        return



    @staticmethod
    def stopHandler(signum, frame):
        if SystemManager.isFileMode() is True:
            SystemManager.condExit = True
        elif SystemManager.isTopMode() is True:
            if SystemManager.printFile is not None:
                SystemManager.printTitle()
                SystemManager.pipePrint(SystemManager.procBuffer)
                SystemManager.printInfo("Saved top usage into %s successfully" % \
                    SystemManager.inputFile)
            sys.exit(0)
        else:
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            SystemManager.runRecordStopCmd()

        # update record status #
        SystemManager.recordStatus = False

        SystemManager.repeatCount = 0

        SystemManager.printStatus('ready to save and analyze... [ STOP(ctrl + c) ]')



    @staticmethod
    def newHandler(signum, frame):
        SystemManager.condExit = False

        if SystemManager.isFileMode() is True:
            SystemManager.printStatus("Saved file usage successfully")
        elif SystemManager.isTopMode() is True:
            SystemManager.printTitle()
            SystemManager.pipePrint(SystemManager.procBuffer)

            if SystemManager.fileForPrint is not None:
                SystemManager.fileForPrint.close()
                SystemManager.fileForPrint = None

            SystemManager.procBuffer = []
            SystemManager.procBufferSize = 0

            if SystemManager.printFile is not None:
                SystemManager.printStatus("Saved top usage into %s successfully" % \
                    SystemManager.inputFile)
        elif SystemManager.resetEnable is True:
            SystemManager.writeEvent("EVENT_START")
        else:
            SystemManager.writeEvent("EVENT_MARK")



    @staticmethod
    def exitHandler(signum, frame):
        SystemManager.printError('Terminated by user\n')
        sys.exit(0)



    @staticmethod
    def isRelocatableFile(path):
        if path.find('.so') == -1 and \
            path.find('.ttf') == -1 and \
            path.find('.pak') == -1:
            return False
        else:
            return True



    @staticmethod
    def exitHandlerForPartInfo(signum, frame):
        for dirnames in os.walk('/sys/class/block'):
            for subdirname in dirnames[1]:
                devPath = '/sys/class/block/' + subdirname + '/dev'
                sizePath = '/sys/class/block/' + subdirname + '/size'
                devFd = open(devPath, 'r')
                sizeFd = open(sizePath, 'r')
                dev = devFd.readline().rstrip()
                size = sizeFd.readline().rstrip()



    @staticmethod
    def timerHandler(signum, frame):
        raise



    @staticmethod
    def alarmHandler(signum, frame):
        if SystemManager.pipeEnable is True:
            if SystemManager.repeatCount > 0:
                SystemManager.runRecordStopCmd()
                SystemManager.repeatInterval = 5
                SystemManager.repeatCount = 0
                signal.alarm(SystemManager.repeatInterval)
            else:
                sys.exit(0)
        elif SystemManager.repeatCount > 0:
            if SystemManager.outputFile != None:
                output = SystemManager.outputFile + str(SystemManager.repeatCount)
                try:
                    shutil.copy(os.path.join(SystemManager.mountPath + '../trace'), output)
                    SystemManager.printInfo('trace data is saved to %s' % output)
                except:
                    SystemManager.printWarning('Fail to save trace data to %s' % output)

                SystemManager.repeatCount -= 1
                signal.alarm(SystemManager.repeatInterval)
            else:
                SystemManager.printError('Fail to save trace data because output file is not set')
                sys.exit(0)
        else:
            sys.exit(0)



    @staticmethod
    def saveDataAndExit(lines):
        # save trace data to file #
        try:
            if SystemManager.outputFile != None:
                # backup data file alread exist #
                if os.path.isfile(SystemManager.outputFile) is True:
                    shutil.copy(SystemManager.outputFile, \
                            os.path.join(SystemManager.outputFile + '.old'))

                f = open(SystemManager.outputFile, 'w')

                if SystemManager.systemInfoBuffer is not '':
                    f.writelines(SystemManager.magicString + '\n')
                    f.writelines(SystemManager.systemInfoBuffer)
                    f.writelines(SystemManager.magicString + '\n')

                f.writelines(lines)

                SystemManager.printInfo('trace data is saved to %s' % SystemManager.outputFile)

                sys.exit(0)
        except IOError:
            SystemManager.printError("Fail to write data to %s" % SystemManager.outputFile)
            sys.exit(0)



    @staticmethod
    def writeCmd(path, val):
        try:
            fd = open(SystemManager.mountPath + path, 'w')
        except:
            SystemManager.printWarning(\
                "Fail to use %s event, please confirm kernel configuration" % path[0:path.rfind('/')])
            return -1

        try:
            fd.write(val)
            fd.close()
        except:
            SystemManager.printWarning("Fail to apply command %s to %s" % (val, path))
            return -2

        return 0



    @staticmethod
    def printProgress(current, dest):
        div = round((current / float(dest)) * 100, 1)
        percent = int(div)

        if div != percent:
            return

        mod = percent % 4

        sys.stdout.write('%3d' % percent + \
            ('% ' + SystemManager.progressChar[mod] + '\b' * 6))
        sys.stdout.flush()



    @staticmethod
    def addPrint(string):
        SystemManager.bufferString += string
        SystemManager.bufferRows += 1



    @staticmethod
    def clearPrint():
        del SystemManager.bufferString
        SystemManager.bufferString = ''



    @staticmethod
    def printTitle():
        if SystemManager.printFile is None:
            os.system('clear')

        SystemManager.pipePrint("[ g.u.i.d.e.r \tver.%s ]\n" % __version__)



    @staticmethod
    def printInfoBuffer():
        SystemManager.pipePrint(SystemManager.systemInfoBuffer)



    @staticmethod
    def removeEmptyValue(targetList):
        for val in targetList:
            if val == '':
                del targetList[targetList.index('')]



    @staticmethod
    def applyLaunchOption():
        # check whether there is launch option in saved buffer #
        if SystemManager.systemInfoBuffer == '':
            return
        launchPosStart = SystemManager.systemInfoBuffer.find('Launch')
        if launchPosStart == -1:
            return
        launchPosEnd = SystemManager.systemInfoBuffer.find('\n', launchPosStart)
        if launchPosEnd == -1:
            return

        # get launch option recorded #
        SystemManager.launchBuffer = SystemManager.systemInfoBuffer[launchPosStart:launchPosEnd]

        # apply mode option #
        launchPosStart = SystemManager.launchBuffer.find(' -f')
        if launchPosStart > -1:
            SystemManager.functionEnable = True
            SystemManager.threadEnable = False

            SystemManager.printInfo("FUNCTION MODE")
        else:
            SystemManager.printInfo("THREAD MODE")

        # apply group filter option #
        filterList = None
        launchPosStart = SystemManager.launchBuffer.find(' -g')
        if SystemManager.isThreadMode() is True and launchPosStart > -1:
            filterList = SystemManager.launchBuffer[launchPosStart + 3:]
            filterList = filterList[:filterList.find(' -')].replace(" ", "")
            SystemManager.showGroup = filterList.split(',')
            SystemManager.removeEmptyValue(SystemManager.showGroup)
            SystemManager.printInfo("only specific threads [%s] were recorded" % ', '.join(SystemManager.showGroup))

        # check filter list #
        if len(SystemManager.showGroup) > 0:
            SystemManager.printInfo("only specific threads %s are shown" % ','.join(SystemManager.showGroup))

        # apply dependency option #
        launchPosStart = SystemManager.launchBuffer.find(' -D')
        if launchPosStart > -1:
            SystemManager.depEnable = True

        # apply disable option #
        launchPosStart = SystemManager.launchBuffer.find(' -d')
        if launchPosStart > -1:
            filterList = SystemManager.launchBuffer[launchPosStart + 3:]
            if filterList[:filterList.find(' -')].find('u') > -1:
                SystemManager.userEnable = False

        # apply arch option #
        launchPosStart = SystemManager.launchBuffer.find(' -A')
        if launchPosStart > -1:
            filterList = SystemManager.launchBuffer[launchPosStart + 3:]
            filterList = filterList[:filterList.find(' -')].replace(" ", "")

            if SystemManager.arch != filterList:
                SystemManager.printError(\
                    "arch(%s) of recorded target is different with current arch(%s), use -A option with %s" % \
                    (filterList, SystemManager.arch, filterList))
                sys.exit(0)



    @staticmethod
    def writeEvent(message):
        if SystemManager.eventLogFD == None:
            if SystemManager.eventLogFile is None:
                SystemManager.eventLogFile = str(SystemManager.getMountPath()) + '/tracing/trace_marker'

            try:
                SystemManager.eventLogFD = open(SystemManager.eventLogFile, 'w')
            except:
                SystemManager.printError("Fail to open %s to write event\n" % SystemManager.eventLogFD)

        if SystemManager.eventLogFD != None:
            try:
                SystemManager.eventLogFD.write(message)
                if SystemManager.resetEnable is True:
                    SystemManager.printInfo('marked RESET event')
                else:
                    SystemManager.printInfo('marked user-defined event')
                SystemManager.eventLogFD.close()
                SystemManager.eventLogFD = None
            except:
                SystemManager.printError("Fail to write %s event\n" % (message))
        else:
            SystemManager.printError("Fail to write %s event because there is no file descriptor\n" % message)



    @staticmethod
    def infoBufferPrint(line):
        SystemManager.systemInfoBuffer += line + '\n'



    @staticmethod
    def clearInfoBuffer():
        SystemManager.systemInfoBuffer = ''



    @staticmethod
    def pipePrint(line):
        if SystemManager.pipeForPrint == None and SystemManager.selectMenu == None and \
            SystemManager.printFile == None and SystemManager.isTopMode() is False:
            try:
                SystemManager.pipeForPrint = os.popen('less', 'w')
            except:
                SystemManager.printError("Fail to find less util, use -o option to save output into file\n")
                sys.exit(0)

        if SystemManager.pipeForPrint != None:
            try:
                SystemManager.pipeForPrint.write(line + '\n')
                return
            except:
                SystemManager.printError("Failed to print to pipe\n")
                SystemManager.pipeForPrint = None

        if SystemManager.printFile != None and SystemManager.fileForPrint == None:
            if SystemManager.isRecordMode() is False and SystemManager.isTopMode() is False:
                fileNamePos = SystemManager.inputFile.rfind('/')
                if  fileNamePos >= 0:
                    SystemManager.inputFile = SystemManager.inputFile[fileNamePos + 1:]
                SystemManager.inputFile = \
                    SystemManager.printFile + '/' + SystemManager.inputFile.replace('dat', 'out')
            else:
                SystemManager.inputFile = SystemManager.printFile + '/guider.out'

            SystemManager.inputFile = SystemManager.inputFile.replace('//', '/')

            try:
                # backup output file #
                shutil.copy(SystemManager.inputFile, os.path.join(SystemManager.inputFile + '.old'))
            except:
                pass

            try:
                SystemManager.fileForPrint = open(SystemManager.inputFile, 'w')

                # print output file name #
                if SystemManager.printFile != None:
                    SystemManager.printInfo("write to %s" % (SystemManager.inputFile))
            except:
                SystemManager.printError("Fail to open %s\n" % (SystemManager.inputFile))
                sys.exit(0)

        if SystemManager.fileForPrint != None:
            try:
                if SystemManager.isTopMode() is False:
                    SystemManager.fileForPrint.write(line + '\n')
                else:
                    SystemManager.fileForPrint.writelines(line)
            except:
                SystemManager.printError("Failed to print to file\n")
                SystemManager.pipeForPrint = None
        else:
            print(line)



    @staticmethod
    def printWarning(line):
        if SystemManager.warningEnable is True:
            print('\n' + ConfigManager.WARNING + '[Warning] ' + line + ConfigManager.ENDC)



    @staticmethod
    def printError(line):
        print('\n' + ConfigManager.FAIL + '[Error] ' + line + ConfigManager.ENDC)



    @staticmethod
    def printInfo(line):
        print('\n' + ConfigManager.BOLD + '[Info] ' + line + ConfigManager.ENDC)



    @staticmethod
    def printGood(line):
        print('\n' + ConfigManager.OKGREEN + '[Info] ' + line + ConfigManager.ENDC)



    @staticmethod
    def printUnderline(line):
        print('\n' + ConfigManager.UNDERLINE + line + ConfigManager.ENDC)



    @staticmethod
    def printStatus(line):
        print('\n' + ConfigManager.SPECIAL + '[Step] ' + line + ConfigManager.ENDC)



    @staticmethod
    def parseAddOption():
        if len(sys.argv) <= 2:
            return

        SystemManager.optionList = ' '.join(sys.argv[1:]).split(' -')[1:]
        for seq in range(0, len(SystemManager.optionList)):
            SystemManager.optionList[seq] = SystemManager.optionList[seq].replace(" ", "")

        for item in SystemManager.optionList:
            option = item[0]
            value = item[1:]

            if option == 'i':
                if len(value) == 0:
                    SystemManager.intervalEnable = 1
                    continue

                try:
                    if int(value) > 0:
                        SystemManager.intervalEnable = int(value)
                except:
                    SystemManager.printError("wrong option value %s with -i option" % value)
                    sys.exit(0)

            elif option == 'o':
                SystemManager.printFile = str(value)
                if os.path.isdir(SystemManager.printFile) == False:
                    SystemManager.printError("wrong option value %s with -o option, use existing directory path" % value)
                    sys.exit(0)

            elif option == 'a':
                SystemManager.showAll = True

            elif option == 'q':
                SystemManager.selectMenu = True
                ConfigManager.taskChainEnable = True

            elif option == 'D':
                SystemManager.depEnable = True

            elif option == 'p':
                if SystemManager.intervalEnable > 0:
                    SystemManager.printWarning("-i option is already enabled, -p option is disabled")
                else:
                    SystemManager.preemptGroup = value.split(',')
                    SystemManager.removeEmptyValue(SystemManager.preemptGroup)

                    if len(SystemManager.preemptGroup) == 0:
                        SystemManager.printError("No specific thread targeted, input tid with -p option")
                        sys.exit(0)

            elif option == 'd':
                # Add somethings to diable when analyzing data #
                options = value

            elif option == 'c':
                SystemManager.customCmd = str(value).split(',')
                SystemManager.removeEmptyValue(SystemManager.customCmd)

            elif option == 'g':
                SystemManager.showGroup = value.split(',')
                SystemManager.removeEmptyValue(SystemManager.showGroup)

            elif option == 'A':
                SystemManager.setArch(value)

            elif option == 'e':
                options = value
                if options.rfind('g') > -1:
                    SystemManager.graphEnable = True
                if options.rfind('d') > -1:
                    SystemManager.diskEnable = True
                if options.rfind('t') > -1:
                    SystemManager.processEnable = False

            elif option == 'v':
                SystemManager.warningEnable = True

            elif option == 'f':
                # Handle error about record option #
                if SystemManager.isFunctionMode() is True and SystemManager.outputFile is None:
                    SystemManager.printError("wrong option with -f, use also -s option to save data")
                    sys.exit(0)
                else:
                    SystemManager.functionEnable = True

            elif option == 'l':
                SystemManager.addr2linePath = value.split(',')

            elif option == 'r':
                SystemManager.rootPath = value

            elif option == 'h':
                SystemManager.printOptions()

            elif option == 'b':
                try:
                    if int(value) > 0:
                        SystemManager.bufferSize = str(value)
                    else:
                        SystemManager.printError("wrong option value %s with -b option" % value)
                        sys.exit(0)
                except:
                    SystemManager.printError("wrong option value %s with -b option" % value)
                    sys.exit(0)

            elif option == 'S':
                SystemManager.sort = value
                if len(SystemManager.sort) > 0:
                    if SystemManager.sort == 'c':
                        SystemManager.printInfo("sorted by CPU")
                    elif SystemManager.sort == 'm':
                        SystemManager.printInfo("sorted by MEMORY")
                    elif SystemManager.sort == 'b':
                        SystemManager.printInfo("sorted by BLOCK_READ")
                    elif SystemManager.sort == 'w':
                        SystemManager.printInfo("sorted by WaitForChild")
                    else:
                        SystemManager.printError("wrong option value %s with -S option" % SystemManager.sort)
                        sys.exit(0)

            elif option == 'u':
                SystemManager.backgroundEnable = True

            elif option == 'W' or option == 'y' or option == 's' or option == 'R' or option == 'F' or option == 't':
                continue

            else:
                SystemManager.printError("unrecognized option -%s" % option)
                sys.exit(0)

    @staticmethod
    def parseRecordOption():
        if len(sys.argv) <= 2:
            return

        SystemManager.optionList = ' '.join(sys.argv[1:]).split(' -')[1:]
        for seq in range(0, len(SystemManager.optionList)):
            SystemManager.optionList[seq] = SystemManager.optionList[seq].replace(" ", "")

        for item in SystemManager.optionList:
            option = item[0]
            value = item[1:]

            if option == 'b':
                try:
                    if int(value) > 0:
                        SystemManager.bufferSize = str(value)
                    else:
                        SystemManager.printError("wrong option value %s with -b option" % value)
                        sys.exit(0)
                except:
                    SystemManager.printError("wrong option value %s with -b option" % value)
                    sys.exit(0)

            elif option == 'f':
                SystemManager.functionEnable = True

            elif option == 'u':
                SystemManager.backgroundEnable = True

            elif option == 'y':
                SystemManager.systemEnable = True

            elif option == 'A':
                SystemManager.setArch(value)

            elif option == 'e':
                options = value
                if options.rfind('i') > -1:
                    SystemManager.irqEnable = True
                if options.rfind('m') > -1:
                    SystemManager.memEnable = True
                if options.rfind('h') > -1:
                    SystemManager.heapEnable = True
                if options.rfind('b') > -1:
                    SystemManager.blockEnable = True
                if options.rfind('p') > -1:
                    SystemManager.pipeEnable = True
                if options.rfind('f') > -1:
                    SystemManager.futexEnable = True
                if options.rfind('r') > -1:
                    SystemManager.resetEnable = True

            elif option == 'v':
                SystemManager.warningEnable = True

            elif option == 'g':
                SystemManager.showGroup = value.split(',')
                SystemManager.removeEmptyValue(SystemManager.showGroup)
                if len(SystemManager.showGroup) == 0:
                    SystemManager.printError("Input value for filtering with -g option")
                    sys.exit(0)
                SystemManager.printInfo("only specific threads [%s] are shown" % \
                    ', '.join(SystemManager.showGroup))

            elif option == 's':
                if SystemManager.isRecordMode() is False:
                    SystemManager.printError("Fail to save data because now is not in recording mode")
                    sys.exit(0)

                SystemManager.outputFile = str(value)

                if os.path.isdir(SystemManager.outputFile) is True:
                    SystemManager.outputFile = SystemManager.outputFile + '/guider.dat'
                elif os.path.isdir(SystemManager.outputFile[:SystemManager.outputFile.rfind('/')]) is True:
                    continue
                else:
                    SystemManager.printError("wrong option value %s with -s option" % value)
                    sys.exit(0)

                SystemManager.outputFile = SystemManager.outputFile.replace('//', '/')

            elif option == 'D':
                SystemManager.depEnable = True

            elif option == 'W':
                SystemManager.waitEnable = True

            elif option == 'F':
                SystemManager.fileEnable = True

            elif option == 't':
                SystemManager.sysEnable = True
                SystemManager.syscallList = value.split(',')
                SystemManager.removeEmptyValue(SystemManager.syscallList)
                enabledSyscall = []

                for val in SystemManager.syscallList:
                    try:
                        if val[0:4] == 'sys_':
                            nrSyscall = ConfigManager.sysList.index(val)
                        else:
                            nrSyscall = ConfigManager.sysList.index('sys_' + val)

                        enabledSyscall.append(ConfigManager.sysList[nrSyscall])
                        SystemManager.syscallList[SystemManager.syscallList.index(val)] = nrSyscall
                    except:
                        SystemManager.printError("No %s syscall in %s ABI" % (val, SystemManager.arch))
                        SystemManager.syscallList.remove(val)

                if len(enabledSyscall) == 0:
                    SystemManager.printInfo("enabled syscall list [ ALL ]")
                else:
                    SystemManager.printInfo("enabled syscall list [ %s ]" % ', '.join(enabledSyscall))

            elif option == 'R':
                repeatParams = value.split(',')
                if len(repeatParams) != 2:
                    SystemManager.printError("wrong option with -R, use -R INTERVAL,REPEAT")
                    sys.exit(0)
                else:
                    try:
                        SystemManager.repeatInterval = int(repeatParams[0])
                        SystemManager.repeatCount = int(repeatParams[1])
                    except:
                        SystemManager.printError("wrong option with -R, use integer values")
                        sys.exit(0)

                if SystemManager.repeatInterval < 1 or SystemManager.repeatCount < 1:
                    SystemManager.printError("wrong option with -R, use values bigger than 0")
                    sys.exit(0)

            elif option == 'o':
                SystemManager.printFile = str(value)

            elif option == 'c':
                SystemManager.customCmd = str(value).split(',')
                SystemManager.removeEmptyValue(SystemManager.customCmd)

            elif option == 'd':
                options = value
                if options.rfind('c') > -1:
                    SystemManager.cpuEnable = False
                if options.rfind('m') > -1:
                    SystemManager.memEnable = False
                if options.rfind('h') > -1:
                    SystemManager.heapEnable = False
                if options.rfind('b') > -1:
                    SystemManager.blockEnable = False
                if options.rfind('u') > -1:
                    SystemManager.userEnable = False

            # Ignore options #
            elif option == 'l' or option == 'r' or option == 'i' or option == 'a' or option == 'q' or \
                option == 'g' or option == 'p' or option == 'S' or option == 'h':
                continue

            else:
                SystemManager.printError("wrong option -%s" % option)
                sys.exit(0)



    @staticmethod
    def makeKerSymTable(symbol):
        try:
            f = open('/proc/kallsyms', 'r')
        except IOError:
            SystemManager.printWarning("Fail to open %s" % '/proc/kallsyms')

        ret = None
        startPos = len(SystemManager.kerSymTable)
        curPos = 0

        while True:
            line = f.readline()
            curPos += 1

            if startPos > curPos:
                continue

            # Cache address and symbol #
            line = line.split()
            SystemManager.kerSymTable[line[2]] = line[0]

            if line[2] == symbol:
                ret = line[0]
                break

        f.close()
        return ret



    @staticmethod
    def getKerAddr(symbol):
        try:
            return SystemManager.kerSymTable[symbol]
        except:
            return SystemManager.makeKerSymTable(symbol)



    @staticmethod
    def isRecordMode():
        if sys.argv[1] == 'record':
            return True
        else:
            return False



    @staticmethod
    def isStartMode():
        if sys.argv[1] == 'start':
            return True
        else:
            return False


    @staticmethod
    def isListMode():
        if sys.argv[1] == 'list':
            return True
        else:
            return False



    @staticmethod
    def isStopMode():
        if sys.argv[1] == 'stop':
            return True
        else:
            return False


    @staticmethod
    def isSendMode():
        if sys.argv[1] == 'send':
            return True
        else:
            return False



    @staticmethod
    def isTopMode():
        if sys.argv[1] == 'top':
            return True
        else:
            return False



    @staticmethod
    def printBackgroundProcs():
        nrProc = 0
        printBuf = ''
        myPid = str(os.getpid())
        compLen = len(__module__)

        pids = os.listdir(SystemManager.procPath)
        for pid in pids:
            if myPid == pid:
                continue

            try:
                int(pid)
            except:
                continue

            # make comm path of pid #
            procPath = os.path.join(SystemManager.procPath, pid)

            fd = open(procPath + '/comm', 'r')
            comm = fd.readline()[0:-1]
            if comm[0:compLen] == __module__:
                try:
                    cmdFd = open(procPath + '/cmdline', 'r')
                    cmdline = cmdFd.readline().replace("\x00", " ")
                    printBuf += "%6s\t%s\n" % (pid, cmdline)
                except:
                    continue

                nrProc += 1

        if nrProc == 0:
            SystemManager.printInfo("No running process in background")
        else:
            print('\n[Running Process]')
            print(twoLine)
            print("%6s\t%s" % ("PID", "COMMAND"))
            print(oneLine)
            print(printBuf,)
            print(oneLine, '\n')


    @staticmethod
    def sendSignalProcs(nrSig):
        nrProc = 0
        myPid = str(os.getpid())
        compLen = len(__module__)

        commLocation = sys.argv[0].rfind('/')
        if commLocation >= 0:
            targetComm = sys.argv[0][commLocation + 1:]
        else:
            targetComm = sys.argv[0]

        pids = os.listdir(SystemManager.procPath)
        for pid in pids:
            if myPid == pid:
                continue

            try:
                int(pid)
            except:
                continue

            # make comm path of pid #
            procPath = os.path.join(SystemManager.procPath, pid)

            try:
                fd = open(procPath + '/comm', 'r')
            except:
                continue

            comm = fd.readline()[0:-1]
            if comm[0:compLen] == __module__:
                if nrSig == signal.SIGINT:
                    waitStatus = False

                    try:
                        cmdFd = open(procPath + '/cmdline', 'r')
                        cmdList = cmdFd.readline().split('\x00')
                        for val in cmdList:
                            if val == '-c':
                                waitStatus = True
                    except:
                        continue

                    if SystemManager.isStartMode() is True and waitStatus is True:
                        try:
                            os.kill(int(pid), nrSig)
                            SystemManager.printInfo("started %s process to profile" % pid)
                        except:
                            SystemManager.printError("Fail to send signal to %s because of permission" % pid)
                    elif SystemManager.isStopMode() is True:
                        try:
                            os.kill(int(pid), nrSig)
                            SystemManager.printInfo("terminated %s process" % pid)
                        except:
                            SystemManager.printError("Fail to send signal to %s because of permission" % pid)
                elif nrSig == signal.SIGQUIT:
                    try:
                        os.kill(int(pid), nrSig)
                        SystemManager.printInfo("sent signal to %s process" % pid)
                    except:
                        SystemManager.printError("Fail to send signal to %s because of permission" % pid)

                nrProc += 1

        if nrProc == 0:
            SystemManager.printInfo("No running process in background")



    @staticmethod
    def setRtPriority(pri):
        os.system('chrt -a -p %s %s 2> /dev/null &' % (pri, os.getpid()))



    @staticmethod
    def setIdlePriority():
        os.system('chrt -a -i -p %s %s 2> /dev/null &' % (0, os.getpid()))



    @staticmethod
    def setTtyCols(cols):
        os.system('stty cols %s' % (cols))



    @staticmethod
    def setTtyRows(rows):
        os.system('stty rows %s' % (rows))



    @staticmethod
    def getTty():
        try:
            SystemManager.ttyRows, SystemManager.ttyCols = \
                os.popen('stty size', 'r').read().split()
        except:
            SystemManager.printWarning("Fail to use stty")



    def saveSystemManager(self):
        uptimeFile = '/proc/uptime'

        try:
            f = open(uptimeFile, 'r')
            self.uptimeData = f.readline()
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % uptimeFile)

        self.uptimeData = self.uptimeData.split()
        # uptimeData[0] = running time in sec, [1]= idle time in sec * cores #

        cmdlineFile = '/proc/cmdline'

        try:
            f = open(cmdlineFile, 'r')
            self.cmdlineData = f.readline()[0:-1]
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % cmdlineFile)

        loadFile = '/proc/loadavg'

        try:
            f = open(loadFile, 'r')
            self.loadData = f.readline()
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % loadFile)

        self.loadData = self.loadData.split()
        '''
        loadData[0] = 1min usage, \
        [1] = 5min usage, \
        [2] = 15min usage, \
        [3] = running/total thread, \
        [4] = lastPid
        '''

        kernelVersionFile = '/proc/sys/kernel/osrelease'

        try:
            f = open(kernelVersionFile, 'r')
            self.SystemManager['kernelVer'] = f.readline()[0:-1]
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % kernelVersionFile)

        osVersionFile = '/proc/sys/kernel/version'

        try:
            f = open(osVersionFile, 'r')
            self.SystemManager['osVer'] = f.readline()[0:-1]
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % osVersionFile)

        osTypeFile = '/proc/sys/kernel/ostype'

        try:
            f = open(osTypeFile, 'r')
            self.SystemManager['osType'] = f.readline()[0:-1]
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % osTypeFile)

        timeFile = '/proc/driver/rtc'

        try:
            f = open(timeFile, 'r')
            timeInfo = f.readlines()

            for val in timeInfo:
                timeEntity = val.split()

                if timeEntity[0] == 'rtc_time':
                    self.SystemManager['time'] = timeEntity[2]
                elif timeEntity[0] == 'rtc_date':
                    self.SystemManager['date'] = timeEntity[2]

            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % osTypeFile)



    def saveAllInfo(self):
        self.saveCpuInfo()
        self.saveMemInfo()
        self.saveDiskInfo()
        self.saveSystemManager()
        self.saveWebOSInfo()



    def saveWebOSInfo(self):
        OSFile = '/var/run/nyx/os_info.json'
        devFile = '/var/run/nyx/device_info.json'

        try:
            f = open(OSFile, 'r')
            self.osData = f.readlines()
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s for webOS" % OSFile)

        try:
            f = open(devFile, 'r')
            self.devData = f.readlines()
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s for webOS" % devFile)



    def saveCpuInfo(self):
        cpuFile = '/proc/cpuinfo'

        try:
            f = open(cpuFile, 'r')
            self.cpuData = f.readlines()
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % cpuFile)



    def saveDiskInfo(self):
        diskFile = '/proc/diskstats'
        mountFile = '/proc/mounts'

        try:
            df = open(diskFile, 'r')

            if self.diskBeforeData is None:
                self.diskBeforeData = df.readlines()
            else:
                self.diskAfterData = df.readlines()

                try:
                    mf = open(mountFile, 'r')
                    self.mountData = mf.readlines()
                    mf.close()
                except:
                    SystemManager.printWarning("Fail to open %s" % mountFile)

            df.close()
        except:
            SystemManager.printWarning("Fail to open %s" % diskFile)



    def saveMemInfo(self):
        memFile = '/proc/meminfo'

        try:
            f = open(memFile, 'r')
            lines = f.readlines()

            if self.memBeforeData is None:
                self.memBeforeData = lines
            else:
                self.memAfterData = lines

            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % memFile)



    @staticmethod
    def getBufferSize():
        bufFile = "../buffer_size_kb"

        try:
            f = open(SystemManager.mountPath + bufFile, 'r')
            size = f.readlines()
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % bufFile)
            return 0


        return int(size[0])



    @staticmethod
    def copyPipeToFile(pipePath, filePath):
        try:
            pd = open(pipePath, 'r')
        except:
            SystemManager.printError("Fail to open %s" % pipePath)
            sys.exit(0)

        try:
            # use os.O_DIRECT | os.O_RDWR | os.O_TRUNC | os.O_CREAT #
            fd = open(filePath, 'w')
        except:
            SystemManager.printError("Fail to open %s" % filePath)
            sys.exit(0)

        while True:
            try:
                if SystemManager.recordStatus is False:
                    raise

                data = pd.read(SystemManager.pageSize)
                fd.write(data)
            except:
                pd.close()
                fd.close()
                return



    @staticmethod
    def getMountPath():
        f = open('/proc/mounts', 'r')
        lines = f.readlines()

        for l in lines:
            m = re.match(r'(?P<dev>\S+)\s+(?P<dir>\S+)\s+(?P<fs>\S+)', l)
            if m is not None:
                d = m.groupdict()
                if d['fs'] == 'debugfs':
                    f.close()
                    return d['dir']
        f.close()




    @staticmethod
    def clearTraceBuffer():
        SystemManager.writeCmd("../trace", '')



    def initCmdList(self):
        self.cmdList["sched/sched_switch"] = True
        self.cmdList["sched/sched_process_wait"] = True
        self.cmdList["sched/sched_process_exit"] = True
        self.cmdList["sched/sched_wakeup"] = SystemManager.depEnable
        self.cmdList["irq"] = SystemManager.irqEnable
        self.cmdList["signal"] = SystemManager.depEnable
        self.cmdList["raw_syscalls/sys_enter"] = SystemManager.depEnable
        self.cmdList["raw_syscalls/sys_exit"] = SystemManager.depEnable
        self.cmdList["raw_syscalls"] = SystemManager.sysEnable
        self.cmdList["kmem/mm_page_alloc"] = SystemManager.memEnable
        self.cmdList["kmem/mm_page_free"] = SystemManager.memEnable
        self.cmdList["kmem/kmalloc"] = SystemManager.memEnable
        self.cmdList["kmem/kfree"] = SystemManager.memEnable
        self.cmdList["filemap/mm_filemap_add_to_page_cache"] = False
        self.cmdList["filemap/mm_filemap_delete_from_page_cache"] = SystemManager.memEnable
        self.cmdList["timer/hrtimer_start"] = False
        self.cmdList["block/block_bio_remap"] = SystemManager.blockEnable
        self.cmdList["block/block_rq_complete"] = SystemManager.blockEnable
        self.cmdList["writeback/writeback_dirty_page"] = SystemManager.blockEnable
        self.cmdList["writeback/wbc_writepage"] = SystemManager.blockEnable
        self.cmdList["vmscan/mm_vmscan_direct_reclaim_begin"] = True
        self.cmdList["vmscan/mm_vmscan_direct_reclaim_end"] = True
        self.cmdList["sched/sched_migrate_task"] = True
        self.cmdList["task"] = True
        self.cmdList["signal"] = True
        self.cmdList["power/suspend_resume"] = True
        self.cmdList["printk"] = True
        self.cmdList["module/module_load"] = True
        self.cmdList["module/module_free"] = True
        self.cmdList["module/module_put"] = True
        self.cmdList["power/cpu_idle"] = True
        self.cmdList["power/cpu_frequency"] = True
        self.cmdList["vmscan/mm_vmscan_wakeup_kswapd"] = False
        self.cmdList["vmscan/mm_vmscan_kswapd_sleep"] = False



    def runPeriodProc(self):
        pid = os.fork()

        if pid == 0:
            signal.signal(signal.SIGINT, 0)

            while True:
                time.sleep(0.0001)

            sys.exit(0)



    def runRecordStartCmd(self):
        cmd = self.getMountPath()
        if cmd == None:
            SystemManager.mountPath = "/sys/kernel/debug"
            cmd = "mount -t debugfs nodev " + SystemManager.mountPath + ";"
            os.system(cmd)
        else:
            SystemManager.mountPath = str(cmd)

        SystemManager.mountPath += "/tracing/events/"

        # check permission #
        if os.path.isdir(SystemManager.mountPath) == False:
            if os.geteuid() == 0:
                SystemManager.printError("Check whether ftrace options are enabled in kernel")
            else:
                SystemManager.printError("Fail to get root permission")

            sys.exit(0)

        # make trace buffer empty #
        self.clearTraceBuffer()

        # set size of trace buffer per core #
        SystemManager.writeCmd("../buffer_size_kb", SystemManager.bufferSize)
        setBufferSize = SystemManager.getBufferSize()
        if int(SystemManager.bufferSize) != setBufferSize:
            SystemManager.printWarning("Set buffer size(%s) is different with %s" % \
                (setBufferSize, SystemManager.bufferSize))

        # initialize event list to enable #
        self.initCmdList()

        # set log format #
        SystemManager.writeCmd('../trace_options', 'noirq-info')
        SystemManager.writeCmd('../trace_options', 'noannotate')
        SystemManager.writeCmd('../trace_options', 'print-tgid')

        if SystemManager.isFunctionMode() is True:
            cmd = ""

            # make filter command for function profiler #
            for cond in SystemManager.showGroup:
                try:
                    cmd += "common_pid == %s || " % int(cond)
                except:
                    if cond.find('>') == -1 and cond.find('<') == -1:
                        SystemManager.printError("wrong tid %s" % cond)
                        sys.exit(0)
                    else:
                        try:
                            if cond.find('>') >= 0:
                                cmd += "common_pid <= %s ||" % int(cond[:cond.find('>')])
                            elif cond.find('<') >= 0:
                                cmd += "common_pid >= %s ||" % int(cond[:cond.find('<')])
                        except:
                            SystemManager.printError("wrong condition %s" % cond)
                            sys.exit(0)

            if cmd == "":
                cmd = "(common_pid != 0)"
            else:
                cmd = "(" + cmd[:cmd.rfind('||')] + ")"

            if SystemManager.userEnable is True:
                SystemManager.writeCmd('../trace_options', 'userstacktrace')
                SystemManager.writeCmd('../trace_options', 'sym-userobj')
            else:
                SystemManager.writeCmd('../trace_options', 'nouserstacktrace')
                SystemManager.writeCmd('../trace_options', 'nosym-userobj')

            SystemManager.writeCmd('../trace_options', 'sym-addr')
            SystemManager.writeCmd('../options/stacktrace', '1')

            # enable custom events #
            SystemManager.writeCustomCmd()

            if SystemManager.cpuEnable is True:
                self.cmdList["timer/hrtimer_start"] = True

                addr = SystemManager.getKerAddr('tick_sched_timer')
                if addr is not None:
                    SystemManager.writeCmd('timer/hrtimer_start/filter', cmd + " && function == 0x%s" % addr)
                SystemManager.writeCmd('timer/hrtimer_start/enable', '1')
            else:
                SystemManager.writeCmd('timer/hrtimer_start/enable', '0')
                self.cmdList["timer/hrtimer_start"] = False

            if SystemManager.memEnable is True:
                self.cmdList["kmem/mm_page_alloc"] = True
                self.cmdList["kmem/mm_page_free"] = True
                SystemManager.writeCmd('kmem/mm_page_alloc/filter', cmd)
                SystemManager.writeCmd('kmem/mm_page_free/filter', cmd)
                SystemManager.writeCmd('kmem/mm_page_alloc/enable', '1')
                SystemManager.writeCmd('kmem/mm_page_free/enable', '1')
            else:
                SystemManager.writeCmd('kmem/mm_page_alloc/enable', '0')
                SystemManager.writeCmd('kmem/mm_page_free/enable', '0')
                self.cmdList["kmem/mm_page_alloc"] = False
                self.cmdList["kmem/mm_page_free"] = False

            if SystemManager.heapEnable is True:
                mmapId = ConfigManager.getMmapId()

                self.cmdList["raw_syscalls/sys_enter"] = True
                sysEnterCmd = "(id == %s || id == %s || id == %s)" % \
                    (ConfigManager.sysList.index('sys_brk'), mmapId, \
                    ConfigManager.sysList.index('sys_munmap'))
                SystemManager.writeCmd('raw_syscalls/sys_enter/filter', sysEnterCmd)
                SystemManager.writeCmd('raw_syscalls/sys_enter/enable', '1')

                self.cmdList["raw_syscalls/sys_exit"] = True
                sysExitCmd = "(id == %s || id == %s)" % \
                    (ConfigManager.sysList.index('sys_brk'), mmapId)

                SystemManager.writeCmd('raw_syscalls/sys_exit/filter', sysExitCmd)
                SystemManager.writeCmd('raw_syscalls/sys_exit/enable', '1')
            else:
                SystemManager.writeCmd('raw_syscalls/sys_enter/enable', '0')
                SystemManager.writeCmd('raw_syscalls/sys_exit/enable', '0')
                self.cmdList["raw_syscalls/sys_enter"] = False
                self.cmdList["raw_syscalls/sys_exit"] = False

            if SystemManager.blockEnable is True:
                self.cmdList["block/block_bio_remap"] = True
                blkCmd = cmd + " && (rwbs == R || rwbs == RA || rwbs == RM)"
                SystemManager.writeCmd('block/block_bio_remap/filter', blkCmd)
                SystemManager.writeCmd('block/block_bio_remap/enable', '1')

                self.cmdList["writeback/writeback_dirty_page"] = True
                self.cmdList["writeback/wbc_writepage"] = True
                SystemManager.writeCmd('writeback/writeback_dirty_page/filter', cmd)
                SystemManager.writeCmd('writeback/writeback_dirty_page/enable', '1')
                SystemManager.writeCmd('writeback/wbc_writepage/filter', cmd)
                SystemManager.writeCmd('writeback/wbc_writepage/enable', '1')
            else:
                self.cmdList["block/block_bio_remap"] = False
                SystemManager.writeCmd('block/block_bio_remap/enable', '0')

                self.cmdList["writeback/writeback_dirty_page"] = False
                self.cmdList["writeback/wbc_writepage"] = False
                SystemManager.writeCmd('writeback/writeback_dirty_page/enable', '0')
                SystemManager.writeCmd('writeback/wbc_writepage/enable', '0')

            self.cmdList["task"] = True
            SystemManager.writeCmd('task/enable', '1')
            self.cmdList["sched/sched_process_exit"] = True
            SystemManager.writeCmd('sched/sched_process_exit/enable', '1')

            # options for segmentation fault tracing #
            sigCmd = "sig == %d" % ConfigManager.sigList.index('SIGSEGV')
            self.cmdList["signal"] = True
            SystemManager.writeCmd('signal/filter', sigCmd)
            SystemManager.writeCmd('signal/enable', '1')

            return

        # enable custom events #
        SystemManager.writeCustomCmd()

        if self.cmdList["sched/sched_switch"] is True:
            if len(SystemManager.showGroup) > 0:
                cmd = "prev_pid == 0 || next_pid == 0 || "

                for comm in SystemManager.showGroup:
                    cmd += "prev_comm == \"*%s*\" || next_comm == \"*%s*\" || " % (comm, comm)
                    cmd += "prev_pid == \"%s\" || next_pid == \"%s\" || " % (comm, comm)

                cmd = cmd[0:cmd.rfind("||")]
                SystemManager.writeCmd('sched/sched_switch/filter', cmd)
            else: SystemManager.writeCmd('sched/sched_switch/filter', '0')

            if SystemManager.writeCmd('sched/sched_switch/enable', '1') < 0:
                SystemManager.printError("sched event of ftrace is not enabled in kernel")
                sys.exit(0)

        if self.cmdList["sched/sched_wakeup"] is True:
            SystemManager.writeCmd('sched/sched_wakeup/enable', '1')

        if self.cmdList["irq"] is True:
            SystemManager.writeCmd('irq/enable', '1')

        # options for dependency tracing #
        # toDo: support sys_recv systemcall for x86, x64 #
        if SystemManager.depEnable is True and self.cmdList["raw_syscalls/sys_enter"] is True:
            cmd = "(id == %s || id == %s || id == %s || id == %s || id == %s || id == %s)" \
                % (ConfigManager.sysList.index("sys_write"), ConfigManager.sysList.index("sys_poll"), \
                ConfigManager.sysList.index("sys_epoll_wait"), ConfigManager.sysList.index("sys_select"), \
                ConfigManager.sysList.index("sys_recv"), ConfigManager.sysList.index("sys_futex"))

            SystemManager.writeCmd('raw_syscalls/sys_enter/filter', cmd)
            SystemManager.writeCmd('raw_syscalls/sys_enter/enable', '1')
        elif SystemManager.futexEnable is True:
            cmd = "(id == %s)" % (ConfigManager.sysList.index("sys_futex"))
            SystemManager.writeCmd('raw_syscalls/sys_enter/filter', cmd)
            SystemManager.writeCmd('raw_syscalls/sys_enter/enable', '1')
            self.cmdList["raw_syscalls/sys_enter"] = True
        else:
            SystemManager.writeCmd('raw_syscalls/sys_enter/filter', '0')
            SystemManager.writeCmd('raw_syscalls/sys_enter/enable', '0')

        # options for dependency tracing #
        if SystemManager.depEnable is True and self.cmdList["raw_syscalls/sys_exit"] is True:
            cmd = "((id == %s || id == %s || id == %s || id == %s || id == %s || id == %s) && ret > 0)" \
                % (ConfigManager.sysList.index("sys_write"), ConfigManager.sysList.index("sys_poll"), \
                ConfigManager.sysList.index("sys_epoll_wait"), ConfigManager.sysList.index("sys_select"), \
                ConfigManager.sysList.index("sys_recv"), ConfigManager.sysList.index("sys_futex"))

            SystemManager.writeCmd('raw_syscalls/sys_exit/filter', cmd)
            SystemManager.writeCmd('raw_syscalls/sys_exit/enable', '1')
        elif SystemManager.futexEnable is True:
            cmd = "(id == %s  && ret == 0)" % (ConfigManager.sysList.index("sys_futex"))
            SystemManager.writeCmd('raw_syscalls/sys_exit/filter', cmd)
            SystemManager.writeCmd('raw_syscalls/sys_exit/enable', '1')
            self.cmdList["raw_syscalls/sys_exit"] = True
        else:
            SystemManager.writeCmd('raw_syscalls/sys_exit/filter', '0')
            SystemManager.writeCmd('raw_syscalls/sys_exit/enable', '0')


        # options for systemcall tracing #
        if self.cmdList["raw_syscalls"] is True:
            cmd = ''

            # tid filter #
            if len(SystemManager.showGroup) > 0:
                cmd += "("
                for comm in SystemManager.showGroup:
                    cmd += "common_pid == \"%s\" || " % comm
                cmd = cmd[:cmd.rfind(" ||")] + ") && "

            # syscall filter #
            if len(SystemManager.syscallList) > 0:
                cmd += "("
                for val in SystemManager.syscallList:
                    cmd += " id == %s ||" % val
                    if SystemManager.syscallList.index(val) == len(SystemManager.syscallList) - 1:
                        cmd += " id == %s)" % val
                cmd = cmd[:cmd.rfind(" ||")] + ")"
                SystemManager.writeCmd('raw_syscalls/filter', cmd)
            else:
                cmd = cmd[:cmd.rfind(" &&")]
                SystemManager.writeCmd('raw_syscalls/filter', cmd)

            if SystemManager.sysEnable is True and \
                len(SystemManager.showGroup) == 0 and len(SystemManager.syscallList) == 0:
                SystemManager.writeCmd('raw_syscalls/filter', '0')
                SystemManager.writeCmd('raw_syscalls/sys_enter/filter', '0')
                SystemManager.writeCmd('raw_syscalls/sys_exit/filter', '0')

            SystemManager.writeCmd('raw_syscalls/enable', '1')

        # options for signal tracing #
        if self.cmdList["signal"] is True:
            if SystemManager.depEnable is True:
                SystemManager.writeCmd('signal/enable', '1')

        # options for hibernation tracing #
        if self.cmdList["power/suspend_resume"] is True:
            SystemManager.writeCmd('power/suspend_resume/enable', '1')

        # options for memory tracing #
        if self.cmdList["kmem/mm_page_alloc"] is True:
            SystemManager.writeCmd('kmem/mm_page_alloc/enable', '1')
        if self.cmdList["kmem/mm_page_free"] is True:
            SystemManager.writeCmd('kmem/mm_page_free/enable', '1')
        if self.cmdList["kmem/kmalloc"] is True:
            SystemManager.writeCmd('kmem/kmalloc/enable', '1')
        if self.cmdList["kmem/kfree"] is True:
            SystemManager.writeCmd('kmem/kfree/enable', '1')
        if self.cmdList["filemap/mm_filemap_add_to_page_cache"] is True:
            SystemManager.writeCmd('filemap/mm_filemap_add_to_page_cache/enable', '1')
        if self.cmdList["filemap/mm_filemap_delete_from_page_cache"] is True:
            SystemManager.writeCmd('filemap/mm_filemap_delete_from_page_cache/enable', '1')

        # options for block tracing #
        if self.cmdList["block/block_bio_remap"] is True:
            cmd = "rwbs == R || rwbs == RA || rwbs == RM"
            SystemManager.writeCmd('block/block_bio_remap/filter', cmd)
            SystemManager.writeCmd('block/block_bio_remap/enable', '1')
        if self.cmdList["block/block_rq_complete"] is True:
            cmd = "rwbs == R || rwbs == RA || rwbs == RM"
            SystemManager.writeCmd('block/block_rq_complete/filter', cmd)
            SystemManager.writeCmd('block/block_rq_complete/enable', '1')

        # options for write event tracing #
        if self.cmdList["writeback/writeback_dirty_page"] is True:
            SystemManager.writeCmd('writeback/writeback_dirty_page/enable', '1')
        if self.cmdList["writeback/wbc_writepage"] is True:
            SystemManager.writeCmd('writeback/wbc_writepage/enable', '1')

        # options for module event tracing #
        if self.cmdList["module/module_load"] is True:
            SystemManager.writeCmd('module/module_load/enable', '1')
        if self.cmdList["module/module_free"] is True:
            SystemManager.writeCmd('module/module_free/enable', '1')
        if self.cmdList["module/module_put"] is True:
            SystemManager.writeCmd('module/module_put/enable', '1')

        # options for power event tracing #
        if self.cmdList["power/cpu_idle"] is True:
            SystemManager.writeCmd('power/cpu_idle/enable', '1')
        if self.cmdList["power/cpu_frequency"] is True:
            SystemManager.writeCmd('power/cpu_frequency/enable', '1')

        # options for reclaim event tracing #
        if self.cmdList["vmscan/mm_vmscan_wakeup_kswapd"] is True:
            SystemManager.writeCmd('vmscan/mm_vmscan_wakeup_kswapd/enable', '1')
        if self.cmdList["vmscan/mm_vmscan_kswapd_sleep"] is True:
            SystemManager.writeCmd('vmscan/mm_vmscan_kswapd_sleep/enable', '1')

        if self.cmdList["vmscan/mm_vmscan_direct_reclaim_begin"] is True:
            SystemManager.writeCmd('vmscan/mm_vmscan_direct_reclaim_begin/enable', '1')
        if self.cmdList["vmscan/mm_vmscan_direct_reclaim_end"] is True:
            SystemManager.writeCmd('vmscan/mm_vmscan_direct_reclaim_end/enable', '1')

        # options for task event tracing #
        if self.cmdList["task"] is True:
            SystemManager.writeCmd('task/enable', '1')
        if self.cmdList["signal"] is True:
            SystemManager.writeCmd('signal/enable', '1')
        if self.cmdList["sched/sched_migrate_task"] is True:
            SystemManager.writeCmd('sched/sched_migrate_task/enable', '1')
        if self.cmdList["sched/sched_process_exit"] is True:
            SystemManager.writeCmd('sched/sched_process_exit/enable', '1')
        if self.cmdList["sched/sched_process_wait"] is True:
            SystemManager.writeCmd('sched/sched_process_wait/enable', '1')

        if self.cmdList["printk"] is True:
            SystemManager.writeCmd('printk/enable', '1')

        return



    @staticmethod
    def runRecordStopCmd():
        if SystemManager.isRecordMode() is True and \
            (SystemManager.isThreadMode() is True or SystemManager.isFunctionMode() is True):
            # disable all ftrace options registered #
            for idx, val in SystemManager.cmdList.items():
                if val is True or val is not False:
                    SystemManager.writeCmd(str(idx) + '/enable', '0')
                    SystemManager.writeCmd(str(idx) + '/filter', '0')

            if SystemManager.customCmd is not None:
                for cmd in SystemManager.customCmd:
                    event = cmd.split(':')[0]
                    SystemManager.writeCmd(event + '/enable', '0')
                    SystemManager.writeCmd(event + '/filter', '0')

            if SystemManager.isFunctionMode() is True:
                SystemManager.writeCmd('../options/stacktrace', '0')
                SystemManager.writeCmd('../trace_options', 'nouserstacktrace')



    def printAllInfoToBuf(self):
        self.printSystemInfo()
        self.printWebOSInfo()
        self.printCpuInfo()
        self.printMemInfo()
        self.printDiskInfo()



    def printWebOSInfo(self):
        if self.osData is None and self.devData is None:
            return

        SystemManager.infoBufferPrint('\n[System OS Info]')
        SystemManager.infoBufferPrint(twoLine)
        SystemManager.infoBufferPrint("{0:^35} {1:100}".format("TYPE", "Information"))
        SystemManager.infoBufferPrint(oneLine)

        for val in self.osData:
            try:
                val = val.split(':')
                if len(val) < 2:
                    continue
                name = val[0].replace('"', '')
                value = val[1].replace('"', '').replace('\n', '').replace(',', '')
                SystemManager.infoBufferPrint("{0:35} {1:<100}".format(name, value))
            except:
                SystemManager.printWarning("Fail to parse osData")

        for val in self.devData:
            try:
                val = val.split(':')
                if len(val) < 2:
                    continue
                name = val[0].replace('"', '')
                value = val[1].replace('"', '').replace('\n', '').replace(',', '')
                SystemManager.infoBufferPrint("{0:35} {1:<100}".format(name, value))
            except:
                SystemManager.printWarning("Fail to parse devData")

        SystemManager.infoBufferPrint(twoLine)



    def printSystemInfo(self):
        SystemManager.infoBufferPrint('\n[System General Info]')
        SystemManager.infoBufferPrint(twoLine)
        SystemManager.infoBufferPrint("{0:^20} {1:100}".format("TYPE", "Information"))
        SystemManager.infoBufferPrint(oneLine)

        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Launch', '# ' + ' '.join(sys.argv)))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Time', self.SystemManager['date'] + ' ' + self.SystemManager['time']))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".format('OS', self.SystemManager['osVer']))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Kernel', self.SystemManager['osType'] + ' ' + self.SystemManager['kernelVer']))
        except:
            pass
        try:
            RunningMin = int(float(self.uptimeData[0])) / 60
            RunningHour = RunningMin / 60
            if RunningHour > 0:
                RunningMin %= 60
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('RunningTime', str(RunningHour) + ' hour  ' + str(RunningMin) + ' min'))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<10}\t/\t{2:<10}\t/\t{3:<10}".format('Load', \
                str(int(float(self.loadData[0]) * 100)) + '% (1 min)', \
                str(int(float(self.loadData[1]) * 100)) + '% (5 min)', \
                str(int(float(self.loadData[2]) * 100)) + '% (15 min)'))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<10}".format('Threads', \
                self.loadData[3] + ' (running/total)'))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<10}".format('LastPid', self.loadData[4]))
        except:
            pass
        try:
            title = 'Cmdline'
            splitLen = SystemManager.lineLength - 21
            cmdlineList = [self.cmdlineData[i:i+splitLen] for i in range(0, len(self.cmdlineData), splitLen)]
            for string in cmdlineList:
                SystemManager.infoBufferPrint("{0:20} {1:<100}".format(title, string))
                title = ''
        except:
            pass

        SystemManager.infoBufferPrint(twoLine)

    def printCpuInfo(self):
        # parse data #
        if self.cpuData is not None:
            for l in self.cpuData:
                m = re.match(r'(?P<type>.*):\s+(?P<val>.*)', l)
                if m is not None:
                    d = m.groupdict()
                    self.cpuInfo[d['type'][0:len(d['type'])-1]] = d['val']
        else:
            return

        SystemManager.infoBufferPrint('\n[System CPU Info]')
        SystemManager.infoBufferPrint(twoLine)
        SystemManager.infoBufferPrint("{0:^20} {1:100}".format("TYPE", "Information"))
        SystemManager.infoBufferPrint(oneLine)

        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Physical', int(self.cpuInfo['physical id']) + 1))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('CoresPerCPU', self.cpuInfo['cpu cores']))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Logical', int(self.cpuInfo['processor']) + 1))
        except:
            pass

        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Vendor', self.cpuInfo['vendor_id']))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Model', self.cpuInfo['model name']))
        except:
            pass

        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Cache(L2)', self.cpuInfo['cache size']))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Perf', self.cpuInfo['bogomips']))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Address', self.cpuInfo['address sizes']))
        except:
            pass

        SystemManager.infoBufferPrint(twoLine)



    def printDiskInfo(self):
        # parse data #
        if self.diskBeforeData is not None or self.diskAfterData is not None:
            time = 'before'
            for l in self.diskBeforeData:
                major, minor, name, readComplete, readMerge, sectorRead, readTime, \
                writeComplete, writeMerge, sectorWrite, writeTime, currentIO, ioTime, ioWTime = \
                l.split()

                name = '/dev/' + name
                self.diskInfo[time][name] = dict()
                diskInfoBuf = self.diskInfo[time][name]
                diskInfoBuf['major'] = major
                diskInfoBuf['minor'] = minor
                diskInfoBuf['readComplete'] = readComplete
                diskInfoBuf['readTime'] = readTime
                diskInfoBuf['writeComplete'] = writeComplete
                diskInfoBuf['writeTime'] = writeTime
                diskInfoBuf['currentIO'] = currentIO
                diskInfoBuf['ioTime'] = ioTime

            time = 'after'
            for l in self.diskAfterData:
                major, minor, name, readComplete, readMerge, sectorRead, readTime, \
                writeComplete, writeMerge, sectorWrite, writeTime, currentIO, ioTime, ioWTime = \
                l.split()

                name = '/dev/' + name
                self.diskInfo[time][name] = dict()
                diskInfoBuf = self.diskInfo[time][name]
                diskInfoBuf['major'] = major
                diskInfoBuf['minor'] = minor
                diskInfoBuf['readComplete'] = readComplete
                diskInfoBuf['readTime'] = readTime
                diskInfoBuf['writeComplete'] = writeComplete
                diskInfoBuf['writeTime'] = writeTime
                diskInfoBuf['currentIO'] = currentIO
                diskInfoBuf['ioTime'] = ioTime
        else:
            return

        if self.mountData is not None:
            for l in self.mountData:
                dev, path, fs, option, etc1, etc2 = l.split()

                self.mountInfo[dev] = dict()
                mountInfoBuf = self.mountInfo[dev]
                mountInfoBuf['path'] = path
                mountInfoBuf['fs'] = fs
                mountInfoBuf['option'] = option
        else:
            return

        # print disk info #
        SystemManager.infoBufferPrint('\n[System Disk Info] [ Unit: ms/KB ]')
        SystemManager.infoBufferPrint(twoLine)
        SystemManager.infoBufferPrint("%16s %10s %10s %10s %10s %10s %10s %10s %20s" % \
            ("Dev", "Major", "Minor", "ReadSize", "ReadTime", "writeSize", "writeTime", \
            "FileSystem", "MountPoint <Option>"))
        SystemManager.infoBufferPrint(oneLine)

        outputCnt = 0

        for key, val in self.mountInfo.items():
            try:
                beforeInfo = self.diskInfo['before'][key]
                afterInfo = self.diskInfo['after'][key]
                outputCnt += 1
            except:
                continue

            SystemManager.infoBufferPrint("%16s %10s %10s %10s %10s %10s %10s %10s %20s" % \
                (key, afterInfo['major'], afterInfo['minor'], \
                (int(afterInfo['readComplete']) - int(beforeInfo['readComplete'])) * 4, \
                (int(afterInfo['readTime']) - int(beforeInfo['readTime'])), \
                (int(afterInfo['writeComplete']) - int(beforeInfo['writeComplete'])) * 4, \
                (int(afterInfo['writeTime']) - int(beforeInfo['writeTime'])), \
                val['fs'], val['path'] + ' <' + val['option'] + '>'))

        if outputCnt == 0:
            SystemManager.infoBufferPrint('N/A')
        SystemManager.infoBufferPrint(twoLine + '\n\n')



    def printMemInfo(self):
        # parse data #
        if self.memBeforeData is not None or self.memAfterData is not None:
            time = 'before'
            for l in self.memBeforeData:
                m = re.match(r'(?P<type>\S+):\s+(?P<size>[0-9]+)', l)
                if m is not None:
                    d = m.groupdict()
                    self.memInfo[time][d['type']] = d['size']

            time = 'after'
            for l in self.memAfterData:
                m = re.match(r'(?P<type>\S+):\s+(?P<size>[0-9]+)', l)
                if m is not None:
                    d = m.groupdict()
                    self.memInfo[time][d['type']] = d['size']
        else:
            return

        beforeInfo = self.memInfo['before']
        afterInfo = self.memInfo['after']

        # check items for compatibility #
        try:
            beforeInfo['Shmem']
        except:
            beforeInfo['Shmem'] = '0'
            afterInfo['Shmem'] = '0'
        try:
            beforeInfo['SReclaimable']
        except:
            beforeInfo['SReclaimable'] = '0'
            afterInfo['SReclaimable'] = '0'
        try:
            beforeInfo['Sunreclaim']
        except:
            beforeInfo['Sunreclaim'] = '0'
            afterInfo['Sunreclaim'] = '0'
        try:
            beforeInfo['Mlocked']
        except:
            beforeInfo['Mlocked'] = '0'
            afterInfo['Mlocked'] = '0'

        # print memory info #
        SystemManager.infoBufferPrint('\n[System Memory Info] [ Unit: MB ]')
        SystemManager.infoBufferPrint(twoLine)
        SystemManager.infoBufferPrint(\
            "[%6s] %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s" % \
            ("DESC", "Memory", "Swap", "Buffer", "Cache", "Shared", "Mapped", \
            "Active", "Inactive", "PageTables", "Slab", "SReclaimable", "SUnreclaim", "Mlocked"))
        SystemManager.infoBufferPrint(oneLine)
        SystemManager.infoBufferPrint("[ TOTAL] %10s %10s" % \
            (int(beforeInfo['MemTotal']) / 1024, int(beforeInfo['SwapTotal']) / 1024))
        SystemManager.infoBufferPrint("[  FREE] %10s %10s" % \
            (int(beforeInfo['MemFree']) / 1024, int(beforeInfo['SwapFree']) / 1024))

        memBeforeUsage = int(beforeInfo['MemTotal']) - int(beforeInfo['MemFree'])
        swapBeforeUsage = int(beforeInfo['SwapTotal']) - int(beforeInfo['SwapFree'])
        memAfterUsage = int(afterInfo['MemTotal']) - int(afterInfo['MemFree'])
        swapAfterUsage = int(afterInfo['SwapTotal']) - int(afterInfo['SwapFree'])

        SystemManager.infoBufferPrint(\
            "[USAGE1] %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s" % \
                (memBeforeUsage / 1024, swapBeforeUsage / 1024, \
                int(beforeInfo['Buffers']) / 1024, int(beforeInfo['Cached']) / 1024, \
                int(beforeInfo['Shmem']) / 1024, int(beforeInfo['Mapped']) / 1024, \
                int(beforeInfo['Active']) / 1024, int(beforeInfo['Inactive']) / 1024, \
                int(beforeInfo['PageTables']) / 1024, int(beforeInfo['Slab']) / 1024, \
                int(beforeInfo['SReclaimable']) / 1024, int(beforeInfo['SUnreclaim']) / 1024, \
                int(beforeInfo['Mlocked']) / 1024))

        SystemManager.infoBufferPrint(\
            "[USAGE2] %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s" % \
                (memAfterUsage / 1024, swapAfterUsage / 1024, \
                int(afterInfo['Buffers']) / 1024, int(afterInfo['Cached']) / 1024, \
                int(afterInfo['Shmem']) / 1024, int(afterInfo['Mapped']) / 1024, \
                int(afterInfo['Active']) / 1024, int(afterInfo['Inactive']) / 1024, \
                int(afterInfo['PageTables']) / 1024, int(afterInfo['Slab']) / 1024, \
                int(afterInfo['SReclaimable']) / 1024, int(afterInfo['SUnreclaim']) / 1024, \
                int(afterInfo['Mlocked']) / 1024))

        SystemManager.infoBufferPrint(\
            "[  DIFF] %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s" % \
                (memAfterUsage / 1024 - memBeforeUsage / 1024, \
                swapAfterUsage / 1024 - swapBeforeUsage / 1024, \
                int(afterInfo['Buffers']) / 1024 - int(beforeInfo['Buffers']) / 1024, \
                int(afterInfo['Cached']) / 1024 - int(beforeInfo['Cached']) / 1024, \
                int(afterInfo['Shmem']) / 1024 - int(beforeInfo['Shmem']) / 1024, \
                int(afterInfo['Mapped']) / 1024 - int(beforeInfo['Mapped']) / 1024, \
                int(afterInfo['Active']) / 1024 - int(beforeInfo['Active']) / 1024, \
                int(afterInfo['Inactive']) / 1024 - int(beforeInfo['Inactive']) / 1024, \
                int(afterInfo['PageTables']) / 1024 - int(beforeInfo['PageTables']) / 1024, \
                int(afterInfo['Slab']) / 1024 - int(beforeInfo['Slab']) / 1024, \
                int(afterInfo['SReclaimable']) / 1024 - int(beforeInfo['SReclaimable']) / 1024, \
                int(afterInfo['SUnreclaim']) / 1024 - int(beforeInfo['SUnreclaim']) / 1024, \
                int(afterInfo['Mlocked']) / 1024 - int(beforeInfo['Mlocked']) / 1024))

        SystemManager.infoBufferPrint(twoLine)





class EventAnalyzer(object):
    """ Analyzer for event profiling """

    def __init__(self):
        self.eventData = {}



    def __del__(self):
        pass



    def addEvent(self, time, event):
        # ramdom event #
        if len(event.split('_')) == 1:
            name = event
            ID = None
        # sequantial event #
        else:
            name = event.split('_')[0]
            ID = event.split('_')[1]

        try:
            self.eventData[name]
            # {'list': [ID, time, number], 'summary': [ID, cnt, avr, min, max, first, last]} #
        except:
            self.eventData[name] = {'list': [], 'summary': []}

        self.eventData[name]['list'].append(\
            [ID, time, sum(t[0] == ID for t in self.eventData[name]['list']) + 1])

        if sum(id[0] == ID for id in self.eventData[name]['summary']) == 0:
            self.eventData[name]['summary'].append([ID, 1, 0, 0, 0, time, 0])
        else:
            for n in self.eventData[name]['summary']:
                if n[0] == ID:
                    n[1] += 1
                    n[6] = time
                    break



    def printEventInfo(self):
        if len(self.eventData) > 0:
            SystemManager.pipePrint('\n\n\n' + twoLine)
            SystemManager.pipePrint("%s# %s: %d\n" % ('', 'EVT', len(self.eventData)))
            self.printEvent(ti.startTime)
            SystemManager.pipePrint(twoLine)



    def printEvent(self, startTime):
        for key, value in sorted(self.eventData.items(), key=lambda e: e[1], reverse=True):
            if self.eventData[key]['summary'][0][0] == None:
                SystemManager.pipePrint("%10s: [total: %s]" % (key, len(self.eventData[key]['list'])))
            else:
                string = ''
                for n in sorted(self.eventData[key]['summary'], key=lambda slist: slist[0]):
                    string += '[%s: %d/%d/%d/%d/%.3f/%.3f] ' % \
                        (n[0], n[1], n[2], n[3], n[4], float(n[5]) - float(startTime), 0)
                SystemManager.pipePrint("%10s: [total: %s] [subEvent: %s] %s" % \
                        (key, len(self.eventData[key]['list']), len(self.eventData[key]['summary']), string))




class ThreadAnalyzer(object):
    """ Analyzer for thread profiling """

    def __init__(self, file):
        self.threadData = {}
        self.irqData = {}
        self.ioData = {}
        self.reclaimData = {}
        self.pageTable = {}
        self.kmemTable = {}
        self.moduleData = []
        self.intervalData = []
        self.depData = []
        self.sigData = []
        self.syscallData = []
        self.lastJob = {}
        self.preemptData = []
        self.suspendData = []
        self.markData = []
        self.consoleData = []

        self.procData = {}
        self.prevProcData = {}
        self.cpuData = {}
        self.prevCpuData = {}
        self.vmData = {}
        self.prevVmData = {}
        self.systemData = {}

        self.stopFlag = False
        self.totalTime = 0
        self.totalTimeOld = 0
        self.cxtSwitch = 0
        self.nrNewTask = 0
        self.thisInterval = 0

        self.threadDataOld = {}
        self.irqDataOld = {}
        self.ioDataOld = {}
        self.reclaimDataOld = {}

        self.init_threadData = {'comm': '', 'usage': float(0), 'cpuRank': int(0), 'yield': int(0), \
            'cpuWait': float(0), 'pri': '0', 'ioWait': float(0), 'reqBlock': int(0), 'readBlock': int(0), \
            'ioRank': int(0), 'irq': float(0), 'reclaimWait': float(0), 'reclaimCnt': int(0), \
            'ptid': '0', 'new': ' ', 'die': ' ', 'preempted': int(0), 'preemption': int(0), \
            'start': float(0), 'stop': float(0), 'readQueueCnt': int(0), 'readStart': float(0), \
            'maxRuntime': float(0), 'coreSchedCnt': int(0), 'migrate': int(0), 'longRunCore': int(-1), \
            'dReclaimWait': float(0), 'dReclaimStart': float(0), 'dReclaimCnt': int(0), \
            'futexCnt': int(0), 'futexEnter': float(0), 'futexTotal': float(0), 'futexMax': float(0), \
            'lastStatus': 'N', 'offCnt': int(0), 'offTime': float(0), 'lastOff': float(0), \
            'nrPages': int(0), 'reclaimedPages': int(0), 'remainKmem': int(0), 'wasteKmem': int(0), \
            'kernelPages': int(0), 'childList': None, 'readBlockCnt': int(0), 'writeBlock': int(0), \
            'writeBlockCnt': int(0), 'cachePages': int(0), 'userPages': int(0), \
            'maxPreempted': float(0), 'anonReclaimedPages': int(0), 'lastIdleStatus': int(0), \
            'createdTime': float(0), 'waitStartAsParent': float(0), 'waitChild': float(0), \
            'waitParent': float(0), 'waitPid': int(0), 'tgid': '-'*5}

        self.init_irqData = {'name': '', 'usage': float(0), 'start': float(0), 'max': float(0), \
            'min': float(0), 'max_period': float(0), 'min_period': float(0), 'count': int(0)}

        self.init_intervalData = {'time': float(0), 'firstLogTime': float(0), 'cpuUsage': float(0), \
            'totalUsage': float(0), 'cpuPer': float(0), 'totalMemUsage': float(0), \
            'ioUsage': float(0), 'totalIoUsage': float(0), 'irqUsage': float(0), 'memUsage': float(0), \
            'kmemUsage': float(0), 'totalKmemUsage': float(0), 'coreSchedCnt': int(0), \
            'totalCoreSchedCnt': int(0), 'preempted': float(0), \
            'totalPreempted': float(0), 'new': ' ', 'die': ' '}

        self.init_kmallocData = {'tid': '0', 'caller': '0', 'ptr': '0', 'req': int(0), 'alloc': int(0), \
            'time': '0', 'waste': int(0), 'core': int(0)}

        self.wakeupData = {'tid': '0', 'nr': '0', 'ret': '0', 'time': '0', 'args': '0', \
            'valid': int(0), 'from': '0', 'to': '0', 'corrupt': '0'}

        self.init_syscallInfo = {'usage': float(0), 'last': float(0), 'count': int(0), \
            'max': float(0), 'min': float(0)}

        self.init_procData = {'comm': '', 'isMain': bool(False), 'tids': None, 'stat': None, \
            'io': None, 'alive': False, 'statFd': None, 'runtime': float(0), \
            'new': bool(False), 'minflt': long(0), 'majflt': long(0), 'ttime': float(0), \
            'utime': float(0), 'stime': float(0), 'ioFd': None, 'taskPath': None, \
            'mainID': int(0), 'btime': float(0), 'read': long(0), 'write': long(0), \
            'cutime': float(0), 'cstime': float(0), 'cttime': float(0), 'statusFd': None, 'status': None}

        self.init_cpuData = {'user': long(0), 'system': long(0), 'nice': long(0), 'idle': long(0), \
            'wait': long(0), 'irq': long(0), 'softirq': long(0)}

        self.init_pageData = {'tid': '0', 'page': '0', 'flags': '0', 'type': '0', 'time': '0'}
        self.init_lastJob = {'job': '0', 'time': '0', 'tid': '0', 'prevWakeupTid': '0'}
        self.init_preemptData = {'usage': float(0), 'count': int(0), 'max': float(0)}

        self.startTime = '0'
        self.finishTime = '0'
        self.lastTidPerCore = {}
        self.lastCore = '0'
        self.lastEvent = '0'

        # top mode #
        if file is None:
            # set index of attributes #
            self.minfltIdx = ConfigManager.statList.index("MINFLT")
            self.majfltIdx = ConfigManager.statList.index("MAJFLT")
            self.utimeIdx = ConfigManager.statList.index("UTIME")
            self.stimeIdx = ConfigManager.statList.index("STIME")
            self.cutimeIdx = ConfigManager.statList.index("CUTIME")
            self.cstimeIdx = ConfigManager.statList.index("CSTIME")
            self.btimeIdx = ConfigManager.statList.index("DELAYBLKTICK")
            self.commIdx = ConfigManager.statList.index("COMM")
            self.ppidIdx = ConfigManager.statList.index("PPID")
            self.nrthreadIdx = ConfigManager.statList.index("NRTHREAD")
            self.prioIdx = ConfigManager.statList.index("PRIORITY")
            self.policyIdx = ConfigManager.statList.index("POLICY")
            self.vsizeIdx = ConfigManager.statList.index("VSIZE")
            self.rssIdx = ConfigManager.statList.index("RSS")
            self.sstackIdx = ConfigManager.statList.index("STARTSTACK")
            self.estackIdx = ConfigManager.statList.index("SP")
            self.scodeIdx = ConfigManager.statList.index("STARTCODE")
            self.ecodeIdx = ConfigManager.statList.index("ENDCODE")
            self.statIdx = ConfigManager.statList.index("STATE")
            self.coreIdx = ConfigManager.statList.index("PROCESSOR")
            self.runtimeIdx = ConfigManager.statList.index("STARTTIME")

            try:
                import resource
                SystemManager.maxFd = resource.getrlimit(getattr(resource, 'RLIMIT_NOFILE'))[0]
            except:
                SystemManager.printWarning(\
                    "Fail to get maxFd because of no resource package, default %d" % SystemManager.maxFd)

            # set default interval #
            if SystemManager.intervalEnable == 0:
                SystemManager.intervalEnable = 1

            if len(SystemManager.showGroup) > 0:
                for idx, val in enumerate(SystemManager.showGroup):
                    if len(val) == 0:
                        SystemManager.showGroup.pop(idx)

            if SystemManager.printFile is not None:
                SystemManager.printStatus(r"start profiling... [ STOP(ctrl + c), SAVE(ctrl + \) ]")

            while True:
                # collect stats of process as soon as possible #
                self.saveProcs()

                if self.prevProcData != {}:
                    if SystemManager.printFile is None:
                        SystemManager.printTitle()

                    self.printTopUsage()

                time.sleep(SystemManager.intervalEnable)

                self.prevProcData = self.procData
                self.procData = {}

            sys.exit(0)

        # initialize preempt thread list #
        if SystemManager.preemptGroup != None:
            for index in SystemManager.preemptGroup:
                # preempted state [preemptBit, threadList, startTime, core, totalUsage] #
                self.preemptData.append([False, {}, float(0), 0, float(0)])

        try:
            f = open(file, 'r')
            lines = f.readlines()
        except IOError:
            SystemManager.printError("Open %s" % file)
            sys.exit(0)

        # save data and exit if output file is set #
        SystemManager.saveDataAndExit(lines)

        # start parsing logs #
        SystemManager.printStatus('start analyzing... [ STOP(ctrl + c) ]')
        SystemManager.totalLine = len(lines)

        for idx, log in enumerate(lines):
            self.parse(log)
            SystemManager.printProgress(SystemManager.curLine, SystemManager.totalLine)

            # save last job per core #
            try:
                self.lastJob[self.lastCore]
            except:
                self.lastJob[self.lastCore] = dict(self.init_lastJob)

            self.lastJob[self.lastCore]['job'] = self.lastEvent
            self.lastJob[self.lastCore]['time'] = self.finishTime

            if self.stopFlag is True:
                break

        # add comsumed time of jobs not finished yet to each threads #
        for idx, val in self.lastTidPerCore.items():
            self.threadData[val]['usage'] += (float(self.finishTime) - float(self.threadData[val]['start']))
            # toDo: add blocking time to read blocks from disk #

        f.close()

        if len(self.threadData) == 0:
            SystemManager.printError("No recognized data in %s" % SystemManager.inputFile)
            sys.exit(0)

        self.totalTime = round(float(self.finishTime) - float(self.startTime), 7)

        # group filter #
        if len(SystemManager.showGroup) > 0:
            for key, value in sorted(self.threadData.items(), key=lambda e: e[1], reverse=False):
                checkResult = False
                for val in SystemManager.showGroup:
                    if value['comm'].rfind(val) > -1 or value['tgid'].rfind(val) > -1 or key == val:
                        checkResult = True
                if checkResult == False and key[0:2] != '0[':
                    try:
                        del self.threadData[key]
                    except:
                        continue
        elif SystemManager.sysEnable is True or len(SystemManager.syscallList) > 0:
            SystemManager.printWarning("-g option is not enabled, -t option is disabled")
            SystemManager.sysEnable = False
            SystemManager.syscallList = []

        # print thread usage #
        self.printUsage()

        # print resource usage of threads on timeline #
        if SystemManager.intervalEnable > 0:
            self.printIntervalInfo()

        # print module information #
        if len(self.moduleData) > 0:
            self.printModuleInfo()

        # print dependency of threads #
        if SystemManager.depEnable is True:
            self.printDepInfo()

        # print kernel messages #
        self.printConsoleInfo()

        # print system call usage #
        self.printSyscallInfo()



    def __del__(self):
        pass



    def makeTaskChain(self):
        if ConfigManager.taskChainEnable != True:
            return

        while True:
            eventInput = raw_input('Input event name for taskchain: ')
            fd = ConfigManager.openConfFile(eventInput)
            if fd != None:
                break

        ConfigManager.writeConfData(fd, '[%s]\n' % (eventInput))
        threadInput = raw_input('Input tids of hot threads for taskchain (ex. 13,144,235): ')
        threadList = threadInput.split(',')
        ConfigManager.writeConfData(fd, 'nr_tid=' + str(len(threadList)) + '\n')

        for index, t in enumerate(threadList):
            cmdline = ConfigManager.readProcData(t, 'cmdline', 0)
            if cmdline == None:
                continue

            cmdline = cmdline[0:cmdline.find('\x00')]
            cmdline = cmdline[0:cmdline.rfind('/')]
            cmdline = cmdline.replace(' ', '-')
            if len(cmdline) > 256:
                cmdline = cmdline[0:255]

            try:
                self.threadData[t]
            except:
                SystemManager.printWarning("thread %s is not in profiled data" % t)
                continue

            ConfigManager.writeConfData(\
                fd, str(index) + '=' + ConfigManager.readProcData(t, 'stat', 2).replace('\x00', '-')\
                + '+' + cmdline + ' ' + str(self.threadData[t]['ioRank']) + ' ' + \
                str(self.threadData[t]['reqBlock']) + ' ' + \
                str(self.threadData[t]['cpuRank']) + ' ' + \
                str(self.threadData[t]['usage']) + '\n')

        SystemManager.pipePrint("%s.tc is written successfully" % eventInput)



    def getRunTaskNum(self):
        return len(self.threadData)



    def printCreationTree(self, tid, loc):
        childList = self.threadData[tid]['childList']
        threadName = "%s(%s)" % (self.threadData[tid]['comm'], tid)

        if self.threadData[tid]['createdTime'] > 0:
            threadName += " /%2.3f/" % (self.threadData[tid]['createdTime'] - float(self.startTime))
        if self.threadData[tid]['usage'] > 0:
            threadName += " <%2.3f>" % (self.threadData[tid]['usage'])
        if self.threadData[tid]['childList'] is not None:
            threadName += " |%d|" % (len(self.threadData[tid]['childList']))
        if self.threadData[tid]['waitChild'] > 0:
            threadName += " {%1.3f}" % (self.threadData[tid]['waitChild'])
        if self.threadData[tid]['waitParent'] > 0:
            threadName += " [%1.3f]" % (self.threadData[tid]['waitParent'])

        # set new position of line #
        newLoc = loc + 5

        if self.threadData[tid]['die'] == ' ':
            life = '+ '
        else:
            life = '- '

        SystemManager.pipePrint(' ' * loc + life + threadName)

        if childList != None:
            for thread in childList:
                self.printCreationTree(thread, newLoc)



    def printUsage(self):
        # print title #
        SystemManager.printTitle()

        # print system information #
        SystemManager.printInfoBuffer()

        # print menu #
        SystemManager.pipePrint(("[%s] [ %s: %0.3f ] [ Running: %d ] [ CtxSwc: %d ] " + \
            "[ LogSize: %d KB ] [ Keys: Foward/Back/Save/Quit ] [ Unit: Sec/MB ]") % \
            ('Thread Info', 'Elapsed time', round(float(self.totalTime), 7), \
            self.getRunTaskNum(), self.cxtSwitch, SystemManager.logSize / 1024))
        SystemManager.pipePrint(twoLine)

        SystemManager.pipePrint("{0:_^32}|{1:_^35}|{2:_^22}|{3:_^26}|{4:_^34}|".\
            format("Thread Info", "CPU Info", "SCHED Info", "BLOCK Info", "MEM Info"))
        SystemManager.pipePrint("{0:^32}|{1:^35}|{2:^22}|{3:^26}|{4:^34}|".\
            format("", "", "", "", "", ""))

        SystemManager.pipePrint(("%16s(%5s/%5s)|%2s|%5s(%5s)|%5s(%5s)|%3s|%5s|" + \
            "%5s|%5s|%5s|%4s|%5s(%3s/%5s)|%4s(%3s)|%4s(%3s|%3s|%3s)|%3s|%3s|%4s(%2s)|") % \
            ('Name', 'Tid', 'Pid', 'LF', 'Usage', '%', 'Delay', 'Max', 'Pri', ' IRQ ', \
            'Yld', ' Lose', 'Steal', 'Mig', 'Read', 'MB', 'Cnt', 'WCnt', 'MB', \
            'Sum', 'Usr', 'Buf', 'Ker', 'Rcl', 'Wst', 'DRcl', 'Nr'))
        SystemManager.pipePrint(twoLine)

        # initialize swapper thread per core #
        for n in range(0, SystemManager.maxCore + 1):
            try:
                self.threadData['0[' + str(n) + ']']
            except:
                self.threadData['0[' + str(n) + ']'] = dict(self.init_threadData)
                self.threadData['0[' + str(n) + ']']['comm'] = 'swapper/' + str(n)
                self.threadData['0[' + str(n) + ']']['usage'] = 0

        # sort by size of io usage and convert read blocks to MB size #
        count = 0
        for key, value in sorted(self.threadData.items(), key=lambda e: e[1]['readBlock'], reverse=True):
            value['ioRank'] = count + 1
            if value['readBlock'] > 0:
                value['readBlock'] = value['readBlock'] * SystemManager.blockSize / 1024 / 1024
                count += 1
            if value['writeBlock'] > 0:
                value['writeBlock'] = value['writeBlock'] * SystemManager.pageSize / 1024 / 1024

       # print total information after sorting by time of cpu usage #
        count = 0
        SystemManager.clearPrint()
        for key, value in sorted(self.threadData.items(), key=lambda e: e[1]['comm'], reverse=False):
            if key[0:2] == '0[':
                # change the name of swapper thread to CORE #
                value['comm'] = value['comm'].replace("swapper", "CORE")

                # modify idle time if this core is not woke up #
                if value['usage'] == 0 and value['coreSchedCnt'] == 0:
                    value['usage'] = self.totalTime

                # calculate total core usage percentage #
                usagePercent = 100 - (round(float(value['usage']) / float(self.totalTime), 7) * 100)
                if value['lastOff'] > 0:
                    value['offTime'] += float(self.finishTime) - value['lastOff']

                SystemManager.addPrint(\
                    ("%16s(%5s/%5s)|%s%s|%5.2f(%5s)|%5.2f(%5.2f)|%3s|%5.2f|" + \
                    "%5d|%5s|%5s|%4s|%5.2f(%3d/%5d)|%4s(%3s)|%4s(%3s|%3s|%3s)|%3s|%3s|%4.2f(%2d)|\n") \
                        % (value['comm'], '0', '0', '-', '-', \
                        self.totalTime - value['usage'], str(round(float(usagePercent), 1)), \
                        round(float(value['offTime']), 7), 0, 0, value['irq'], \
                        value['offCnt'], '-', '-', '-', \
                        value['ioWait'], value['readBlock'], value['readBlockCnt'], value['writeBlockCnt'], \
                        value['writeBlock'], (value['nrPages'] * 4 / 1024) + (value['remainKmem'] / 1024 / 1024), \
                        value['userPages'] * 4 / 1024, value['cachePages'] * 4 / 1024, \
                        value['kernelPages'] * 4 / 1024 + (value['remainKmem'] / 1024 / 1024), \
                        (value['reclaimedPages'] * 4 / 1024), value['wasteKmem'] / 1024 / 1024, \
                        value['dReclaimWait'], value['dReclaimCnt']))
                count += 1
            else:
                # convert priority #
                prio = int(value['pri']) - 120
                if prio >= -20:
                    value['pri'] = str(prio)
                else:
                    value['pri'] = 'R%2s' % abs(prio + 21)

        SystemManager.pipePrint("%s# %s: %d\n" % ('', 'CPU', count))
        SystemManager.pipePrint(SystemManager.bufferString)
        SystemManager.pipePrint(oneLine)

        # set sort value #
        if SystemManager.sort == 'm':
            sortedThreadData = sorted(self.threadData.items(), \
                key=lambda e: e[1]['nrPages'], reverse=True)
        elif SystemManager.sort == 'b':
            sortedThreadData = sorted(self.threadData.items(), \
                key=lambda e: e[1]['readBlock'], reverse=True)
        else:
            # set cpu usage as default #
            sortedThreadData = sorted(self.threadData.items(), \
                key=lambda e: e[1]['usage'], reverse=True)

        # print thread information after sorting by time of cpu usage #
        count = 0
        SystemManager.clearPrint()
        for key, value in sortedThreadData:
            if key[0:2] == '0[':
                continue

            usagePercent = round(float(value['usage']) / float(self.totalTime), 7) * 100

            # set break condition #
            if SystemManager.sort == 'm':
                breakCond = value['nrPages']
            elif SystemManager.sort == 'b':
                breakCond = value['readBlock']
            else:
                breakCond = usagePercent
                value['cpuRank'] = count + 1
                count += 1

            if breakCond < 1 and SystemManager.showAll is False and SystemManager.showGroup == []:
                break

            SystemManager.addPrint(\
                ("%16s(%5s/%5s)|%s%s|%5.2f(%5s)|%5.2f(%5.2f)|%3s|%5.2f|" + \
                "%5d|%5s|%5s|%4s|%5.2f(%3d/%5d)|%4s(%3s)|%4d(%3d|%3d|%3d)|%3d|%3d|%4.2f(%2d)|\n") % \
                (value['comm'], key, value['tgid'], value['new'], value['die'], value['usage'], \
                str(round(float(usagePercent), 1)), value['cpuWait'], value['maxPreempted'], \
                value['pri'], value['irq'], value['yield'], value['preempted'], value['preemption'], \
                value['migrate'], value['ioWait'], value['readBlock'], value['readBlockCnt'], \
                value['writeBlockCnt'], value['writeBlock'], \
                (value['nrPages'] * 4 / 1024) + (value['remainKmem'] / 1024 / 1024), \
                value['userPages'] * 4 / 1024, value['cachePages'] * 4 / 1024, \
                value['kernelPages'] * 4 / 1024 + (value['remainKmem'] / 1024 / 1024), \
                value['reclaimedPages'] * 4 / 1024, value['wasteKmem'] / 1024 / 1024, \
                value['dReclaimWait'], value['dReclaimCnt']))

        SystemManager.pipePrint("%s# %s: %d\n" % ('', 'Hot', count))
        SystemManager.pipePrint(SystemManager.bufferString)
        SystemManager.pipePrint(oneLine)

        # print thread preempted information after sorting by time of cpu usage #
        for val in SystemManager.preemptGroup:
            index = SystemManager.preemptGroup.index(val)
            count = 0

            tid = SystemManager.preemptGroup[index]
            try:
                self.threadData[tid]
            except:
                SystemManager.printError("Fail to find \"%s\" thread" % tid)
                continue

            SystemManager.clearPrint()
            for key, value in sorted(self.preemptData[index][1].items(), key=lambda e: e[1]['usage'], reverse=True):
                count += 1
                if float(self.preemptData[index][4]) == 0:
                    break
                SystemManager.addPrint("%16s(%5s/%5s)|%s%s|%5.2f(%5s)\n" \
                    % (self.threadData[key]['comm'], key, '0', self.threadData[key]['new'], \
                    self.threadData[key]['die'], value['usage'], \
                    str(round(float(value['usage']) / float(self.preemptData[index][4]) * 100, 1))))
            SystemManager.pipePrint("%s# %s: Tid(%s) / Comm(%s) / Total(%6.3f) / Threads(%d)\n" % \
                ('', 'PRT', tid, self.threadData[tid]['comm'], self.preemptData[index][4], count))
            SystemManager.pipePrint(SystemManager.bufferString)
            SystemManager.pipePrint(oneLine)

        # print new thread information after sorting by new thread flags #
        count = 0
        SystemManager.clearPrint()
        for key, value in sorted(self.threadData.items(), key=lambda e: e[1]['new'], reverse=True):
            if value['new'] == ' ' or SystemManager.selectMenu != None:
                break
            count += 1
            if SystemManager.showAll is True:
                SystemManager.addPrint(\
                    ("%16s(%5s/%5s)|%s%s|%5.2f(%5s)|%5.2f(%5.2f)|%3s|%5.2f|" + \
                    "%5d|%5s|%5s|%4s|%5.2f(%3d/%5d)|%4s(%3s)|%4d(%3d|%3d|%3d)|%3d|%3d|%4.2f(%2d)|\n") % \
                    (value['comm'], key, value['ptid'], value['new'], value['die'], \
                    value['usage'], str(round(float(usagePercent), 1)), \
                    value['cpuWait'], value['maxPreempted'], value['pri'], value['irq'], \
                    value['yield'], value['preempted'], value['preemption'], value['migrate'], \
                    value['ioWait'], value['readBlock'], value['readBlockCnt'], value['writeBlockCnt'], \
                    value['writeBlock'], (value['nrPages'] * 4 / 1024) + (value['remainKmem'] / 1024 / 1024), \
                    value['userPages'] * 4 / 1024, value['cachePages'] * 4 / 1024, \
                    value['kernelPages'] * 4 / 1024 + (value['remainKmem'] / 1024 / 1024), \
                    value['reclaimedPages'] * 4 / 1024, value['wasteKmem'] / 1024 / 1024, \
                    value['dReclaimWait'], value['dReclaimCnt']))
        if count > 0:
            SystemManager.pipePrint("%s# %s: %d\n" % ('', 'New', count))
            SystemManager.pipePrint(SystemManager.bufferString)
            SystemManager.pipePrint(oneLine)

        # print die thread information after sorting by die thread flags #
        count = 0
        SystemManager.clearPrint()
        for key, value in sorted(self.threadData.items(), key=lambda e: e[1]['die'], reverse=True):
            if value['die'] == ' ' or SystemManager.selectMenu != None:
                break
            count += 1
            usagePercent = round(float(value['usage']) / float(self.totalTime), 7) * 100
            if SystemManager.showAll is True:
                SystemManager.addPrint(\
                    ("%16s(%5s/%5s)|%s%s|%5.2f(%5s)|%5.2f(%5.2f)|%3s|%5.2f|" + \
                    "%5d|%5s|%5s|%4s|%5.2f(%3d/%5d)|%4s(%3s)|%4d(%3d|%3d|%3d)|%3d|%3d|%4.2f(%2d)|\n") % \
                    (value['comm'], key, value['ptid'], value['new'], value['die'], \
                    value['usage'], str(round(float(usagePercent), 1)), \
                    value['cpuWait'], value['maxPreempted'], value['pri'], value['irq'], \
                    value['yield'], value['preempted'], value['preemption'], value['migrate'], \
                    value['ioWait'], value['readBlock'], value['readBlockCnt'], value['writeBlockCnt'], \
                    value['writeBlock'], (value['nrPages'] * 4 / 1024) + (value['remainKmem'] / 1024 / 1024), \
                    value['userPages'] * 4 / 1024, value['cachePages'] * 4 / 1024, \
                    value['kernelPages'] * 4 / 1024 + (value['remainKmem'] / 1024 / 1024), \
                    value['reclaimedPages'] * 4 / 1024, value['wasteKmem'] / 1024 / 1024, \
                    value['dReclaimWait'], value['dReclaimCnt']))
        if count > 0:
            SystemManager.pipePrint("%s# %s: %d\n" % ('', 'Die', count))
            SystemManager.pipePrint(SystemManager.bufferString)
            SystemManager.pipePrint(oneLine)

        # print thread tree by creation #
        if SystemManager.showAll is True and len(SystemManager.showGroup) == 0 and self.nrNewTask > 0:
            SystemManager.clearPrint()
            SystemManager.pipePrint('\n' + \
                '[Thread Creation Info] [Alive: +] [Die: -] [CreatedTime: //] [ChildCount: ||] ' + \
                '[Usage: <>] [WaitTimeForChilds: {}] [WaitTimeOfParent: []]')
            SystemManager.pipePrint(twoLine)

            for key, value in sorted(self.threadData.items(), key=lambda e: e[1]['waitChild'], reverse=True):
                # print tree from root threads #
                if value['childList'] is not None and value['new'] is ' ':
                    self.printCreationTree(key, 0)
            SystemManager.pipePrint(oneLine)

        # print signal traffic #
        if SystemManager.showAll is True and len(SystemManager.showGroup) == 0 and len(self.sigData) > 0:
            SystemManager.clearPrint()
            SystemManager.pipePrint('\n' + '[Thread Signal Info]')
            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("%4s\t %8s\t %16s(%5s) \t%9s\t %16s(%5s)" % \
                ('TYPE', 'TIME', 'SENDER', 'TID', 'SIGNAL', 'RECEIVER', 'TID'))
            SystemManager.pipePrint(twoLine)

            for val in self.sigData:
                try:
                    ConfigManager.sigList[int(val[6])]
                except:
                    continue

                if val[0] == 'SEND':
                    SystemManager.pipePrint("%4s\t %3.6f\t %16s(%5s) \t%9s\t %16s(%5s)" % \
                        (val[0], val[1], val[2], val[3], \
                        ConfigManager.sigList[int(val[6])], val[4], val[5]))
                elif val[0] == 'RECV':
                    SystemManager.pipePrint("%4s\t %3.6f\t %16s(%5s) \t%9s\t %16s(%5s)" % \
                        (val[0], val[1], '', '', ConfigManager.sigList[int(val[6])], val[4], val[5]))
            SystemManager.pipePrint(oneLine)

        # print interrupt information #
        if len(self.irqData) > 0:
            totalCnt = int(0)
            totalUsage = float(0)

            SystemManager.pipePrint('\n' + '[Thread IRQ Info]')
            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("%16s(%16s): \t%6s\t\t%8s\t%8s\t%8s\t%8s\t%8s" % \
                ("IRQ", "Name", "Count", "Usage", "ProcMax", "ProcMin", "InterMax", "InterMin"))
            SystemManager.pipePrint(twoLine)

            SystemManager.clearPrint()
            for key in sorted(self.irqData.keys()):
                totalCnt += self.irqData[key]['count']
                totalUsage += self.irqData[key]['usage']
                SystemManager.addPrint("%16s(%16s): \t%6d\t\t%.6f\t%0.6f\t%0.6f\t%0.6f\t%0.6f\n" % \
                    (key, self.irqData[key]['name'], self.irqData[key]['count'], \
                    self.irqData[key]['usage'], self.irqData[key]['max'], \
                    self.irqData[key]['min'], self.irqData[key]['max_period'], \
                    self.irqData[key]['min_period']))

            SystemManager.pipePrint("%s# IRQ(%d) / Total(%6.3f) / Cnt(%d)\n" % \
                ('', len(self.irqData), totalUsage, totalCnt))
            SystemManager.pipePrint(SystemManager.bufferString)
            SystemManager.pipePrint(oneLine)

        # set option for making graph #
        if SystemManager.graphEnable is True:
            if SystemManager.intervalEnable > 0:
                os.environ['DISPLAY'] = 'localhost:0'
                rc('legend', fontsize=5)
                rcParams.update({'font.size': 8})
            else:
                SystemManager.printError("Use also -i option if you want to draw graph")
                SystemManager.graphEnable = False



    def printModuleInfo(self):
        eventCnt = 0
        for val in self.moduleData:
            event = val[0]
            if event == 'load' or event == 'free':
                eventCnt += 1
        if eventCnt == 0:
            return

        moduleTable = {}
        init_moduleData = {'startTime': float(0), 'loadCnt': int(0), 'elapsed': float(0)}

        SystemManager.clearPrint()
        SystemManager.pipePrint('\n' + '[Thread Module Info]')
        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^6}|{1:_^6}|{2:_^16}|{3:_^16}({4:^5})|{5:_^6}|".\
            format("Type", "Time", "Module", "Thread Name", "Tid", "Elapsed"))
        SystemManager.pipePrint(twoLine)

        for val in self.moduleData:
            event = val[0]
            tid = val[1]
            time = val[2]
            module = val[3]

            if event is 'load':
                try:
                    moduleTable[module]
                except:
                    moduleTable[module] = dict(init_moduleData)

                moduleTable[module]['startTime'] = time
                moduleTable[module]['loadCnt'] += 1

            elif event is 'free':
                SystemManager.pipePrint("{0:^6}|{1:6.3f}|{2:^16}|{3:>16}({4:>5})|{5:7}".\
                    format('FREE', float(time) - float(self.startTime), module, \
                    self.threadData[tid]['comm'], tid, ''))
            elif event is 'put':
                try:
                    moduleTable[module]
                except:
                    continue

                moduleTable[module]['elapsed'] += float(time) - float(moduleTable[module]['startTime'])
                moduleTable[module]['startTime'] = 0

                SystemManager.pipePrint("{0:^6}|{1:6.3f}|{2:^16}|{3:>16}({4:>5})|{5:7.3f}|".\
                    format('LOAD', float(time) - float(self.startTime), module, \
                    self.threadData[tid]['comm'], tid, moduleTable[module]['elapsed']))

        SystemManager.pipePrint(SystemManager.bufferString)
        SystemManager.pipePrint(oneLine)



    def printDepInfo(self):
        SystemManager.clearPrint()
        SystemManager.pipePrint('\n' + '[Thread Dependency Info]')
        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("\t%5s/%4s \t%16s(%4s) -> %16s(%4s) \t%5s" % \
            ("Total", "Inter", "From", "Tid", "To", "Tid", "Event"))
        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("%s# %s: %d\n" % ('', 'Dep', len(self.depData)))

        for icount in range(0, len(self.depData)):
            SystemManager.addPrint(self.depData[icount] + '\n')

        SystemManager.pipePrint(SystemManager.bufferString)
        SystemManager.pipePrint(oneLine)



    def printSyscallInfo(self):
        SystemManager.clearPrint()

        if self.syscallData != []:
            outputCnt = 0
            SystemManager.pipePrint('\n' + '[Thread Syscall Info]')
            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("%16s(%4s)\t%7s\t\t%5s\t\t%6s\t\t%6s\t\t%8s\t\t%8s\t\t%8s" % \
                ("Name", "Tid", "Syscall", "SysId", "Usage", "Count", "Min", "Max", "Avg"))
            SystemManager.pipePrint(twoLine)

            for key, value in sorted(self.threadData.items(), key=lambda e: e[1]['comm']):
                threadInfo = ''
                syscallInfo = ''

                if key[0:2] == '0[':
                    continue

                try:
                    if len(value['syscallInfo']) > 0:
                        threadInfo = "%16s(%4s)" % (value['comm'], key)
                    else:
                        continue
                except:
                    continue

                for sysId, val in sorted(value['syscallInfo'].items(), key=lambda e: e[1]['usage'], reverse=True):
                    try:
                        if val['count'] > 0:
                            val['average'] = val['usage'] / val['count']

                            syscallInfo += "%31s\t\t%5s\t\t%6.3f\t\t%6d\t\t%6.6f\t\t%6.6f\t\t%6.6f\n" % \
                                (ConfigManager.sysList[int(sysId)], sysId, val['usage'], \
                                 val['count'], val['min'], val['max'], val['average'])
                    except:
                        continue

                if syscallInfo != '':
                    outputCnt += 1
                    SystemManager.pipePrint(threadInfo)
                    SystemManager.pipePrint(syscallInfo)

            if outputCnt == 0:
                SystemManager.pipePrint('None')

            SystemManager.pipePrint(oneLine)

            SystemManager.clearPrint()
            if SystemManager.showAll is True:
                SystemManager.pipePrint('\n' + '[Thread Syscall History Info]')
                SystemManager.pipePrint(twoLine)
                SystemManager.pipePrint("%16s(%4s)\t%8s\t%8s\t%5s\t%16s\t%6s\t%4s\t%8s\t%s" % \
                    ("Name", "Tid", "Time", "Diff", "Type", "Syscall", "SysId", "Core", "Return", "Parameter"))
                SystemManager.pipePrint(twoLine)

                for icount in range(0, len(self.syscallData)):
                    try:
                        if self.syscallData[icount][0] == 'enter':
                            if self.syscallData[icount + 1][0] == 'exit' and \
                                self.syscallData[icount][4] == self.syscallData[icount + 1][4]:
                                eventType = 'both'
                                eventTime = float(self.syscallData[icount][1]) - float(self.startTime)
                                diffTime = float(self.syscallData[icount + 1][1]) - \
                                    float(self.syscallData[icount][1])
                                ret = self.syscallData[icount + 1][5]
                                param = self.syscallData[icount][5]
                            else:
                                eventType = self.syscallData[icount][0]
                                eventTime = float(self.syscallData[icount][1]) - float(self.startTime)
                                diffTime = float(0)
                                ret = '-'
                                param = self.syscallData[icount][5]
                        else:
                            if self.syscallData[icount - 1][0] == 'enter' and \
                                    self.syscallData[icount][4] == self.syscallData[icount - 1][4]:
                                continue
                            else:
                                eventType = self.syscallData[icount][0]
                                eventTime = float(self.syscallData[icount][1]) - float(self.startTime)
                                diffTime = float(0)
                                ret = self.syscallData[icount][5]
                                param = '-'

                        SystemManager.pipePrint("%16s(%4s)\t%6.6f\t%6.6f\t%5s\t%16s\t%6s\t%4s\t%8s\t%s" % \
                            (self.threadData[self.syscallData[icount][2]]['comm'], \
                            self.syscallData[icount][2], eventTime, diffTime, eventType, \
                            ConfigManager.sysList[int(self.syscallData[icount][4])], \
                            self.syscallData[icount][4], self.syscallData[icount][3], ret, param))
                    except:
                        continue
                SystemManager.pipePrint(oneLine)



    def printConsoleInfo(self):
        if len(self.consoleData) > 0 and SystemManager.showAll is True:
            SystemManager.pipePrint('\n' + '[Thread Message Info]')
            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint(\
                "%16s %5s %4s %10s %30s" % ('Name', 'Tid', 'Core', 'Time', 'Console message'))
            SystemManager.pipePrint(twoLine)

            for msg in self.consoleData:
                try:
                    SystemManager.pipePrint("%16s %5s %4s %10.3f %s" % \
                        (self.threadData[msg[0]]['comm'], msg[0], msg[1], \
                        round(float(msg[2]) - float(self.startTime), 7), msg[3]))
                except:
                    continue

            SystemManager.pipePrint(twoLine)



    def printIntervalInfo(self):
        SystemManager.pipePrint('\n' + '[Thread Interval Info] [ Unit: %s Sec ]' % SystemManager.intervalEnable)
        SystemManager.pipePrint(twoLine)

        # Total timeline #
        timeLine = ''
        for icount in range(1, int(float(self.totalTime) / SystemManager.intervalEnable) + 2):
            checkEvent = ' '
            cnt = icount - 1

            # check suspend event #
            for val in self.suspendData:
                if float(self.startTime) + cnt * SystemManager.intervalEnable < float(val[0]) < \
                    float(self.startTime) + ((cnt + 1) * SystemManager.intervalEnable):
                    if val[1] == 'S':
                        checkEvent = '!'
                    elif val[1] == 'F':
                        checkEvent = '^'
                    else:
                        checkEvent = '>'

            # check mark event #
            for val in self.markData:
                if float(self.startTime) + cnt * SystemManager.intervalEnable < float(val) < \
                    float(self.startTime) + ((cnt + 1) * SystemManager.intervalEnable):
                    checkEvent = 'v'

            # print timeline #
            if icount * SystemManager.intervalEnable < float(self.totalTime):
                timeLine += '%s%2d ' % (checkEvent, icount * SystemManager.intervalEnable)
            else:
                timeLine += '%s%.2f ' % (checkEvent, self.totalTime)

        SystemManager.pipePrint("%16s(%5s/%5s): %s" % ('Name', 'Tid', 'Pid', timeLine))
        SystemManager.pipePrint(twoLine)
        SystemManager.clearPrint()

        # total CPU in timeline #
        for key, value in sorted(self.threadData.items(), key=lambda e: e[1]['comm'], reverse=False):
            if key[0:2] == '0[':
                icount = 0
                timeLine = ''
                for icount in range(0, int(float(self.totalTime) / SystemManager.intervalEnable) + 1):
                    try:
                        self.intervalData[icount][key]
                    except:
                        timeLine += '%3s ' % '0'
                        continue

                    timeLine += '%3d ' % (100 - self.intervalData[icount][key]['cpuPer'])
                SystemManager.addPrint("%16s(%5s/%5s): " % \
                    (value['comm'], '0', value['tgid']) + timeLine + '\n')

                if SystemManager.graphEnable is True:
                    try:
                        timeLine = timeLine.replace('N', '')
                        timeLine = timeLine.replace('D', '')
                        timeLine = timeLine.replace('F', '')
                        timeLineData = [int(n) for n in timeLine.split()]

                        subplot(2, 1, 1)
                        range(SystemManager.intervalEnable, \
                            (len(timeLineData)+1)*SystemManager.intervalEnable, \
                            SystemManager.intervalEnable)
                        plot(range(SystemManager.intervalEnable, \
                            (len(timeLineData)+1)*SystemManager.intervalEnable, \
                            SystemManager.intervalEnable), timeLineData, '.-')
                        SystemManager.graphLabels.append(value['comm'])
                    except:
                        SystemManager.graphEnable = False
                        SystemManager.printError("Fail to draw graph")

        if SystemManager.graphEnable is True:
            title('Core Usage')
            ylabel('Percentage(%)', fontsize=10)
            legend(SystemManager.graphLabels, bbox_to_anchor=(1.135, 1.02))
            del SystemManager.graphLabels[:]

        # total MEM in timeline #
        icount = 0
        timeLine = ''
        for icount in range(0, int(float(self.totalTime) / SystemManager.intervalEnable) + 1):
            try:
                timeLine += '%3d ' % ((self.intervalData[icount]['toTal']['totalMem'] * 4 / 1024) + \
                    (self.intervalData[icount]['toTal']['totalKmem'] / 1024 / 1024))
            except:
                timeLine += '%3d ' % (0)
        SystemManager.addPrint("\n%16s(%5s/%5s): " % ('MEM', '0', '-----') + timeLine + '\n')

        # total BLOCK_READ in timeline #
        icount = 0
        timeLine = ''
        for icount in range(0, int(float(self.totalTime) / SystemManager.intervalEnable) + 1):
            try:
                timeLine += '%3d ' % (self.intervalData[icount]['toTal']['totalIo'] * \
                    SystemManager.blockSize / 1024 / 1024)
            except:
                timeLine += '%3d ' % (0)
        SystemManager.addPrint("\n%16s(%5s/%5s): " % ('BLK_RD', '0', '-----') + timeLine + '\n')

        SystemManager.pipePrint("%s# %s\n" % ('', 'Total(%/MB)'))
        SystemManager.pipePrint(SystemManager.bufferString)
        SystemManager.pipePrint(oneLine)
        SystemManager.clearPrint()

        # CPU timeline #
        for key, value in sorted(self.threadData.items(), key=lambda e: e[1]['usage'], reverse=True):
            if key[0:2] != '0[':
                icount = 0
                timeLine = ''

                for icount in range(0, int(float(self.totalTime) / SystemManager.intervalEnable) + 1):
                    newFlag = ' '
                    dieFlag = ' '

                    try:
                        self.intervalData[icount][key]
                    except:
                        timeLine += '%3d ' % 0
                        continue

                    if icount > 0:
                        try:
                            if self.intervalData[icount][key]['new'] != self.intervalData[icount - 1][key]['new']:
                                newFlag = self.intervalData[icount][key]['new']
                        except:
                            newFlag = self.intervalData[icount][key]['new']
                        try:
                            if self.intervalData[icount][key]['die'] != self.intervalData[icount - 1][key]['die']:
                                dieFlag = self.intervalData[icount][key]['die']
                        except:
                            dieFlag = self.intervalData[icount][key]['die']
                    else:
                        newFlag = self.intervalData[icount][key]['new']
                        dieFlag = self.intervalData[icount][key]['die']

                    timeLine += '%4s' % (newFlag + str(int(self.intervalData[icount][key]['cpuPer'])) + dieFlag)
                SystemManager.addPrint("%16s(%5s/%5s): " % (value['comm'], key, value['tgid']) + timeLine + '\n')

                if SystemManager.graphEnable is True:
                    timeLine = timeLine.replace('N', '')
                    timeLine = timeLine.replace('D', '')
                    timeLine = timeLine.replace('F', '')
                    timeLineData = [int(n) for n in timeLine.split()]

                    subplot(2, 1, 2)
                    plot(range(SystemManager.intervalEnable, \
                        (len(timeLineData)+1)*SystemManager.intervalEnable, \
                        SystemManager.intervalEnable), timeLineData, '.-')
                    SystemManager.graphLabels.append(value['comm'])

                if value['usage'] / float(self.totalTime) * 100 < 1 and SystemManager.showAll is False:
                    break

        if SystemManager.graphEnable is True:
            title('CPU Usage of Threads')
            ylabel('Percentage(%)', fontsize=10)
            legend(SystemManager.graphLabels, bbox_to_anchor=(1.135, 1.02))
            del SystemManager.graphLabels[:]
            figure(num=1, figsize=(20, 20), dpi=200, facecolor='b', edgecolor='k')
            savefig("cpuInfo.png", dpi=(200))
            clf()

        SystemManager.pipePrint("%s# %s\n" % ('', 'CPU(%)'))
        SystemManager.pipePrint(SystemManager.bufferString)
        SystemManager.pipePrint(oneLine)

        # Preempted timeline #
        SystemManager.clearPrint()
        for key, value in sorted(self.threadData.items(), key=lambda e: e[1]['cpuWait'], reverse=True):
            if key[0:2] != '0[':
                icount = 0
                timeLine = ''
                for icount in range(0, int(float(self.totalTime) / SystemManager.intervalEnable) + 1):
                    newFlag = ' '
                    dieFlag = ' '

                    try:
                        self.intervalData[icount][key]
                    except:
                        timeLine += '%3d ' % 0
                        continue

                    if icount > 0:
                        try:
                            if self.intervalData[icount][key]['new'] != self.intervalData[icount - 1][key]['new']:
                                newFlag = self.intervalData[icount][key]['new']
                        except:
                            newFlag = self.intervalData[icount][key]['new']
                        try:
                            if self.intervalData[icount][key]['die'] != self.intervalData[icount - 1][key]['die']:
                                dieFlag = self.intervalData[icount][key]['die']
                        except:
                            dieFlag = self.intervalData[icount][key]['die']
                    else:
                        newFlag = self.intervalData[icount][key]['new']
                        dieFlag = self.intervalData[icount][key]['die']

                    timeLine += '%4s' % (newFlag + \
                        str(int(self.intervalData[icount][key]['preempted'] / \
                        float(SystemManager.intervalEnable) * 100)) + dieFlag)

                SystemManager.addPrint("%16s(%5s/%5s): " % (value['comm'], key, value['tgid']) + timeLine + '\n')

                if value['cpuWait'] / float(self.totalTime) * 100 < 1 and SystemManager.showAll is False:
                    break

        SystemManager.pipePrint("%s# %s\n" % ('', 'Delay(%)'))
        SystemManager.pipePrint(SystemManager.bufferString)
        SystemManager.pipePrint(oneLine)

        # Memory timeline #
        SystemManager.clearPrint()
        if SystemManager.memEnable is True:
            for key, value in sorted(self.threadData.items(), key=lambda e: e[1]['nrPages'], reverse=True):
                if key[0:2] != '0[':
                    icount = 0
                    timeLine = ''
                    for icount in range(0, int(float(self.totalTime) / SystemManager.intervalEnable) + 1):
                        newFlag = ' '
                        dieFlag = ' '

                        try:
                            self.intervalData[icount][key]
                        except:
                            timeLine += '%3d ' % 0
                            continue

                        if icount > 0:
                            try:
                                if self.intervalData[icount][key]['new'] != self.intervalData[icount - 1][key]['new']:
                                    newFlag = self.intervalData[icount][key]['new']
                            except:
                                newFlag = self.intervalData[icount][key]['new']
                            try:
                                if self.intervalData[icount][key]['die'] != self.intervalData[icount - 1][key]['die']:
                                    dieFlag = self.intervalData[icount][key]['die']
                            except:
                                dieFlag = self.intervalData[icount][key]['die']
                        else:
                            newFlag = self.intervalData[icount][key]['new']
                            dieFlag = self.intervalData[icount][key]['die']

                        timeLine += '%4s' % (newFlag + \
                            str(int((self.intervalData[icount][key]['memUsage'] * 4 / 1024) + \
                            (self.intervalData[icount][key]['kmemUsage'] / 1024 / 1024))) + dieFlag)
                    SystemManager.addPrint("%16s(%5s/%5s): " % (value['comm'], key, value['tgid']) + timeLine + '\n')

                    if SystemManager.graphEnable is True:
                        timeLine = timeLine.replace('N', '')
                        timeLine = timeLine.replace('D', '')
                        timeLine = timeLine.replace('F', '')
                        timeLineData = [int(n) for n in timeLine.split()]

                        subplot(2, 1, 2)
                        plot(range(SystemManager.intervalEnable, \
                            (len(timeLineData) + 1) * SystemManager.intervalEnable, \
                            SystemManager.intervalEnable), timeLineData, '.-')
                        SystemManager.graphLabels.append(value['comm'])

                    if (value['nrPages'] * 4 / 1024) + (value['remainKmem'] / 1024 / 1024) < 1 and \
                        SystemManager.showAll == False:
                        break

            SystemManager.pipePrint("%s# %s\n" % ('', 'MEM(MB)'))
            SystemManager.pipePrint(SystemManager.bufferString)
            SystemManager.pipePrint(oneLine)

            if SystemManager.graphEnable is True:
                title('MEM Usage of Threads')
                ylabel('Size(MB)', fontsize=10)
                legend(SystemManager.graphLabels, bbox_to_anchor=(1.135, 1.02))
                del SystemManager.graphLabels[:]

        # Block timeline #
        SystemManager.clearPrint()
        if SystemManager.blockEnable is True:
            for key, value in sorted(self.threadData.items(), key=lambda e: e[1]['reqBlock'], reverse=True):
                if key[0:2] != '0[':
                    icount = 0
                    timeLine = ''
                    for icount in range(0, int(float(self.totalTime) / SystemManager.intervalEnable) + 1):
                        newFlag = ' '
                        dieFlag = ' '

                        try:
                            self.intervalData[icount][key]
                        except:
                            timeLine += '%3d ' % 0
                            continue

                        if icount > 0:
                            try:
                                if self.intervalData[icount][key]['new'] != self.intervalData[icount - 1][key]['new']:
                                    newFlag = self.intervalData[icount][key]['new']
                            except:
                                newFlag = self.intervalData[icount][key]['new']
                            try:
                                if self.intervalData[icount][key]['die'] != self.intervalData[icount - 1][key]['die']:
                                    dieFlag = self.intervalData[icount][key]['die']
                            except:
                                dieFlag = self.intervalData[icount][key]['die']
                        else:
                            newFlag = self.intervalData[icount][key]['new']
                            dieFlag = self.intervalData[icount][key]['die']

                        timeLine += '%4s' % (newFlag + \
                            str(int(self.intervalData[icount][key]['ioUsage'] * \
                            SystemManager.blockSize / 1024 / 1024)) + dieFlag)

                    SystemManager.addPrint("%16s(%5s/%5s): " % (value['comm'], key, value['tgid']) + timeLine + '\n')

                    if SystemManager.graphEnable is True:
                        timeLine = timeLine.replace('N', '')
                        timeLine = timeLine.replace('D', '')
                        timeLine = timeLine.replace('F', '')
                        timeLineData = [int(n) for n in timeLine.split()]

                        subplot(2, 1, 1)
                        plot(range(SystemManager.intervalEnable, \
                            (len(timeLineData)+1)*SystemManager.intervalEnable, \
                            SystemManager.intervalEnable), timeLineData, '.-')
                        SystemManager.graphLabels.append(value['comm'])

                    if value['readBlock'] < 1 and SystemManager.showAll == False:
                        break

            if SystemManager.graphEnable is True:
                title('Disk Usage of Threads')
                ylabel('Size(MB)', fontsize=10)
                legend(SystemManager.graphLabels, bbox_to_anchor=(1.135, 1.02))
                del SystemManager.graphLabels[:]

            SystemManager.pipePrint("%s# %s\n" % ('', 'BLK_RD(MB)'))
            SystemManager.pipePrint(SystemManager.bufferString)
            SystemManager.pipePrint(oneLine)

        if SystemManager.graphEnable is True:
            figure(num=1, figsize=(20, 20), dpi=200, facecolor='b', edgecolor='k')
            savefig("ioInfo.png", dpi=(200))





    @staticmethod
    def getInitTime(file):
        readLineCnt = 0
        systemInfoBuffer = ''

        try:
            f = open(file, 'r')

            while True:
                # Make delay because some filtered logs are not written soon #
                time.sleep(0.01)

                # Find recognizable log in file #
                if readLineCnt > 500 and SystemManager.recordStatus is not True:
                    SystemManager.printError(\
                        "Fail to recognize format: corrupted log / no log collected")
                    sys.exit(0)

                l = f.readline()

                # Find system info data in file and save it #
                if l[0:-1] == SystemManager.magicString:
                    while True:
                        l = f.readline()

                        if l[0:-1] == SystemManager.magicString:
                            SystemManager.systemInfoBuffer = systemInfoBuffer
                            break
                        else:
                            systemInfoBuffer += l

                readLineCnt += 1

                m = re.match(r'^\s*(?P<comm>\S+)-(?P<thread>[0-9]+)\s+\(\s*(?P<tgid>\S+)\)' + \
                    r'\s+\[(?P<core>[0-9]+)\]\s+(?P<time>\S+):\s+(?P<func>\S+):(?P<etc>.+)', l)
                if m is not None:
                    d = m.groupdict()
                    f.close()
                    return d['time']

                m = re.match(r'^\s*(?P<comm>\S+)-(?P<thread>[0-9]+)\s+\[(?P<core>[0-9]+)\]' + \
                    r'\s+(?P<time>\S+):\s+(?P<func>\S+):(?P<etc>.+)', l)
                if m is not None:
                    d = m.groupdict()
                    f.close()
                    SystemManager.tgidEnable = False
                    return d['time']

        except IOError:
            SystemManager.printError("Fail to open %s" % file)
            sys.exit(0)



    def parse(self, string):
        SystemManager.curLine += 1

        if SystemManager.tgidEnable is True:
            m = re.match(r'^\s*(?P<comm>.+)-(?P<thread>[0-9]+)\s+\(\s*(?P<tgid>\S+)\)\s+' + \
                r'\[(?P<core>[0-9]+)\]\s+(?P<time>\S+):\s+(?P<func>\S+):(?P<etc>.+)', string)
        else:
            m = re.match(r'^\s*(?P<comm>.+)-(?P<thread>[0-9]+)\s+\[(?P<core>[0-9]+)\]\s+' + \
                r'(?P<time>\S+):\s+(?P<func>\S+):(?P<etc>.+)', string)
        if m is not None:
            d = m.groupdict()
            comm = d['comm']
            core = str(int(d['core']))
            func = d['func']
            etc = d['etc']
            time = d['time']

            SystemManager.logSize += len(string)

            self.lastCore = core
            self.lastEvent = func

            if SystemManager.maxCore < int(core):
                SystemManager.maxCore = int(core)

            coreId = '0' + '['  + core + ']'
            if int(d['thread']) == 0:
                thread = coreId
                comm = comm.replace("<idle>", "swapper/" + core)
            else:
                thread = d['thread']

            # make core thread entity in advance for total irq per core #
            try:
                self.threadData[coreId]
            except:
                self.threadData[coreId] = dict(self.init_threadData)
                self.threadData[coreId]['comm'] = "swapper/" + core

            # make thread entity #
            try:
                self.threadData[thread]
            except:
                self.threadData[thread] = dict(self.init_threadData)
                self.threadData[thread]['comm'] = comm

            if SystemManager.tgidEnable is True:
                self.threadData[thread]['tgid'] = d['tgid']

            # calculate usage of threads had been running longer than interval #
            if SystemManager.intervalEnable > 0:
                for key, value in sorted(self.lastTidPerCore.items()):
                    try:
                        if float(time) - float(self.threadData[self.lastTidPerCore[key]]['start']) > \
                            SystemManager.intervalEnable / 1000:
                            self.threadData[self.lastTidPerCore[key]]['usage'] += \
                                float(time) - float(self.threadData[self.lastTidPerCore[key]]['start'])

                            self.threadData[self.lastTidPerCore[key]]['start'] = float(time)
                    except:
                        continue

            if self.startTime == '0':
                self.startTime = time
            else:
                # check whether this log is last one or not #
                if SystemManager.curLine >= SystemManager.totalLine:
                    self.finishTime = time

                # calculate usage of threads in interval #
                if SystemManager.intervalEnable > 0:
                    intervalCnt = float(SystemManager.intervalNow + SystemManager.intervalEnable)

                    if float(time) - float(self.startTime) > intervalCnt or self.finishTime != '0':
                        SystemManager.intervalNow += SystemManager.intervalEnable

                        for key, value in sorted(self.threadData.items(), key=lambda e: e[1]['usage'], reverse=True):
                            index = int(SystemManager.intervalNow / SystemManager.intervalEnable) - 1
                            nextIndex = int(SystemManager.intervalNow / SystemManager.intervalEnable)

                            try:
                                self.intervalData[index]
                            except:
                                self.intervalData.append({})
                            try:
                                self.intervalData[index][key]
                            except:
                                self.intervalData[index][key] = dict(self.init_intervalData)
                            try:
                                self.intervalData[index]['toTal']
                            except:
                                self.intervalData[index]['toTal'] = \
                                    {'totalIo': int(0), 'totalMem': int(0), 'totalKmem': int(0)}
                            intervalThread = self.intervalData[index][key]

                            # save start time in this interval #
                            intervalThread['firstLogTime'] = float(time)

                            try:
                                self.intervalData[nextIndex]
                            except:
                                self.intervalData.append({})
                            try:
                                self.intervalData[nextIndex][key]
                            except:
                                self.intervalData[nextIndex][key] = dict(self.init_intervalData)

                            # save total usage in this interval #
                            intervalThread['totalUsage'] = float(self.threadData[key]['usage'])
                            intervalThread['totalPreempted'] = float(self.threadData[key]['cpuWait'])
                            intervalThread['totalCoreSchedCnt'] = float(self.threadData[key]['coreSchedCnt'])
                            intervalThread['totalIoUsage'] = float(self.threadData[key]['reqBlock'])
                            intervalThread['totalMemUsage'] = float(self.threadData[key]['nrPages'])
                            intervalThread['totalKmemUsage'] = float(self.threadData[key]['remainKmem'])

                            # add time not calculated yet in this interval to related threads #
                            for idx, val in self.lastTidPerCore.items():
                                intervalThread['totalUsage'] += \
                                    (float(time) - float(self.threadData[val]['start']))

                            # mark life flag #
                            if self.threadData[key]['new'] != ' ':
                                intervalThread['new'] = self.threadData[key]['new']
                            if self.threadData[key]['die'] != ' ':
                                intervalThread['die'] = self.threadData[key]['die']

                            # first interval #
                            if SystemManager.intervalNow - SystemManager.intervalEnable == 0:
                                intervalThread['cpuUsage'] += float(self.threadData[key]['usage'])
                                intervalThread['preempted'] += float(self.threadData[key]['cpuWait'])
                                intervalThread['coreSchedCnt'] = float(self.threadData[key]['coreSchedCnt'])
                                intervalThread['ioUsage'] = float(self.threadData[key]['reqBlock'])
                                intervalThread['memUsage'] = float(self.threadData[key]['nrPages'])
                                intervalThread['kmemUsage'] = float(self.threadData[key]['remainKmem'])
                            # later intervals #
                            else:
                                try:
                                    self.intervalData[index - 1][key]
                                except:
                                    self.intervalData[index - 1][key] = dict(self.init_intervalData)
                                prevIntervalThread = self.intervalData[index - 1][key]

                                intervalThread['cpuUsage'] += \
                                    intervalThread['totalUsage'] - prevIntervalThread['totalUsage']
                                intervalThread['preempted'] += \
                                    intervalThread['totalPreempted'] - prevIntervalThread['totalPreempted']
                                intervalThread['coreSchedCnt'] = \
                                    intervalThread['totalCoreSchedCnt'] - prevIntervalThread['totalCoreSchedCnt']
                                intervalThread['ioUsage'] = \
                                    intervalThread['totalIoUsage'] - prevIntervalThread['totalIoUsage']
                                intervalThread['memUsage'] = \
                                    intervalThread['totalMemUsage'] - prevIntervalThread['totalMemUsage']
                                intervalThread['kmemUsage'] = \
                                    intervalThread['totalKmemUsage'] - prevIntervalThread['totalKmemUsage']

                            # fix cpu usage exceed this interval #
                            self.thisInterval = SystemManager.intervalEnable
                            if intervalThread['cpuUsage'] > SystemManager.intervalEnable or self.finishTime != '0':
                                # first interval #
                                if index == 0:
                                    self.thisInterval = float(time) - float(self.startTime)
                                # normal intervals #
                                elif float(self.intervalData[index - 1][key]['firstLogTime']) > 0:
                                    self.thisInterval = \
                                        float(time) - float(self.intervalData[index - 1][key]['firstLogTime'])
                                # long time running intervals #
                                else:
                                    for idx in range(index - 1, -1, -1):
                                        if float(self.intervalData[index - 1][key]['firstLogTime']) > 0:
                                            self.thisInterval = \
                                                float(time) - float(self.intervalData[idx][key]['firstLogTime'])
                                            break
                                    if self.thisInterval != SystemManager.intervalEnable:
                                        self.thisInterval = float(time) - float(self.startTime)

                                # recalculate previous intervals if there was no context switching since profile start #
                                remainTime = intervalThread['cpuUsage']
                                if intervalThread['cpuUsage'] > self.thisInterval:
                                    for idx in range(int(intervalThread['cpuUsage'] / SystemManager.intervalEnable), -1, -1):
                                        try:
                                            self.intervalData[idx][key]
                                        except:
                                            self.intervalData[idx][key] = dict(self.init_intervalData)
                                        try:
                                            self.intervalData[idx - 1][key]
                                        except:
                                            self.intervalData[idx - 1][key] = dict(self.init_intervalData)
                                        prevIntervalData = self.intervalData[idx - 1][key]

                                        # make previous intervals of core there was no context switching #
                                        longRunCore = self.threadData[key]['longRunCore']
                                        if longRunCore >= 0:
                                            longRunCoreId = '0[' + longRunCore + ']'
                                            try:
                                                self.intervalData[idx][longRunCoreId]
                                            except:
                                                self.intervalData[idx][longRunCoreId] = dict(self.init_intervalData)

                                        if remainTime >= SystemManager.intervalEnable:
                                            remainTime = \
                                                int(remainTime / SystemManager.intervalEnable) * SystemManager.intervalEnable
                                            prevIntervalData['cpuUsage'] = SystemManager.intervalEnable
                                            prevIntervalData['cpuPer'] = 100
                                        else:
                                            if prevIntervalData['cpuUsage'] > remainTime:
                                                remainTime = prevIntervalData['cpuUsage']
                                            else:
                                                prevIntervalData['cpuUsage'] = remainTime
                                            prevIntervalData['cpuPer'] = remainTime / SystemManager.intervalEnable * 100

                                        remainTime -= SystemManager.intervalEnable

                            # add remainter of cpu usage exceed interval in this interval to previous interval #
                            if SystemManager.intervalNow - SystemManager.intervalEnable > 0 and \
                                self.thisInterval > SystemManager.intervalEnable:
                                diff = self.thisInterval - SystemManager.intervalEnable
                                if prevIntervalThread['cpuUsage'] + diff > SystemManager.intervalEnable:
                                    diff = SystemManager.intervalEnable - prevIntervalThread['cpuUsage']

                                prevIntervalThread['cpuUsage'] += diff
                                prevIntervalThread['cpuPer'] = \
                                    prevIntervalThread['cpuUsage'] / SystemManager.intervalEnable * 100

                            # calculate percentage of cpu usage of this thread in this interval #
                            if self.thisInterval > 0:
                                intervalThread['cpuPer'] = intervalThread['cpuUsage'] / self.thisInterval * 100
                            else:
                                intervalThread['cpuPer'] = 0

                            # revise thread interval usage in DVFS system #
                            if intervalThread['cpuPer'] > 100:
                                intervalThread['cpuPer'] = 100
                            elif intervalThread['cpuPer'] < 0:
                                intervalThread['cpuPer'] = 0

                            # fix preempted time exceed this interval #
                            if intervalThread['preempted'] > SystemManager.intervalEnable:
                                # recalculate previous intervals if there was no context switching since profile start #
                                remainTime = intervalThread['preempted']
                                if intervalThread['preempted'] > self.thisInterval:
                                    for idx in range(index + 1, -1, -1):
                                        try:
                                            self.intervalData[idx][key]
                                        except:
                                            self.intervalData[idx][key] = dict(self.init_intervalData)
                                        try:
                                            self.intervalData[idx - 1][key]
                                        except:
                                            self.intervalData[idx - 1][key] = dict(self.init_intervalData)

                                        if remainTime >= SystemManager.intervalEnable:
                                            self.intervalData[idx - 1][key]['preempted'] = SystemManager.intervalEnable
                                        else:
                                            self.intervalData[idx - 1][key]['preempted'] += remainTime

                                        remainTime -= SystemManager.intervalEnable
                                        if remainTime <= 0:
                                            break

                            # calculate block usage of this thread in this interval #
                            self.intervalData[index]['toTal']['totalIo'] += \
                                self.intervalData[index][key]['ioUsage']

                            """
                            calculate memory usage of this thread in this interval \
                            except for core threads because its already calculated
                            """
                            if key[0:2] == '0[':
                                continue

                            self.intervalData[index]['toTal']['totalMem'] += self.intervalData[index][key]['memUsage']
                            self.intervalData[index]['toTal']['totalKmem'] += self.intervalData[index][key]['kmemUsage']

            if func == "sched_switch":
                m = re.match(r'^\s*prev_comm=(?P<prev_comm>.*)\s+prev_pid=(?P<prev_pid>[0-9]+)\s+' + \
                    r'prev_prio=(?P<prev_prio>\S+)\s+prev_state=(?P<prev_state>\S+)\s+==>\s+' + \
                    r'next_comm=(?P<next_comm>.*)\s+next_pid=(?P<next_pid>[0-9]+)\s+' + \
                    r'next_prio=(?P<next_prio>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    self.cxtSwitch += 1

                    prev_comm = d['prev_comm']
                    prev_pid = d['prev_pid']
                    prev_id = prev_pid

                    if int(d['prev_pid']) == 0:
                        prev_id = d['prev_pid'] + '[' + str(int(core)) + ']'
                    else:
                        prev_id = prev_pid

                    next_comm = d['next_comm']
                    next_pid = d['next_pid']

                    if int(d['next_pid']) == 0:
                        next_id = d['next_pid'] + '[' + str(int(core)) + ']'
                    else:
                        next_id = next_pid

                    # make list #
                    try:
                        self.threadData[prev_id]
                    except:
                        self.threadData[prev_id] = dict(self.init_threadData)
                        self.threadData[prev_id]['comm'] = prev_comm
                    try:
                        self.threadData[next_id]
                    except:
                        self.threadData[next_id] = dict(self.init_threadData)
                        self.threadData[next_id]['comm'] = next_comm
                    try:
                        self.threadData['0[' + core + ']']
                    except:
                        self.threadData['0[' + core + ']'] = dict(self.init_threadData)
                        self.threadData['0[' + core + ']']['comm'] = 'swapper/' + core

                    if self.wakeupData['valid'] > 0 and self.wakeupData['tid'] == prev_id:
                        self.wakeupData['valid'] -= 1

                    # update anonymous comm #
                    if comm == '<...>':
                        comm = prev_comm
                    if self.threadData[prev_id]['comm'] == '<...>':
                        self.threadData[prev_id]['comm'] = prev_comm
                    if self.threadData[next_id]['comm'] == '<...>':
                        self.threadData[next_id]['comm'] = next_comm

                    # write current time #
                    self.threadData[prev_id]['stop'] = float(time)
                    self.threadData[next_id]['start'] = float(time)
                    self.threadData[next_id]['waitStartAsParent'] = float(0)

                    # update priority of thread to highest one #
                    if self.threadData[prev_id]['pri'] == '0' or \
                        int(self.threadData[prev_id]['pri']) > int(d['prev_prio']):
                        self.threadData[prev_id]['pri'] = d['prev_prio']
                    if self.threadData[next_id]['pri'] == '0' or \
                        int(self.threadData[next_id]['pri']) > int(d['next_prio']):
                        self.threadData[next_id]['pri'] = d['next_prio']

                    # calculate running time of prev_process #
                    diff = 0
                    if self.threadData[prev_id]['start'] <= 0:
                        # calculate running time of prev_process started before starting to profile #
                        if self.threadData['0[' + core + ']']['coreSchedCnt'] == 0:
                            diff = float(time) - float(self.startTime)
                            self.threadData[prev_id]['usage'] = diff
                        # it is possible that log was loss #
                        else:
                            pass
                    else:
                        diff = self.threadData[prev_id]['stop'] - self.threadData[prev_id]['start']
                        self.threadData[prev_id]['usage'] += diff

                        if self.threadData[prev_id]['maxRuntime'] < diff:
                            self.threadData[prev_id]['maxRuntime'] = diff

                    if diff > int(SystemManager.intervalEnable):
                        self.threadData[prev_id]['longRunCore'] = core

                    # update core sched count #
                    self.threadData['0[' + core + ']']['coreSchedCnt'] += 1

                    # calculate preempted time of threads blocked #
                    if SystemManager.preemptGroup != None:
                        for value in SystemManager.preemptGroup:
                            index = SystemManager.preemptGroup.index(value)
                            if self.preemptData[index][0] is True and self.preemptData[index][3] == core:
                                try:
                                    self.preemptData[index][1][prev_id]
                                except:
                                    self.preemptData[index][1][prev_id] = dict(self.init_preemptData)

                                self.preemptData[index][1][prev_id]['usage'] +=  \
                                    self.threadData[prev_id]['stop'] - self.threadData[prev_id]['start']
                                self.preemptData[index][4] += \
                                    self.threadData[prev_id]['stop'] - self.threadData[prev_id]['start']

                    if d['prev_state'][0] == 'R':
                        self.threadData[prev_id]['preempted'] += 1
                        self.threadData[next_id]['preemption'] += 1
                        self.threadData[prev_id]['lastStatus'] = 'P'

                        if SystemManager.preemptGroup != None:
                            # enable preempted bit #
                            try:
                                index = SystemManager.preemptGroup.index(prev_id)
                            except:
                                index = -1

                            if index >= 0:
                                self.preemptData[index][0] = True
                                try:
                                    self.preemptData[index][1][next_id]
                                except:
                                    self.preemptData[index][1][next_id] = dict(self.init_preemptData)

                                self.preemptData[index][2] = float(time)
                                self.preemptData[index][3] = core

                    elif d['prev_state'][0] == 'S':
                        self.threadData[prev_id]['yield'] += 1
                        self.threadData[prev_id]['stop'] = 0
                        self.threadData[prev_id]['lastStatus'] = 'S'

                    else:
                        self.threadData[prev_id]['stop'] = 0
                        self.threadData[prev_id]['lastStatus'] = d['prev_state'][0]

                    # calculate preempted time of next_process #
                    self.lastTidPerCore[core] = next_id
                    if self.threadData[next_id]['stop'] <= 0:
                        # no stop time of next_id #
                        self.threadData[next_id]['stop'] = 0
                    else:
                        if self.threadData[next_id]['lastStatus'] == 'P':
                            preemptedTime = \
                                self.threadData[next_id]['start'] - self.threadData[next_id]['stop']
                            self.threadData[next_id]['cpuWait'] += preemptedTime

                            if preemptedTime > self.threadData[next_id]['maxPreempted']:
                                self.threadData[next_id]['maxPreempted'] = preemptedTime

                            try:
                                self.preemptData[SystemManager.preemptGroup.index(next_id)][0] = False
                            except:
                                return
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "irq_handler_entry":
                m = re.match(r'^\s*irq=(?P<irq>[0-9]+)\s+name=(?P<name>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    irqId = 'irq/' + d['irq']

                    # make list #
                    try:
                        self.irqData[irqId]
                    except:
                        self.irqData[irqId] = dict(self.init_irqData)

                    if self.irqData[irqId]['start'] > 0:
                        diff = float(time) - self.irqData[irqId]['start']
                        if diff > self.irqData[irqId]['max_period'] or self.irqData[irqId]['max_period'] <= 0:
                            self.irqData[irqId]['max_period'] = diff
                        if diff < self.irqData[irqId]['min_period'] or self.irqData[irqId]['min_period'] <= 0:
                            self.irqData[irqId]['min_period'] = diff

                    self.irqData[irqId]['start'] = float(time)
                    self.irqData[irqId]['name'] = d['name']
                    self.irqData[irqId]['count'] += 1
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "irq_handler_exit":
                m = re.match(r'^\s*irq=(?P<irq>[0-9]+)\s+ret=(?P<return>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    irqId = 'irq/' + d['irq']

                    # make list #
                    try:
                        self.irqData[irqId]
                    except:
                        self.irqData[irqId] = dict(self.init_irqData)

                    if self.irqData[irqId]['start'] > 0:
                        diff = float(time) - self.irqData[irqId]['start']
                        self.irqData[irqId]['usage'] += diff
                        self.threadData[thread]['irq'] += diff
                        if thread is not coreId:
                            self.threadData[coreId]['irq'] += diff

                        if diff > self.irqData[irqId]['max'] or self.irqData[irqId]['max'] <= 0:
                            self.irqData[irqId]['max'] = diff
                        if diff < self.irqData[irqId]['min'] or self.irqData[irqId]['min'] <= 0:
                            self.irqData[irqId]['min'] = diff
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "softirq_entry":
                m = re.match(r'^\s*vec=(?P<vector>[0-9]+)\s+\[action=(?P<action>\S+)\]', etc)
                if m is not None:
                    d = m.groupdict()

                    irqId = 'softirq/' + d['vector']

                    # make list #
                    try:
                        self.irqData[irqId]
                    except:
                        self.irqData[irqId] = dict(self.init_irqData)
                        self.irqData[irqId]['name'] = d['action']

                    if self.irqData[irqId]['start'] > 0:
                        diff = float(time) - self.irqData[irqId]['start']
                        if diff > self.irqData[irqId]['max_period'] or self.irqData[irqId]['max_period'] <= 0:
                            self.irqData[irqId]['max_period'] = diff
                        if diff < self.irqData[irqId]['min_period'] or self.irqData[irqId]['min_period'] <= 0:
                            self.irqData[irqId]['min_period'] = diff

                    self.irqData[irqId]['start'] = float(time)
                    self.irqData[irqId]['count'] += 1
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "softirq_exit":
                m = re.match(r'^\s*vec=(?P<vector>[0-9]+)\s+\[action=(?P<action>\S+)\]', etc)
                if m is not None:
                    d = m.groupdict()

                    irqId = 'softirq/' + d['vector']

                    # make list #
                    try:
                        self.irqData[irqId]
                    except:
                        self.irqData[irqId] = dict(self.init_irqData)
                        self.irqData[irqId]['name'] = d['action']

                    if self.irqData[irqId]['start'] > 0:
                        diff = float(time) - self.irqData[irqId]['start']
                        self.irqData[irqId]['usage'] += diff
                        self.threadData[thread]['irq'] += diff

                        if diff > self.irqData[irqId]['max'] or self.irqData[irqId]['max'] <= 0:
                            self.irqData[irqId]['max'] = diff
                        if diff < self.irqData[irqId]['min'] or self.irqData[irqId]['min'] <= 0:
                            self.irqData[irqId]['min'] = diff
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "sched_migrate_task":
                m = re.match(r'^\s*comm=(?P<comm>.*)\s+pid=(?P<pid>[0-9]+)\s+prio=(?P<prio>[0-9]+)\s+' + \
                    r'orig_cpu=(?P<orig_cpu>[0-9]+)\s+dest_cpu=(?P<dest_cpu>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    pid = d['pid']

                    try:
                        self.threadData[pid]
                    except:
                        self.threadData[pid] = dict(self.init_threadData)
                        self.threadData[pid]['comm'] = d['comm']

                    self.threadData[pid]['migrate'] += 1

                    # update core data for preempted info #
                    if SystemManager.preemptGroup != None:
                        try:
                            index = SystemManager.preemptGroup.index(thread)
                        except:
                            index = -1

                        if index >= 0:
                            self.preemptData[index][3] = core
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "mm_page_alloc":
                m = re.match(r'^\s*page=\s*(?P<page>\S+)\s+pfn=(?P<pfn>[0-9]+)\s+order=(?P<order>[0-9]+)\s+' + \
                    r'migratetype=(?P<mt>[0-9]+)\s+gfp_flags=(?P<flags>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    SystemManager.memEnable = True

                    # check whether it is huge page #
                    if d['page'] == '(null)':
                        page = 'huge'
                    else:
                        page = d['page']

                    pfn = int(d['pfn'])
                    flags = d['flags']
                    order = int(d['order'])

                    self.threadData[thread]['nrPages'] += pow(2, order)
                    self.threadData[coreId]['nrPages'] += pow(2, order)

                    if flags.find('NOFS') >= 0 or flags.find('GFP_WRITE') >= 0 or flags.find('0x1000000') >= 0:
                        pageType = 'CACHE'
                        self.threadData[thread]['cachePages'] += pow(2, order)
                        self.threadData[coreId]['cachePages'] += pow(2, order)
                    elif flags.find('USER') >= 0:
                        pageType = 'USER'
                        self.threadData[thread]['userPages'] += pow(2, order)
                        self.threadData[coreId]['userPages'] += pow(2, order)
                    else:
                        pageType = 'KERNEL'
                        self.threadData[thread]['kernelPages'] += pow(2, order)
                        self.threadData[coreId]['kernelPages'] += pow(2, order)

                    # make PTE in page table #
                    for cnt in range(0, pow(2, order)):
                        pfnv = pfn + cnt

                        try:
                            # this allocated page is not freed #
                            if self.pageTable[pfnv] == {}:
                                raise
                            else:
                                self.threadData[thread]['nrPages'] -= 1
                                self.threadData[coreId]['nrPages'] -= 1
                        except:
                            self.pageTable[pfnv] = dict(self.init_pageData)

                        self.pageTable[pfnv]['tid'] = thread
                        self.pageTable[pfnv]['page'] = page
                        self.pageTable[pfnv]['flags'] = flags
                        self.pageTable[pfnv]['type'] = pageType
                        self.pageTable[pfnv]['time'] = time
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "mm_page_free":
                m = re.match(r'^\s*page=(?P<page>\S+)\s+pfn=(?P<pfn>[0-9]+)\s+order=(?P<order>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    SystemManager.memEnable = True

                    page = d['page']
                    pfn = int(d['pfn'])
                    order = int(d['order'])

                    for cnt in range(0, pow(2, order)):
                        pfnv = pfn + cnt

                        try:
                            self.threadData[self.pageTable[pfnv]['tid']]['nrPages'] -= 1
                            self.threadData[coreId]['nrPages'] -= 1

                            if thread != self.pageTable[pfnv]['tid']:
                                self.threadData[self.pageTable[pfnv]['tid']]['reclaimedPages'] += 1
                                self.threadData[coreId]['reclaimedPages'] += 1

                            if self.pageTable[pfnv]['type'] is 'CACHE':
                                self.threadData[self.pageTable[pfnv]['tid']]['cachePages'] -= 1
                                self.threadData[coreId]['cachePages'] -= 1
                            elif self.pageTable[pfnv]['type'] is 'USER':
                                self.threadData[self.pageTable[pfnv]['tid']]['userPages'] -= 1
                                self.threadData[coreId]['userPages'] -= 1
                            elif self.pageTable[pfnv]['type'] is 'KERNEL':
                                self.threadData[self.pageTable[pfnv]['tid']]['kernelPages'] -= 1
                                self.threadData[coreId]['kernelPages'] -= 1

                            del self.pageTable[pfnv]
                            self.pageTable[pfnv] = {}
                        except:
                            # this page is allocated before starting profile #
                            self.threadData[thread]['anonReclaimedPages'] += 1
                            self.threadData[coreId]['anonReclaimedPages'] += 1
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "mm_filemap_delete_from_page_cache":
                m = re.match(r'^\s*dev (?P<major>[0-9]+):(?P<minor>[0-9]+) .+' + \
                    r'page=(?P<page>\S+)\s+pfn=(?P<pfn>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    SystemManager.memEnable = True

                    pfn = int(d['pfn'])

                    try:
                        # attribute of page is changed to file #
                        if self.pageTable[pfn]['type'] is 'USER':
                            self.threadData[self.pageTable[pfn]['tid']]['userPages'] -= 1
                            self.threadData[coreId]['userPages'] -= 1
                            self.threadData[self.pageTable[pfn]['tid']]['cachePages'] += 1
                            self.threadData[coreId]['cachePages'] += 1
                        elif self.pageTable[pfn]['type'] is 'KERNEL':
                            self.threadData[self.pageTable[pfn]['tid']]['kernelPages'] -= 1
                            self.threadData[coreId]['kernelPages'] -= 1
                            self.threadData[self.pageTable[pfn]['tid']]['cachePages'] += 1
                            self.threadData[coreId]['cachePages'] += 1

                        self.pageTable[pfn]['type'] = 'CACHE'
                    except:
                        return
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "kmalloc":
                m = re.match(r'^\s*call_site=(?P<caller>\S+)\s+ptr=(?P<ptr>\S+)\s+bytes_req=(?P<req>[0-9]+)\s+' + \
                    r'bytes_alloc=(?P<alloc>[0-9]+)\s+gfp_flags=(?P<flags>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    SystemManager.memEnable = True

                    caller = d['caller']
                    ptr = d['ptr']
                    req = int(d['req'])
                    alloc = int(d['alloc'])

                    try:
                        self.kmemTable[ptr]
                        # some allocated object is not freed #
                    except:
                        self.kmemTable[ptr] = dict(self.init_kmallocData)

                    self.kmemTable[ptr]['tid'] = thread
                    self.kmemTable[ptr]['caller'] = caller
                    self.kmemTable[ptr]['req'] = req
                    self.kmemTable[ptr]['alloc'] = alloc
                    self.kmemTable[ptr]['waste'] = alloc - req
                    self.kmemTable[ptr]['core'] = coreId

                    self.threadData[thread]['remainKmem'] += alloc
                    self.threadData[thread]['wasteKmem'] += alloc - req
                    self.threadData[coreId]['remainKmem'] += alloc
                    self.threadData[coreId]['wasteKmem'] += alloc - req
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "kfree":
                m = re.match(r'^\s*call_site=(?P<caller>\S+)\s+ptr=(?P<ptr>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    SystemManager.memEnable = True

                    caller = d['caller']
                    ptr = d['ptr']

                    try:
                        self.threadData[self.kmemTable[ptr]['tid']]['remainKmem'] -= \
                            self.kmemTable[ptr]['alloc']
                        self.threadData[self.kmemTable[ptr]['core']]['remainKmem'] -= \
                            self.kmemTable[ptr]['alloc']
                        self.threadData[self.kmemTable[ptr]['tid']]['wasteKmem'] -= \
                            self.kmemTable[ptr]['waste']
                        self.threadData[self.kmemTable[ptr]['core']]['wasteKmem'] -= \
                            self.kmemTable[ptr]['waste']

                        self.kmemTable[ptr] = {}
                        del self.kmemTable[ptr]
                    except:
                        '''
                        this allocated object is not logged or \
                        this object is allocated before starting profile
                        '''
                        return
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "sched_wakeup":
                m = re.match(r'^\s*comm=(?P<comm>.*)\s+pid=(?P<pid>[0-9]+)\s+prio=(?P<prio>[0-9]+)\s+' + \
                    r'target_cpu=(?P<target>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    target_comm = d['comm']
                    pid = d['pid']

                    if self.wakeupData['tid'] == '0':
                        self.wakeupData['time'] = float(time) - float(self.startTime)
                    elif thread[0] == '0' or pid == '0':
                        return
                    elif self.wakeupData['valid'] > 0 \
                        and (self.wakeupData['from'] != self.wakeupData['tid'] or self.wakeupData['to'] != pid):
                        if self.wakeupData['valid'] == 1 and self.wakeupData['corrupt'] == '0':
                            try:
                                kicker = self.threadData[self.wakeupData['tid']]['comm']
                            except:
                                kicker = "NULL"

                            kicker_pid = self.wakeupData['tid']
                        else:
                            kicker = self.threadData[thread]['comm']
                            kicker_pid = thread

                        self.depData.append("\t%.3f/%.3f \t%16s(%4s) -> %16s(%4s) \t%s" % \
                            (round(float(time) - float(self.startTime), 7), \
                             round(float(time) - float(self.startTime) - float(self.wakeupData['time']), 7), \
                             kicker, kicker_pid, target_comm, pid, "kick"))

                        self.wakeupData['time'] = float(time) - float(self.startTime)
                        self.wakeupData['from'] = self.wakeupData['tid']
                        self.wakeupData['to'] = pid
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "sys_enter":
                m = re.match(r'^\s*NR (?P<nr>[0-9]+) (?P<args>.+)', etc)
                if m is not None:
                    d = m.groupdict()

                    nr = d['nr']
                    args = d['args']

                    if nr == str(ConfigManager.sysList.index("sys_futex")):
                        n = re.match(r'^\s*(?P<uaddr>\S+), (?P<op>[0-9]+), (?P<val>\S+), (?P<timep>\S+),', d['args'])
                        if n is not None:
                            l = n.groupdict()

                            op = int(l['op']) % 10
                            if op == 0:
                                self.threadData[thread]['futexEnter'] = float(time)

                    if self.wakeupData['tid'] == '0':
                        self.wakeupData['time'] = float(time) - float(self.startTime)

                    if nr == str(ConfigManager.sysList.index("sys_write")):
                        self.wakeupData['tid'] = thread
                        self.wakeupData['nr'] = nr
                        self.wakeupData['args'] = args

                        if (self.wakeupData['valid'] > 0 and \
                            (self.wakeupData['tid'] == thread and \
                            self.wakeupData['from'] == comm)) is False:
                            self.wakeupData['valid'] += 1

                            if self.wakeupData['valid'] > 1:
                                self.wakeupData['corrupt'] = '1'
                            else:
                                self.wakeupData['corrupt'] = '0'

                    try:
                        self.threadData[thread]['syscallInfo']
                    except:
                        self.threadData[thread]['syscallInfo'] = {}
                    try:
                        self.threadData[thread]['syscallInfo'][nr]
                    except:
                        self.threadData[thread]['syscallInfo'][nr] = dict(self.init_syscallInfo)

                    self.threadData[thread]['syscallInfo'][nr]['last'] = float(time)

                    if len(SystemManager.syscallList) > 0:
                        try:
                            idx = SystemManager.syscallList.index(nr)
                        except:
                            idx = -1

                        if idx >= 0:
                            self.syscallData.append(['enter', time, thread, core, nr, args])
                    else:
                        self.syscallData.append(['enter', time, thread, core, nr, args])
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "sys_exit":
                m = re.match(r'^\s*NR (?P<nr>[0-9]+) = (?P<ret>.+)', etc)
                if m is not None:
                    d = m.groupdict()

                    nr = d['nr']
                    ret = d['ret']

                    if nr == str(ConfigManager.sysList.index("sys_futex")) and \
                        self.threadData[thread]['futexEnter'] > 0:
                        self.threadData[thread]['futexCnt'] += 1
                        futexTime = float(time) - self.threadData[thread]['futexEnter']
                        if futexTime > self.threadData[thread]['futexMax']:
                            self.threadData[thread]['futexMax'] = futexTime
                        self.threadData[thread]['futexTotal'] += futexTime
                        self.threadData[thread]['futexEnter'] = 0

                    try:
                        if SystemManager.depEnable is False:
                            raise
                        elif nr == str(ConfigManager.sysList.index("sys_write")) and \
                            self.wakeupData['valid'] > 0:
                            self.wakeupData['valid'] -= 1
                        elif nr == str(ConfigManager.sysList.index("sys_select")) or \
                            nr == str(ConfigManager.sysList.index("sys_poll")) or \
                            nr == str(ConfigManager.sysList.index("sys_epoll_wait")):
                            if (self.lastJob[core]['job'] == "sched_switch" or \
                                self.lastJob[core]['job'] == "sched_wakeup") and \
                                self.lastJob[core]['prevWakeupTid'] != thread:
                                self.depData.append("\t%.3f/%.3f \t%16s %4s     %16s(%4s) \t%s" % \
                                    (round(float(time) - float(self.startTime), 7), \
                                    round(float(time) - float(self.startTime) - float(self.wakeupData['time']), 7), \
                                    " ", " ", self.threadData[thread]['comm'], thread, "wakeup"))

                                self.wakeupData['time'] = float(time) - float(self.startTime)
                                self.lastJob[core]['prevWakeupTid'] = thread
                        elif nr == str(ConfigManager.sysList.index("sys_recv")):
                            if self.lastJob[core]['prevWakeupTid'] != thread:
                                self.depData.append("\t%.3f/%.3f \t%16s %4s     %16s(%4s) \t%s" % \
                                    (round(float(time) - float(self.startTime), 7), \
                                    round(float(time) - float(self.startTime) - float(self.wakeupData['time']), 7), \
                                    " ", " ", self.threadData[thread]['comm'], thread, "recv"))

                                self.wakeupData['time'] = float(time) - float(self.startTime)
                                self.lastJob[core]['prevWakeupTid'] = thread
                    except:
                        pass

                    try:
                        self.threadData[thread]['syscallInfo']
                    except:
                        self.threadData[thread]['syscallInfo'] = {}
                    try:
                        self.threadData[thread]['syscallInfo'][nr]
                    except:
                        self.threadData[thread]['syscallInfo'][nr] = dict(self.init_syscallInfo)

                    if self.threadData[thread]['syscallInfo'][nr]['last'] > 0:
                        diff = float(time) - self.threadData[thread]['syscallInfo'][nr]['last']
                        self.threadData[thread]['syscallInfo'][nr]['usage'] += diff
                        self.threadData[thread]['syscallInfo'][nr]['last'] = 0
                        self.threadData[thread]['syscallInfo'][nr]['count'] += 1

                        if self.threadData[thread]['syscallInfo'][nr]['max'] == 0 or \
                            self.threadData[thread]['syscallInfo'][nr]['max'] < diff:
                            self.threadData[thread]['syscallInfo'][nr]['max'] = diff
                        if self.threadData[thread]['syscallInfo'][nr]['min'] <= 0 or \
                            self.threadData[thread]['syscallInfo'][nr]['min'] > diff:
                            self.threadData[thread]['syscallInfo'][nr]['min'] = diff

                    if len(SystemManager.syscallList) > 0:
                        try:
                            idx = SystemManager.syscallList.index(nr)
                        except:
                            idx = -1

                        if idx >= 0:
                            self.syscallData.append(['exit', time, thread, core, nr, ret])
                    else:
                        self.syscallData.append(['exit', time, thread, core, nr, ret])
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "signal_generate":
                m = re.match(r'^\s*sig=(?P<sig>[0-9]+) errno=(?P<err>[0-9]+) ' + \
                        r'code=(?P<code>.*) comm=(?P<comm>.*) pid=(?P<pid>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    sig = d['sig']
                    target_comm = d['comm']
                    pid = d['pid']

                    self.depData.append("\t%.3f/%.3f \t%16s(%4s) -> %16s(%4s) \t%s(%s)" % \
                        (round(float(time) - float(self.startTime), 7), \
                        round(float(time) - float(self.startTime) - float(self.wakeupData['time']), 7), \
                        self.threadData[thread]['comm'], thread, target_comm, pid, "sigsend", sig))

                    self.sigData.append(('SEND', float(time) - float(self.startTime), \
                        self.threadData[thread]['comm'], thread, target_comm, pid, sig))

                    self.wakeupData['time'] = float(time) - float(self.startTime)

                    try:
                        # SIGCHLD #
                        if sig == str(ConfigManager.sigList.index('SIGCHLD')):
                            if self.threadData[pid]['waitStartAsParent'] > 0:
                                if self.threadData[pid]['waitPid'] == 0 or \
                                    self.threadData[pid]['waitPid'] == int(thread):
                                    diff = float(time) - self.threadData[pid]['waitStartAsParent']
                                    self.threadData[thread]['waitParent'] = diff
                                    self.threadData[pid]['waitChild'] += diff
                        elif sig == str(ConfigManager.sigList.index('SIGSEGV')):
                            self.threadData[pid]['die'] = 'F'
                    except:
                        return
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "signal_deliver":
                m = re.match(r'^\s*sig=(?P<sig>[0-9]+) errno=(?P<err>[0-9]+) code=(?P<code>.*) ' + \
                        r'sa_handler=(?P<handler>.*) sa_flags=(?P<flags>.*)', etc)
                if m is not None:
                    d = m.groupdict()

                    sig = d['sig']
                    flags = d['flags']

                    self.depData.append("\t%.3f/%.3f \t%16s %4s     %16s(%4s) \t%s(%s)" % \
                        (round(float(time) - float(self.startTime), 7), \
                        round(float(time) - float(self.startTime) - float(self.wakeupData['time']), 7), "", "", \
                        self.threadData[thread]['comm'], thread, "sigrecv", sig))

                    self.sigData.append(('RECV', float(time) - float(self.startTime), \
                        None, None, self.threadData[thread]['comm'], thread, sig))

                    self.wakeupData['time'] = float(time) - float(self.startTime)
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "block_bio_remap":
                m = re.match(r'^\s*(?P<major>[0-9]+),(?P<minor>[0-9]+)\s*(?P<operation>\S+)\s*' + \
                    r'(?P<address>\S+)\s+\+\s+(?P<size>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    if d['operation'][0] == 'R':

                        SystemManager.blockEnable = True

                        bio = d['major'] + '/' + d['minor'] + '/' + d['operation'][0] + '/' + d['address']

                        self.ioData[bio] = {'thread': thread, 'time': float(time), \
                            'major': d['major'], 'minor': d['minor'], \
                            'address': int(d['address']), 'size': int(d['size'])}

                        self.threadData[thread]['reqBlock'] += int(d['size'])
                        self.threadData[thread]['readQueueCnt'] += 1
                        self.threadData[thread]['readBlockCnt'] += 1
                        self.threadData[coreId]['readBlockCnt'] += 1
                        if self.threadData[thread]['readStart'] == 0:
                            self.threadData[thread]['readStart'] = float(time)
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "block_rq_complete":
                m = re.match(r'^\s*(?P<major>[0-9]+),(?P<minor>[0-9]+)\s*(?P<operation>\S+)' + \
                    r'\s*\(.*\)\s*(?P<address>\S+)\s+\+\s+(?P<size>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    address = d['address']
                    size = d['size']

                    bio = d['major'] + '/' + d['minor'] + '/' + d['operation'][0] + '/' + d['address']

                    try:
                        self.threadData[self.ioData[bio]['thread']] = self.threadData[self.ioData[bio]['thread']]
                        bioStart = int(address)
                        bioEnd = int(address) + int(size)
                    except:
                        return

                    for key, value in sorted(self.ioData.items(), key=lambda e: e[1]['address'], reverse=False):
                        if value['major'] == d['major'] and value['minor'] == d['minor']:
                            if bioStart <= value['address'] < bioEnd or \
                                bioStart < value['address'] + value['size'] <= bioEnd:

                                matchBlock = 0

                                if bioStart < value['address']:
                                    matchStart = value['address']
                                else:
                                    matchStart = bioStart

                                if bioEnd > value['address'] + value['size']:
                                    matchEnd = value['address'] + value['size']
                                else:
                                    matchEnd = bioEnd

                                if matchStart == value['address']:
                                    matchBlock = matchEnd - value['address']
                                    value['size'] = value['address'] + value['size'] - matchEnd
                                    value['address'] = matchEnd
                                elif matchStart > value['address']:
                                    if matchEnd == value['address'] + value['size']:
                                        matchBlock = matchEnd - matchStart
                                        value['size'] = matchStart - value['address']
                                    else:
                                        del value
                                        continue
                                else:
                                    del value
                                    continue

                                # just ignore error ;( #
                                if bioEnd < value['address'] + value['size']:
                                    pass

                                self.threadData[value['thread']]['readBlock'] += matchBlock
                                self.threadData[coreId]['readBlock'] += matchBlock

                                if value['size'] == 0:
                                    if self.threadData[value['thread']]['readQueueCnt'] > 0:
                                        self.threadData[value['thread']]['readQueueCnt'] -= 1

                                    """
                                    if error of size and time of block read is big then \
                                    consider inserting bellow condition
                                    # self.threadData[value['thread']]['readQueueCnt'] == 0 #
                                    """
                                    if self.threadData[value['thread']]['readStart'] > 0:
                                        waitTime = \
                                                float(time) - self.threadData[value['thread']]['readStart']
                                        self.threadData[coreId]['ioWait'] += waitTime
                                        self.threadData[value['thread']]['ioWait'] += waitTime
                                        self.threadData[value['thread']]['readStart'] = 0

                                    del value
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "writeback_dirty_page":
                m = re.match(r'^\s*bdi\s+(?P<major>[0-9]+):(?P<minor>[0-9]+):\s*' + \
                    r'ino=(?P<ino>\S+)\s+index=(?P<index>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    SystemManager.blockEnable = True

                    self.threadData[thread]['writeBlock'] += 1
                    self.threadData[thread]['writeBlockCnt'] += 1
                    self.threadData[coreId]['writeBlock'] += 1
                    self.threadData[coreId]['writeBlockCnt'] += 1
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "wbc_writepage":
                m = re.match(r'^\s*bdi\s+(?P<major>[0-9]+):(?P<minor>[0-9]+):\s*' + \
                    r'towrt=(?P<towrt>\S+)\s+skip=(?P<skip>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    if d['skip'] == '0':
                        SystemManager.blockEnable = True

                        self.threadData[thread]['writeBlock'] += 1
                        self.threadData[thread]['writeBlockCnt'] += 1
                        self.threadData[coreId]['writeBlock'] += 1
                        self.threadData[coreId]['writeBlockCnt'] += 1
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "mm_vmscan_wakeup_kswapd":
                try:
                    self.reclaimData[thread]
                except:
                    self.reclaimData[thread] = {'start': float(0)}

                if self.reclaimData[thread]['start'] <= 0:
                    self.reclaimData[thread]['start'] = float(time)

                self.threadData[thread]['reclaimCnt'] += 1

            elif func == "mm_vmscan_kswapd_sleep":
                for key, value in self.reclaimData.items():
                    try:
                        self.threadData[key]
                    except:
                        self.threadData[key] = dict(self.init_threadData)
                        self.threadData[key]['comm'] = comm

                    self.threadData[key]['reclaimWait'] += float(time) - float(value['start'])
                    del self.reclaimData[key]

            elif func == "mm_vmscan_direct_reclaim_begin":
                if self.threadData[thread]['dReclaimStart'] <= 0:
                    self.threadData[thread]['dReclaimStart'] = float(time)

                self.threadData[thread]['dReclaimCnt'] += 1
                self.threadData[coreId]['dReclaimCnt'] += 1

            elif func == "mm_vmscan_direct_reclaim_end":
                m = re.match(r'^\s*nr_reclaimed=(?P<nr>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    if self.threadData[thread]['dReclaimStart'] > 0:
                        self.threadData[thread]['dReclaimWait'] += \
                            float(time) - self.threadData[thread]['dReclaimStart']
                        self.threadData[coreId]['dReclaimWait'] += \
                            float(time) - self.threadData[thread]['dReclaimStart']

                    self.threadData[thread]['dReclaimStart'] = 0
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "task_newtask":
                m = re.match(r'^\s*pid=(?P<pid>[0-9]+)\s+comm=(?P<comm>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    pid = d['pid']

                    try:
                        self.threadData[pid]
                    except:
                        self.threadData[pid] = dict(self.init_threadData)
                        self.threadData[pid]['comm'] = d['comm']
                        self.threadData[pid]['ptid'] = thread
                        self.threadData[pid]['new'] = 'N'
                        self.threadData[pid]['createdTime'] = float(time)

                    if self.threadData[thread]['childList'] is None:
                        self.threadData[thread]['childList'] = list()

                    self.threadData[thread]['childList'].append(pid)
                    self.nrNewTask += 1
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "task_rename":
                m = re.match(r'^\s*pid=(?P<pid>[0-9]+)\s+oldcomm=(?P<oldcomm>.*)\s+' + \
                    r'newcomm=(?P<newcomm>.*)\s+oom_score_adj', etc)
                if m is not None:
                    d = m.groupdict()

                    pid = d['pid']
                    newcomm = d['newcomm']

                    try:
                        self.threadData[pid]
                    except:
                        self.threadData[pid] = dict(self.init_threadData)
                        self.threadData[pid]['comm'] = newcomm
                        self.threadData[pid]['ptid'] = thread

                    self.threadData[pid]['comm'] = newcomm
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "sched_process_exit":
                m = re.match(r'^\s*comm=(?P<comm>.*)\s+pid=(?P<pid>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    pid = d['pid']

                    try:
                        self.threadData[pid]
                    except:
                        self.threadData[pid] = dict(self.init_threadData)
                        self.threadData[pid]['comm'] = d['comm']
                        self.threadData[pid]['die'] = 'D'

                    if self.threadData[pid]['die'] != 'F':
                        self.threadData[pid]['die'] = 'D'
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "sched_process_wait":
                m = re.match(r'^\s*comm=(?P<comm>.*)\s+pid=(?P<pid>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    self.threadData[thread]['waitStartAsParent'] = float(time)
                    self.threadData[thread]['waitPid'] = int(d['pid'])
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "suspend_resume":
                state = None

                if etc.rfind("suspend_enter") > 0:
                    if etc.rfind("begin") > 0:
                        state = 'S'
                elif etc.rfind("machine_suspend") > 0:
                    if etc.rfind("end") > 0:
                        state = 'F'
                # Complete a PM transition for all non-sysdev devices #
                elif etc.rfind("dpm_resume_user") > 0:
                    if etc.rfind("end") > 0:
                        state = 'R'

                if state is not None:
                    self.suspendData.append([time, state])

            elif func == "module_load":
                m = re.match(r'^\s*(?P<module>.*)\s+(?P<address>.*)', etc)
                if m is not None:
                    d = m.groupdict()

                    module = d['module']
                    address = d['address']

                    self.moduleData.append(['load', thread, time, module, address])
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "module_free":
                m = re.match(r'^\s*(?P<module>.*)', etc)
                if m is not None:
                    d = m.groupdict()

                    module = d['module']

                    self.moduleData.append(['free', thread, time, module, None])
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "module_put":
                m = re.match(r'^\s*(?P<module>.*)\s+call_site=(?P<site>.*)\s+refcnt=(?P<refcnt>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    module = d['module']
                    refcnt = int(d['refcnt'])

                    self.moduleData.append(['put', thread, time, module, refcnt])
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "cpu_idle":
                m = re.match(r'^\s*state=(?P<state>[0-9]+)\s+cpu_id=(?P<cpu_id>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    tid = '0[' + d['cpu_id']+ ']'

                    if self.threadData[tid]['lastIdleStatus'] == int(d['state']):
                        return
                    else:
                        self.threadData[tid]['lastIdleStatus'] = int(d['state'])

                    if self.threadData[tid]['coreSchedCnt'] == 0 and self.threadData[tid]['offTime'] == 0:
                        self.threadData[tid]['offTime'] = float(time) - float(self.startTime)

                    # Wake core up, but the number 3 as this condition is not certain #
                    if int(d['state']) < 3:
                        self.threadData[tid]['offCnt'] += 1
                        self.threadData[tid]['lastOff'] = float(time)
                    # Start to sleep #
                    else:
                        if self.threadData[tid]['lastOff'] > 0:
                            self.threadData[tid]['offTime'] += (float(time) - self.threadData[tid]['lastOff'])
                            self.threadData[tid]['lastOff'] = float(0)
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "cpu_frequency":
                # toDo: calculate power consumption for DVFS system #
                return

            elif func == "console":
                m = re.match(r'^\s*\[\s*(?P<time>\S+)\s*\]\s+EVENT_(?P<event>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    event = d['event']

                    # initialize ThreadAnalyzer data #
                    if event == 'START':
                        self.threadData = {}
                        self.irqData = {}
                        self.ioData = {}
                        self.reclaimData = {}
                        self.pageTable = {}
                        self.kmemTable = {}
                        self.intervalData = []
                        self.depData = []
                        self.syscallData = []
                        self.lastJob = {}
                        self.preemptData = []
                        self.suspendData = []
                        self.markData = []
                        self.consoleData = []
                        self.startTime = time
                        return
                    # finish data processing #
                    elif event == 'STOP':
                        self.finishTime = time
                        self.stopFlag = True
                        return
                    # restart data processing #
                    elif event == 'RESTART':
                        self.threadDataOld = self.threadData
                        self.threadData = {}
                        self.irqDataOld = self.irqData
                        self.irqData = {}
                        self.ioDataOld = self.ioData
                        self.ioData = {}
                        self.reclaimDataOld = self.reclaimData
                        self.reclaimData = {}

                        self.totalTimeOld = round(float(time) - float(self.startTime), 7)
                        self.startTime = time
                        return
                    # save mark event #
                    elif event == 'MARK':
                        self.markData.append(time)

                    ei.addEvent(time, event)
                else:
                    self.consoleData.append([d['thread'], core, time, etc])

            elif func == "tracing_mark_write":
                m = re.match(r'^\s*EVENT_(?P<event>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    event = d['event']

                    # initialize ThreadAnalyzer data #
                    if event == 'START':
                        self.threadData = {}
                        self.irqData = {}
                        self.ioData = {}
                        self.reclaimData = {}
                        self.pageTable = {}
                        self.kmemTable = {}
                        self.intervalData = []
                        self.depData = []
                        self.syscallData = []
                        self.lastJob = {}
                        self.preemptData = []
                        self.suspendData = []
                        self.markData = []
                        self.consoleData = []
                        self.startTime = time
                        return
                    # finish data processing #
                    elif event == 'STOP':
                        self.finishTime = time
                        self.stopFlag = True
                        return
                    # restart data processing #
                    elif event == 'RESTART':
                        self.threadDataOld = self.threadData
                        self.threadData = {}
                        self.irqDataOld = self.irqData
                        self.irqData = {}
                        self.ioDataOld = self.ioData
                        self.ioData = {}
                        self.reclaimDataOld = self.reclaimData
                        self.reclaimData = {}

                        self.totalTimeOld = round(float(time) - float(self.startTime), 7)
                        self.startTime = time
                        return
                    # save mark event #
                    elif event == 'MARK':
                        self.markData.append(time)

                    ei.addEvent(time, event)
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

        else:
            # handle modified type of event #
            if SystemManager.tgidEnable is True:
                m = re.match(r'^\s*(?P<comm>.+)-(?P<thread>[0-9]+)\s+\(\s*(?P<tgid>\S+)\)\s+' + \
                    r'\[(?P<core>[0-9]+)\]\s+(?P<time>\S+):\s+(?P<func>.+):(?P<etc>.+)', string)
            else:
                m = re.match(r'^\s*(?P<comm>.+)-(?P<thread>[0-9]+)\s+\[(?P<core>[0-9]+)\]\s+' + \
                    r'(?P<time>\S+):\s+(?P<func>.+):(?P<etc>.+)', string)

            if m is not None:
                d = m.groupdict()
                comm = d['comm']
                core = str(int(d['core']))
                func = d['func']
                etc = d['etc']
                time = d['time']

                if func.find("tracing_mark_write") >= 0:
                    m = re.match(r'^\s*EVENT_(?P<event>\S+)', etc)
                    if m is not None:
                        d = m.groupdict()

                        event = d['event']

                        # initialize ThreadAnalyzer data #
                        if event == 'START':
                            self.threadData = {}
                            self.irqData = {}
                            self.ioData = {}
                            self.reclaimData = {}
                            self.pageTable = {}
                            self.kmemTable = {}
                            self.intervalData = []
                            self.depData = []
                            self.syscallData = []
                            self.lastJob = {}
                            self.preemptData = []
                            self.suspendData = []
                            self.markData = []
                            self.consoleData = []
                            self.startTime = time
                            return
                        # finish data processing #
                        elif event == 'STOP':
                            self.finishTime = time
                            self.stopFlag = True
                            return
                        # restart data processing #
                        elif event == 'RESTART':
                            self.threadDataOld = self.threadData
                            self.threadData = {}
                            self.irqDataOld = self.irqData
                            self.irqData = {}
                            self.ioDataOld = self.ioData
                            self.ioData = {}
                            self.reclaimDataOld = self.reclaimData
                            self.reclaimData = {}

                            self.totalTimeOld = round(float(time) - float(self.startTime), 7)
                            self.startTime = time
                            return
                        # saving mark event #
                        elif event == 'MARK':
                            self.markData.append(time)

                        ei.addEvent(time, event)



    def compareThreadData(self):
        for key, value in sorted(ti.threadData.items(), key=lambda e: e[1]['usage'], reverse=True):
            newPercent = round(float(value['usage']) / float(ti.totalTime), 7) * 100

            try:
                ti.threadDataOld[key]
            except:
                if int(newPercent) < 1:
                    del ti.threadData[key]
                continue

            oldPercent = round(float(ti.threadDataOld[key]['usage']) / float(ti.totalTimeOld), 7) * 100
            if int(oldPercent) >= int(newPercent) or int(newPercent) < 1:
                del ti.threadData[key]



    def saveProcs(self):
        # save cpu info #
        try:
            cpuBuf = None
            SystemManager.statFd.seek(0)
            cpuBuf = SystemManager.statFd.readlines()
        except:
            try:
                cpuPath = os.path.join(SystemManager.procPath, 'stat')
                SystemManager.statFd = open(cpuPath, 'r')
                cpuBuf = SystemManager.statFd.readlines()
            except:
                SystemManager.printWarning('Fail to open %s' % cpuPath)

        if cpuBuf is not None:
            self.prevCpuData = self.cpuData
            self.cpuData = {}

            for line in cpuBuf:
                statList = line.split()
                cpuId = statList[0]
                if cpuId == 'cpu':
                    try:
                        self.cpuData['all']
                    except:
                        # stat list from http://man7.org/linux/man-pages/man5/proc.5.html #
                        self.cpuData['all'] = {'user': long(statList[1]), \
                            'nice': long(statList[2]), 'system': long(statList[3]), \
                            'idle': long(statList[4]), 'iowait': long(statList[5]), \
                            'irq': long(statList[6]), 'softirq': long(statList[7])}
                elif cpuId.rfind('cpu') == 0:
                    try:
                        self.cpuData[int(cpuId[3:])]
                    except:
                        self.cpuData[int(cpuId[3:])] = {'user': long(statList[1]), \
                            'nice': long(statList[2]), 'system': long(statList[3]), \
                            'idle': long(statList[4]), 'iowait': long(statList[5]), \
                            'irq': long(statList[6]), 'softirq': long(statList[7])}
                else:
                    try:
                        self.cpuData[cpuId]
                    except:
                        self.cpuData[cpuId] = {cpuId: long(statList[1])}

        # save vmstat info #
        try:
            vmBuf = None
            SystemManager.vmstatFd.seek(0)
            vmBuf = SystemManager.vmstatFd.readlines()
        except:
            try:
                vmstatPath = os.path.join(SystemManager.procPath, 'vmstat')
                SystemManager.vmstatFd = open(vmstatPath, 'r')

                # vmstat list from https://access.redhat.com/solutions/406773 #
                vmBuf = SystemManager.vmstatFd.readlines()
            except:
                SystemManager.printWarning('Fail to open %s' % vmstatPath)

        if vmBuf is not None:
            self.prevVmData = self.vmData
            self.vmData = {}

            for line in vmBuf:
                vmList = line.split()
                self.vmData[vmList[0]] = long(vmList[1])

        # save swaps info #
        try:
            swapBuf = None
            SystemManager.swapFd.seek(0)
            swapBuf = SystemManager.swapFd.readlines()
        except:
            try:
                swapPath = os.path.join(SystemManager.procPath, 'swaps')
                SystemManager.swapFd = open(swapPath, 'r')

                swapBuf = SystemManager.swapFd.readlines()
            except:
                SystemManager.printWarning('Fail to open %s' % swapPath)

        if swapBuf is not None:
            swapTotal = 0
            swapUsed = 0

            for line in swapBuf:
                swapList = line.split()
                # swapList = [Filename, Type, Size, Used, Priority] #
                try:
                    swapTotal += int(swapList[2])
                    swapUsed += int(swapList[3])
                except:
                    continue

            self.vmData['swapTotal'] = swapTotal
            self.vmData['swapUsed'] = swapUsed

        # save uptime #
        try:
            SystemManager.uptimeFd.seek(0)
            SystemManager.prevUptime = SystemManager.uptime
            SystemManager.uptime = float(SystemManager.uptimeFd.readline().split()[0])
            SystemManager.uptimeDiff = SystemManager.uptime - SystemManager.prevUptime
            SystemManager.uptimeFd.flush()
        except:
            try:
                uptimePath = os.path.join(SystemManager.procPath, 'uptime')
                SystemManager.uptimeFd = open(uptimePath, 'r')

                SystemManager.uptime = float(SystemManager.uptimeFd.readline().split()[0])
                SystemManager.uptimeFd.flush()
            except:
                SystemManager.printWarning('Fail to open %s' % uptimePath)

        # get process list in proc directory #
        try:
            pids = os.listdir(SystemManager.procPath)
        except:
            SystemManager.printError('Fail to open %s' % SystemManager.procPath)
            sys.exit(0)

        # get thread list in proc directory #
        for pid in pids:
            try:
                int(pid)
            except:
                continue

            # make path of tid #
            procPath = os.path.join(SystemManager.procPath, pid)
            taskPath = os.path.join(procPath, 'task')

            # save info per process #
            if SystemManager.processEnable is True:
                # make process object with constant value #
                self.procData[pid] = dict(self.init_procData)
                self.procData[pid]['mainID'] = int(pid)
                self.procData[pid]['taskPath'] = procPath

                # save stat of process #
                self.saveProcData(procPath, pid)

                continue

            # save info per thread #
            try:
                tids = os.listdir(taskPath)
            except:
                SystemManager.printWarning('Fail to open %s' % taskPath)
                continue

            for tid in tids:
                try:
                    int(tid)
                except:
                    continue

                threadPath = os.path.join(taskPath, tid)

                # make process object with constant value #
                self.procData[tid] = dict(self.init_procData)
                self.procData[tid]['mainID'] = int(pid)
                self.procData[tid]['taskPath'] = threadPath

                # main thread #
                if pid == tid:
                    self.procData[tid]['isMain'] = True
                    self.procData[tid]['tids'] = []
                # sibling thread #
                else:
                    try:
                        self.procData[pid]['tids'].append(tid)
                    except:
                        self.procData[pid] = dict(self.init_procData)
                        self.procData[pid]['tids'] = []
                        self.procData[pid]['tids'].append(tid)

                # save stat of thread #
                self.saveProcData(threadPath, tid)



    def saveProcStatusData(self, path, tid):
        # save status info #
        try:
            self.prevProcData[tid]['statusFd'].seek(0)
            self.procData[tid]['statusFd'] = self.prevProcData[tid]['statusFd']
            self.procData[tid]['statusFd'].flush()
            statusBuf = self.procData[tid]['statusFd'].readlines()
        except:
            try:
                statusPath = os.path.join(path, 'status')
                self.procData[tid]['statusFd'] = open(statusPath, 'r')
                statusBuf = self.procData[tid]['statusFd'].readlines()

                # fd resource is about to run out #
                if SystemManager.maxFd - 16 < self.procData[tid]['statusFd'].fileno():
                    self.procData[tid]['statusFd'].close()
                    self.procData[tid]['statusFd'] = None
            except:
                SystemManager.printWarning('Fail to open %s' % statusPath)
                del self.procData[tid]
                return

        if self.procData[tid]['status'] is None:
            self.procData[tid]['status'] = {}

        for line in statusBuf:
            statusList = line.split(':')
            self.procData[tid]['status'][statusList[0]] = statusList[1].strip()



    def saveProcData(self, path, tid):
        # save stat info #
        try:
            self.prevProcData[tid]['statFd'].seek(0)
            self.procData[tid]['statFd'] = self.prevProcData[tid]['statFd']
            self.procData[tid]['statFd'].flush()
            statBuf = self.procData[tid]['statFd'].readline()
            self.prevProcData[tid]['alive'] = True
        except:
            try:
                statPath = os.path.join(path, 'stat')
                self.procData[tid]['statFd'] = open(statPath, 'r')
                statBuf = self.procData[tid]['statFd'].readline()

                # fd resource is about to run out #
                if SystemManager.maxFd - 16 < self.procData[tid]['statFd'].fileno():
                    self.procData[tid]['statFd'].close()
                    self.procData[tid]['statFd'] = None
            except:
                SystemManager.printWarning('Fail to open %s' % statPath)
                del self.procData[tid]
                return

        statList = statBuf.split()

        # merge comm parts that splited by space #
        commIndex = ConfigManager.statList.index("COMM")
        if statList[commIndex][-1] != ')':
            idx = ConfigManager.statList.index("COMM") + 1
            while True:
                statList[commIndex] += ' ' + str(statList[idx])
                if statList[idx].rfind(')') > -1:
                    statList.pop(idx)
                    break
                statList.pop(idx)

        # convert type of values #
        self.procData[tid]['stat'] = statList
        statList[self.minfltIdx] = long(statList[self.minfltIdx])
        statList[self.majfltIdx] = long(statList[self.majfltIdx])
        statList[self.utimeIdx] = long(statList[self.utimeIdx])
        statList[self.stimeIdx] = long(statList[self.stimeIdx])
        statList[self.btimeIdx] = long(statList[self.btimeIdx])
        statList[self.cutimeIdx] = long(statList[self.cutimeIdx])
        statList[self.cstimeIdx] = long(statList[self.cstimeIdx])

        # save io info #
        if SystemManager.diskEnable is True:
            try:
                self.prevProcData[tid]['ioFd'].seek(0)
                self.procData[tid]['ioFd'] = self.prevProcData[tid]['ioFd']
                self.procData[tid]['ioFd'].flush()
                ioBuf = self.procData[tid]['ioFd'].readlines()
                self.prevProcData[tid]['alive'] = True
            except:
                try:
                    ioPath = os.path.join(path, 'io')
                    self.procData[tid]['ioFd'] = open(ioPath, 'r')
                    ioBuf = self.procData[tid]['ioFd'].readlines()

                    # fd resource is about to run out #
                    if SystemManager.maxFd - 16 < self.procData[tid]['ioFd'].fileno():
                        self.procData[tid]['ioFd'].close()
                        self.procData[tid]['ioFd'] = None
                except:
                    SystemManager.printWarning('Fail to open %s' % ioPath)
                    del self.procData[tid]
                    return

            for line in ioBuf:
                line = line.split()
                if line[0] == 'read_bytes:':
                    try:
                        self.procData[tid]['io']['read_bytes'] = line[1]
                    except:
                        self.procData[tid]['io'] = {}
                        self.procData[tid]['io']['read_bytes'] = line[1]
                elif line[0] == 'write_bytes:':
                    try:
                        self.procData[tid]['io']['write_bytes'] = line[1]
                    except:
                        self.procData[tid]['io'] = {}
                        self.procData[tid]['io']['write_bytes'] = line[1]



    def printSystemUsage(self):
        try:
            freeMem = self.vmData['nr_free_pages'] * 4 / 1024
        except:
            freeMem = 'NA'
        try:
            freeDiffMem = (self.vmData['nr_free_pages'] - self.prevVmData['nr_free_pages']) * 4 / 1024
        except:
            freeDiffMem = 'NA'

        try:
            anonMem = (self.vmData['nr_anon_pages'] - self.prevVmData['nr_anon_pages']) * 4 / 1024
        except:
            anonMem = 'NA'
        try:
            fileMem = (self.vmData['nr_file_pages'] - self.prevVmData['nr_file_pages']) * 4 / 1024
        except:
            fileMem = 'NA'

        '''
        try:
            anonInMem = (self.vmData['nr_inactive_anon'] - self.prevVmData['nr_inactive_anon']) * 4 / 1024
        except:
            anonInMem = 'NA'
        try:
            anonAcMem = (self.vmData['nr_active_anon'] - self.prevVmData['nr_active_anon']) * 4 / 1024
        except:
            anonAcMem = 'NA'

        try:
            fileInMem = (self.vmData['nr_inactive_file'] - self.prevVmData['nr_inactive_file']) * 4 / 1024
        except:
            fileInMem = 'NA'
        try:
            fileAcMem = (self.vmData['nr_active_file'] - self.prevVmData['nr_active_file']) * 4 / 1024
        except:
            fileAcMem = 'NA'
        '''

        try:
            slabReclm = (self.vmData['nr_slab_reclaimable'] - self.prevVmData['nr_slab_reclaimable'])
        except:
            slabReclm = 'NA'
        try:
            slabUnReclm = (self.vmData['nr_slab_unreclaimable'] - self.prevVmData['nr_slab_unreclaimable'])
        except:
            slabUnReclm = 'NA'
        try:
            slabMem = (slabReclm + slabUnReclm) * 4 / 1024
        except:
            slabMem = 'NA'

        try:
            majFaultMem = (self.vmData['pgmajfault'] - self.prevVmData['pgmajfault'])
        except:
            majFaultMem = 'NA'
        '''
        try:
            faultMem = (self.vmData['pgfault'] - self.prevVmData['pgfault'])
        except:
            faultMem = 'NA'
        try:
            minFaultMem = faultMem - majFaultMem
        except:
            minFaultMem = 'NA'
        '''

        # paged in/out from/to disk #
        try:
            pgInMem = (self.vmData['pgpgin'] - self.prevVmData['pgpgin']) / 1024
        except:
            pgInMem = 'NA'
        try:
            pgOutMem = (self.vmData['pgpgout'] - self.prevVmData['pgpgout']) / 1024
        except:
            pgOutMem = 'NA'

        '''
        try:
            swapTotal = (self.vmData['swapTotal'] - self.prevVmData['swapTotal']) / 1024
        except:
            swapTotal = 'NA'
        '''
        try:
            swapFree = self.vmData['swapUsed'] / 1024
        except:
            swapFree = 'NA'
        try:
            swapUsed = (self.vmData['swapUsed'] - self.prevVmData['swapUsed']) / 1024
        except:
            swapUsed = 'NA'
        try:
            swapInMem = (self.vmData['pswpin'] - self.prevVmData['pswpin']) / 1024
        except:
            swapInMem = 'NA'
        try:
            swapOutMem = (self.vmData['pswpout'] - self.prevVmData['pswpout']) / 1024
        except:
            swapOutMem = 'NA'

        '''
        try:
            nrBgReclaim = (self.vmData['pageoutrun'] - self.prevVmData['pageoutrun'])
        except:
            nrBgReclaim = 'NA'
        '''
        try:
            bgReclaimNormal = (self.vmData['pgsteal_kswapd_normal'] - \
                self.prevVmData['pgsteal_kswapd_normal'])
        except:
            bgReclaimNormal = 0
        try:
            bgReclaimHigh = (self.vmData['pgsteal_kswapd_high'] - \
                self.prevVmData['pgsteal_kswapd_high'])
        except:
            bgReclaimHigh = 0
        try:
            bgReclaim = (bgReclaimNormal + bgReclaimHigh) * 4 / 1024
        except:
            bgReclaim = 'NA'

        '''
        try:
            nrDrReclaim = (self.vmData['allocstall'] - self.prevVmData['allocstall'])
        except:
            nrDrReclaim = 'NA'
        '''
        try:
            drReclaimNormal = (self.vmData['pgsteal_direct_normal'] - \
                self.prevVmData['pgsteal_direct_normal'])
        except:
            drReclaimNormal = 0
        try:
            drReclaimHigh = (self.vmData['pgsteal_direct_high'] - \
                self.prevVmData['pgsteal_direct_high'])
        except:
            drReclaimHigh = 0
        try:
            drReclaim = (drReclaimNormal + drReclaimHigh) * 4 / 1024
        except:
            drReclaim = 'NA'

        try:
            mlockMem = self.vmData['nr_mlock'] * 4 / 1024
        except:
            mlockMem = 'NA'

        '''
        try:
            mappedMem = self.vmData['nr_mapped'] * 4 / 1024
        except:
            mappedMem = 'NA'
        try:
            shMem = self.vmData['nr_shmem'] * 4 / 1024
        except:
            shMem = 'NA'
        '''

        SystemManager.addPrint(twoLine + '\n')
        SystemManager.addPrint(("{0:^7}|{1:^5}({2:^3}/{3:^3}/{4:^3}/{5:^3})|{6:^5}({7:^4}/{8:^4}/{9:^4}/{10:^4})|" + \
            "{11:^6}({12:^4}/{13:^7})|{14:^10}|{15:^7}|{16:^7}|{17:^7}|\n").\
            format("ID", "CPU", "Usr", "Ker", "Blk", "IRQ", "Mem", "Free", "Anon", "File", "Slab", \
            "Swap", "Used", "InOut", "RclmBgDr", "BlkRW", "NrFlt", "Mlock"))
        SystemManager.addPrint(oneLine + '\n')

        # set biggest core number #
        for idx, val in sorted(self.cpuData.items(), reverse=False):
            try:
                SystemManager.maxCore = int(idx)
            except:
                continue

        maxCore = SystemManager.maxCore + 1
        interval = SystemManager.uptimeDiff

        # print total cpu usage #
        nowData = self.cpuData['all']
        prevData = self.prevCpuData['all']

        userUsage = \
            int(((nowData['user'] - prevData['user'] + nowData['nice'] - prevData['nice']) / maxCore) / interval)
        kerUsage = int(((nowData['system'] - prevData['system']) / maxCore) / interval)
        irqUsage = \
            int(((nowData['irq'] - prevData['irq'] + nowData['softirq'] - prevData['softirq']) / maxCore) / interval)
        ioUsage = int(((nowData['iowait'] - prevData['iowait']) / maxCore) / interval)

        totalUsage = int(userUsage + kerUsage + irqUsage + ioUsage)

        totalCoreStat = ("{0:<7}|{1:>5}({2:^3}/{3:^3}/{4:^3}/{5:^3})|{6:^5}({7:^4}/{8:^4}/{9:^4}/{10:^4})|" + \
            "{11:^6}({12:^4}/{13:^7})|{14:^10}|{15:^7}|{16:^7}|{17:^7}|\n").\
            format("Total", \
            str(totalUsage) + ' %', userUsage, kerUsage, ioUsage, irqUsage, \
            freeMem, freeDiffMem, anonMem, fileMem, slabMem, \
            swapFree, swapUsed, str(swapInMem) + '/' + str(swapOutMem), \
            str(bgReclaim) + '/' + str(drReclaim), \
            str(pgInMem) + '/' + str(pgOutMem), majFaultMem, mlockMem)

        SystemManager.addPrint(totalCoreStat)

        # print each cpu usage #
        if SystemManager.showAll is True:
            SystemManager.addPrint(oneLine + '\n')

            for idx, value in sorted(self.cpuData.items(), reverse=False):
                nowData = self.cpuData[idx]
                prevData = self.prevCpuData[idx]

                try:
                    int(idx)

                    userUsage = int((nowData['user'] - prevData['user'] + \
                        nowData['nice'] - prevData['nice']) / interval)
                    kerUsage = int((nowData['system'] - prevData['system']) / interval)
                    ioUsage = int((nowData['iowait'] - prevData['iowait']) / interval)
                    irqUsage = int((nowData['irq'] - prevData['irq'] + \
                        nowData['softirq'] - prevData['softirq']) / interval)
                    totalUsage = userUsage + kerUsage + ioUsage + irqUsage

                    # limit total usage of each cpus #
                    if totalUsage > 100:
                        totalUsage = 100

                    # limit total usage of each modes #
                    if userUsage > 100:
                        userUsage = 100
                    elif kerUsage > 100:
                        kerUsage = 100

                    coreStat = "{0:<7}|{1:>5}({2:^3}/{3:^3}/{4:^3}/{5:^3})|".\
                        format("Core/" + str(idx), str(totalUsage) + ' %', userUsage, kerUsage, ioUsage, irqUsage)

                    # print graph of per-core usage #
                    if totalUsage > 0:
                        coreGraph = '#' * ((len(totalCoreStat) - len(coreStat) - 2) * totalUsage / 100)
                        coreGraph += (' ' * (len(totalCoreStat) - len(coreStat) - len(coreGraph) - 2))
                    else:
                        coreGraph = ' ' * int(len(totalCoreStat) - len(coreStat) - 2)

                    SystemManager.addPrint(coreStat + coreGraph + '|\n')
                except:
                    continue



    def printProcUsage(self):
        procCnt = 0
        dieCnt = 0
        interval = SystemManager.uptimeDiff

        # calculate diff between previous and now #
        for pid, value in self.procData.items():
            try:
                nowData = value['stat']
                prevData = self.prevProcData[pid]['stat']

                value['runtime'] = int(SystemManager.uptime - (float(value['stat'][self.runtimeIdx]) / 100))
                value['minflt'] = nowData[self.minfltIdx] - prevData[self.minfltIdx]
                value['majflt'] = nowData[self.majfltIdx] - prevData[self.majfltIdx]
                value['utime'] = int((nowData[self.utimeIdx] - prevData[self.utimeIdx]) / interval)
                value['stime'] = int((nowData[self.stimeIdx] - prevData[self.stimeIdx]) / interval)
                value['ttime'] = value['utime'] + value['stime']
                value['cutime'] = int((nowData[self.cutimeIdx] - prevData[self.cutimeIdx]) / interval)
                value['cstime'] = int((nowData[self.cstimeIdx] - prevData[self.cstimeIdx]) / interval)
                value['cttime'] = value['cutime'] + value['cstime']
                value['btime'] = int((nowData[self.btimeIdx] - prevData[self.btimeIdx]) / interval)

                if value['io'] is not None:
                    value['read'] = long(value['io']['read_bytes']) - \
                            long(self.prevProcData[pid]['io']['read_bytes'])
                    value['write'] = long(value['io']['write_bytes']) - \
                            long(self.prevProcData[pid]['io']['write_bytes'])
            except:
                value['new'] = True
                value['runtime'] = int(SystemManager.uptime - (float(value['stat'][self.runtimeIdx]) / 100))
                value['minflt'] = nowData[self.minfltIdx]
                value['majflt'] = nowData[self.majfltIdx]
                value['utime'] = int(nowData[self.utimeIdx] / interval)
                value['stime'] = int(nowData[self.stimeIdx] / interval)
                value['cutime'] = int(nowData[self.cutimeIdx] / interval)
                value['cstime'] = int(nowData[self.cstimeIdx] / interval)
                value['btime'] = int(nowData[self.btimeIdx] / interval)
                value['ttime'] = value['utime'] + value['stime']

                if value['io'] is not None:
                    value['read'] = long(value['io']['read_bytes'])
                    value['write'] = long(value['io']['write_bytes'])

        # get profile mode #
        if SystemManager.processEnable is True:
            mode = 'Process'
        else:
            mode = 'Thread'

        SystemManager.addPrint(twoLine + '\n')
        SystemManager.addPrint(\
            ("{0:^16} ({1:^5}/{2:^5}/{3:^4}/{4:>4})| {5:^3}({6:^3}/{7:^3}/{8:^3})| " + \
            "{9:>4}({10:^3}/{11:^3}/{12:^3}/{13:^3})| {14:^3}({15:^4}/{16:^4}/{17:^5})|{18:>9}|\n").\
            format(mode, "ID", "Pid", "Nr", "Pri", "CPU", "Usr", "Ker", "WFC", \
            "Mem", "RSS", "Txt", "Lib", "Swp", "Blk", "RD", "WR", "NrFlt", "LifeTime"))

        SystemManager.addPrint(oneLine + '\n')

        # set sort value #
        if SystemManager.sort == 'm':
            sortedProcData = sorted(self.procData.items(), \
                key=lambda e: long(e[1]['stat'][self.rssIdx]), reverse=True)
        elif SystemManager.sort == 'b':
            sortedProcData = sorted(self.procData.items(), \
                key=lambda e: e[1]['btime'], reverse=True)
        elif SystemManager.sort == 'w':
            sortedProcData = sorted(self.procData.items(), \
                key=lambda e: e[1]['cttime'], reverse=True)
        else:
            # set cpu usage as default #
            sortedProcData = sorted(self.procData.items(), \
                key=lambda e: e[1]['ttime'], reverse=True)

        # print process usage sorted by cpu usage #
        for idx, value in sortedProcData:
            # filter #
            if SystemManager.showGroup != []:
                found = False
                for val in SystemManager.showGroup:
                    if value['stat'][self.commIdx].rfind(val) > -1 or idx == val:
                        found = True
                        break
                if found is False:
                    continue

            # cut by rows of terminal #
            if int(SystemManager.bufferRows) >= int(SystemManager.ttyRows) - 5 and \
                    SystemManager.printFile is None:
                return

            # set sort value #
            if SystemManager.sort == 'c' or SystemManager.sort is None:
                targetValue = value['ttime']
            elif SystemManager.sort == 'm':
                targetValue = long(value['stat'][self.rssIdx]) * 4 / 1024
            elif SystemManager.sort == 'b':
                targetValue = value['btime']
            elif SystemManager.sort == 'w':
                targetValue = value['cttime']

            # check limit #
            if SystemManager.showGroup == [] and SystemManager.showAll is False and targetValue == 0:
                break

            if value['new'] is True:
                comm = '*' + value['stat'][self.commIdx][1:-1]
            else:
                comm = value['stat'][self.commIdx][1:-1]

            if SystemManager.processEnable is True:
                pid = value['stat'][self.ppidIdx]
                stackSize = (long(value['stat'][self.sstackIdx]) - \
                    long(value['stat'][self.estackIdx])) / 1024 / 1024
            else:
                pid = value['mainID']
                stackSize = '-'

            codeSize = (long(value['stat'][self.ecodeIdx]) - \
                long(value['stat'][self.scodeIdx])) / 1024 / 1024

            if ConfigManager.schedList[int(value['stat'][self.policyIdx])] == 'C':
                schedValue = "%3d" % (int(value['stat'][self.prioIdx]) - 20)
            else:
                schedValue = "%3d" % (abs(int(value['stat'][self.prioIdx]) + 1))

            runtimeSec = value['runtime']
            runtimeMin = runtimeSec / 60
            runtimeHour = runtimeMin / 60
            if runtimeHour > 0:
                runtimeMin %= 60
            runtimeSec %= 60
            lifeTime = "%3d:%2d:%2d" % (runtimeHour, runtimeMin, runtimeSec)

            # save status info to get memory status #
            self.saveProcStatusData(value['taskPath'], idx)

            try:
                vmlib = long(value['status']['VmLib'][:value['status']['VmLib'].find(' kb') - 1]) / 1024
            except:
                vmlib = '-'
            try:
                vmswp = long(value['status']['VmSwap'][:value['status']['VmSwap'].find(' kb') - 1]) / 1024
            except:
                vmswp = '-'

            if SystemManager.diskEnable is True:
                readSize = value['read'] / 1024 / 1024
                writeSize = value['write'] / 1024 / 1024
            else:
                readSize = '-'
                writeSize = '-'

            SystemManager.addPrint(\
                ("{0:>16} ({1:>5}/{2:>5}/{3:>4}/{4:>4})| {5:>3}({6:>3}/{7:>3}/{8:>3})| " + \
                "{9:>4}({10:>3}/{11:>3}/{12:>3}/{13:>3})| {14:>3}({15:>4}/{16:>4}/{17:>5})|{18:>9}|\n").\
                format(comm, idx, pid, value['stat'][self.nrthreadIdx], \
                ConfigManager.schedList[int(value['stat'][self.policyIdx])] + str(schedValue), \
                value['ttime'], value['utime'], value['stime'], int(value['cttime']), \
                long(value['stat'][self.vsizeIdx]) / 1024 / 1024, \
                long(value['stat'][self.rssIdx]) * 4 / 1024, codeSize, vmlib, vmswp, \
                value['btime'], readSize, writeSize, value['majflt'], lifeTime))
            procCnt += 1

        if procCnt == 0:
            SystemManager.addPrint("{0:^16}\n".format('None'))
        SystemManager.addPrint(oneLine + '\n')

        # close fd that thread who already termiated created becuase of limited resource #
        for idx, value in sorted(self.prevProcData.items(), key=lambda e: e[1]['alive'], reverse=True):
            if value['alive'] is False:
                comm = '#' + value['stat'][self.commIdx][1:-1]

                if SystemManager.processEnable is True:
                    pid = value['stat'][self.ppidIdx]
                    stackSize = (long(value['stat'][self.sstackIdx]) - \
                        long(value['stat'][self.estackIdx])) / 1024 / 1024
                else:
                    pid = value['mainID']
                    stackSize = '-'

                codeSize = (long(value['stat'][self.ecodeIdx]) - \
                    long(value['stat'][self.scodeIdx])) / 1024 / 1024

                if ConfigManager.schedList[int(value['stat'][self.policyIdx])] == 'C':
                    schedValue = "%3d" % (int(value['stat'][self.prioIdx]) - 20)
                else:
                    schedValue = "%3d" % (abs(int(value['stat'][self.prioIdx]) + 1))

                runtimeSec = value['runtime'] + SystemManager.uptimeDiff
                runtimeMin = runtimeSec / 60
                runtimeHour = runtimeMin / 60
                if runtimeHour > 0:
                    runtimeMin %= 60
                runtimeSec %= 60
                lifeTime = "%3d:%2d:%2d" % (runtimeHour, runtimeMin, runtimeSec)

                try:
                    vmlib = long(value['status']['VmLib'][:value['status']['VmLib'].find(' kb') - 1]) / 1024
                except:
                    vmlib = '-'
                try:
                    vmswp = long(value['status']['VmSwap'][:value['status']['VmSwap'].find(' kb') - 1]) / 1024
                except:
                    vmswp = '-'

                if SystemManager.diskEnable is True:
                    readSize = value['read'] / 1024 / 1024
                    writeSize = value['write'] / 1024 / 1024
                else:
                    readSize = '-'
                    writeSize = '-'

                # print die thread information #
                SystemManager.addPrint(\
                    ("{0:>16} ({1:>5}/{2:>5}/{3:>4}/{4:>4})| {5:>3}({6:>3}/{7:>3}/{8:>3})| " + \
                    "{9:>4}({10:>3}/{11:>3}/{12:>3}/{13:>3})| {14:>3}({15:>4}/{16:>4}/{17:>5})|{18:>9}|\n").\
                    format(comm, idx, pid, value['stat'][self.nrthreadIdx], \
                    ConfigManager.schedList[int(value['stat'][self.policyIdx])] + str(schedValue), \
                    value['ttime'], value['utime'], value['stime'], int(value['cttime']), \
                    long(value['stat'][self.vsizeIdx]) / 1024 / 1024, \
                    long(value['stat'][self.rssIdx]) * 4 / 1024, codeSize, vmlib, vmswp, \
                    value['btime'], readSize, writeSize, value['majflt'], lifeTime))
                dieCnt += 1

                try:
                    if value['statFd'] is not None:
                        value['statFd'].close()
                except:
                    pass
                try:
                    if value['statusFd'] is not None:
                        value['statusFd'].close()
                except:
                    pass
                try:
                    if value['ioFd'] is not None:
                        value['ioFd'].close()
                except:
                    pass

            # cut by rows of terminal #
            if int(SystemManager.bufferRows) >= int(SystemManager.ttyRows) - 5 and \
                SystemManager.printFile is None:
                return

        if dieCnt > 0:
            SystemManager.addPrint(oneLine + '\n')



    def printTopUsage(self):
        SystemManager.addPrint((" \n[Top Info] [Time: %7.3f] [Period: %d sec] [Interval: %.1f sec] " + \
            "[Ctxt: %d] [Fork: %d] [IRQ: %d] [Unit: %%/MB]\n") % \
            (SystemManager.uptime, SystemManager.intervalEnable, SystemManager.uptimeDiff, \
            self.cpuData['ctxt']['ctxt'] - self.prevCpuData['ctxt']['ctxt'], \
            self.cpuData['processes']['processes'] - self.prevCpuData['processes']['processes'], \
            self.cpuData['intr']['intr'] - self.prevCpuData['intr']['intr']))

        # print system usage #
        self.printSystemUsage()

        # print process info #
        self.printProcUsage()

        # realtime mode #
        if SystemManager.printFile is None:
            SystemManager.pipePrint(SystemManager.bufferString)
            SystemManager.clearPrint()
            SystemManager.bufferRows = 0
        # buffered mode #
        else:
            SystemManager.procBuffer.insert(0, SystemManager.bufferString)
            SystemManager.procBufferSize += len(SystemManager.bufferString)
            SystemManager.clearPrint()
            SystemManager.bufferRows = 0

            while SystemManager.procBufferSize > int(SystemManager.bufferSize) * 10:
                SystemManager.procBufferSize -= len(SystemManager.procBuffer[-1])
                SystemManager.procBuffer.pop(-1)





if __name__ == '__main__':

    oneLine = "-" * SystemManager.lineLength
    twoLine = "=" * SystemManager.lineLength

    SystemManager.printOptions()

    SystemManager.inputFile = sys.argv[1]
    SystemManager.outputFile = None

    SystemManager.setComm()

    # print backgroud process list #
    if SystemManager.isListMode() is True:
        SystemManager.printBackgroundProcs()
        sys.exit(0)

    # send start / stop signal to background process #
    if SystemManager.isStartMode() is True or SystemManager.isStopMode() is True:
        SystemManager.sendSignalProcs(signal.SIGINT)
        sys.exit(0)

    # send event signal to background process #
    if SystemManager.isSendMode() is True:
        SystemManager.sendSignalProcs(signal.SIGQUIT)
        sys.exit(0)

    # parse recording option #
    if SystemManager.isRecordMode() is True:
        # update record status #
        SystemManager.recordStatus = True
        SystemManager.inputFile = '/sys/kernel/debug/tracing/trace'

        # set this process to RT priority #
        SystemManager.setRtPriority('90')

        # save system information #
        si = SystemManager()

        SystemManager.parseRecordOption()

        SystemManager.printRecordOption()

        # run in background #
        if SystemManager.backgroundEnable is True:
            pid = os.fork()

            if pid > 0:
                sys.exit(0)
            else:
                SystemManager.printStatus("background running as process %s" % os.getpid())

        # wait for signal #
        if SystemManager.waitEnable is True:
            SystemManager.printStatus("wait for starting profile... [ START(ctrl + c) ]")
            signal.signal(signal.SIGINT, SystemManager.defaultHandler)
            signal.signal(signal.SIGQUIT, SystemManager.defaultHandler)
            signal.pause()

        if SystemManager.isSystemMode() is True:
            # save system info and write it to buffer #
            si.saveAllInfo()
            si.printAllInfoToBuf()

            # parse all options and make output file path #
            SystemManager.parseAddOption()
            if SystemManager.printFile is not None:
                SystemManager.outputFile = SystemManager.printFile + '/guider.out'

            # print system information #
            SystemManager.printTitle()
            SystemManager.pipePrint(SystemManager.systemInfoBuffer)

            # close pipe for less util #
            if SystemManager.pipeForPrint is not None:
                SystemManager.pipeForPrint.close()

            sys.exit(0)

        # set signal #
        if SystemManager.repeatCount > 0 and SystemManager.repeatInterval > 0 and \
            SystemManager.isThreadMode() is True:
            signal.signal(signal.SIGALRM, SystemManager.alarmHandler)
            signal.signal(signal.SIGINT, SystemManager.stopHandler)
            signal.alarm(SystemManager.repeatInterval)

            if SystemManager.outputFile is None:
                SystemManager.printError("wrong option with -s, use also path to save data")
                sys.exit(0)
        else:
            SystemManager.repeatInterval = 0
            SystemManager.repeatCount = 0
            signal.signal(signal.SIGINT, SystemManager.stopHandler)
            signal.signal(signal.SIGQUIT, SystemManager.newHandler)

        # create FileAnalyzer #
        if SystemManager.isFileMode() is True:
            # check permission #
            if os.geteuid() != 0:
                SystemManager.printError("Fail to get root permission")
                sys.exit(0)

            # parse additional option #
            SystemManager.parseAddOption()

            # start file profiling #
            pi = FileAnalyzer()

            # save system info and write it to buffer #
            si.saveAllInfo()
            si.printAllInfoToBuf()

            # print total file usage per process #
            if SystemManager.intervalEnable == 0:
                pi.printUsage()
            # print file usage per process on timeline #
            else:
                pi.printIntervalInfo()

            # close pipe for less util #
            if SystemManager.pipeForPrint is not None:
                SystemManager.pipeForPrint.close()

            sys.exit(0)

        # start recording for thread profile #
        SystemManager.printStatus(r'start recording... [ STOP(ctrl + c), MARK(ctrl + \) ]')
        si.runRecordStartCmd()

        # register exit handler #
        atexit.register(SystemManager.runRecordStopCmd)

        if SystemManager.pipeEnable is True:
            if SystemManager.outputFile is not None:
                SystemManager.setIdlePriority()
                SystemManager.copyPipeToFile(SystemManager.inputFile + '_pipe', SystemManager.outputFile)
                SystemManager.printInfo("wrote output to %s successfully" % (SystemManager.outputFile))
            else:
                SystemManager.printError("wrong option with -ep, use also -s option to save data")

            sys.exit(0)

        # get init time from buffer for verification #
        initTime = ThreadAnalyzer.getInitTime(SystemManager.inputFile)

        # enter loop to record and save data periodically #
        while SystemManager.repeatInterval > 0:
            if SystemManager.repeatCount == 0:
                sys.exit(0)

            # get init time in buffer for verification #
            initTime = ThreadAnalyzer.getInitTime(SystemManager.inputFile)

            # wait for timer #
            signal.pause()

            # compare init time with now time for buffer verification #
            if initTime != ThreadAnalyzer.getInitTime(SystemManager.inputFile):
                SystemManager.printError("buffer size is not enough (%s KB) to profile" % \
                    SystemManager.getBufferSize())
                sys.exit(0)
            else:
                SystemManager.clearTraceBuffer()

        # wait for user input #
        while True:
            SystemManager.condExit = True
            signal.pause()
            if SystemManager.condExit is True:
                break

        if initTime != ThreadAnalyzer.getInitTime(SystemManager.inputFile):
            SystemManager.printError("buffer size is not enough (%s KB) to profile" % \
                SystemManager.getBufferSize())
            sys.exit(0)

        # save system information #
        si.saveAllInfo()

    # parse additional option #
    SystemManager.parseAddOption()

    # get tty setting #
    SystemManager.getTty()

    if SystemManager.isTopMode() is True:
        SystemManager.printRecordOption()

        # set handler for exit #
        signal.signal(signal.SIGINT, SystemManager.stopHandler)
        signal.signal(signal.SIGQUIT, SystemManager.newHandler)

        # run in background #
        if SystemManager.backgroundEnable is True:
            pid = os.fork()

            if pid > 0:
                sys.exit(0)
            else:
                SystemManager.printStatus("background running as process %s" % os.getpid())

        # create ThreadAnalyzer using proc #
        ti = ThreadAnalyzer(None)

        # close pipe for less util #
        if SystemManager.pipeForPrint is not None:
            SystemManager.pipeForPrint.close()

        sys.exit(0)

    # set handler for exit #
    signal.signal(signal.SIGINT, SystemManager.exitHandler)

    # check log file is recoginizable #
    ThreadAnalyzer.getInitTime(SystemManager.inputFile)

    if SystemManager.isRecordMode() is True:
        # write system info to buffer #
        si.printAllInfoToBuf()
    else:
        # apply launch option from data file #
        SystemManager.applyLaunchOption()

    # print analysis option #
    SystemManager.printAnalOption()

    # create Event Info #
    ei = EventAnalyzer()

    # create Function Info #
    if SystemManager.functionEnable is not False:
        fi = FunctionAnalyzer(SystemManager.inputFile)

        # print Function Info #
        fi.printUsage()

        # close pipe for less util #
        if SystemManager.pipeForPrint is not None:
            SystemManager.pipeForPrint.close()

        sys.exit(0)
    else:
        # import packages to draw graph #
        if SystemManager.graphEnable is True:
            try:
                import matplotlib
                matplotlib.use('Agg')
                from pylab import \
                    rc, rcParams, subplot, plot, title, ylabel, legend, figure, savefig, clf
            except:
                SystemManager.printError("graph is not supported because of no matplotlib")
                SystemManager.graphEnable = False

        # create ThreadAnalyzer using ftrace #
        ti = ThreadAnalyzer(SystemManager.inputFile)

    # print event info #
    ei.printEventInfo()

    # close pipe for less util #
    if SystemManager.pipeForPrint is not None:
        SystemManager.pipeForPrint.close()

    # start input menu #
    if SystemManager.selectMenu != None:
        # make file related to taskchain #
        ti.makeTaskChain()
