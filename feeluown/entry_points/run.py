from feeluown.utils.patch import patch_janus, patch_qeventloop
patch_janus()

try:
    patch_qeventloop()
except ImportError:
    # qasync/qt is not installed
    # FIXME: should not catch the error at here
    pass

# pylint: disable=wrong-import-position
from feeluown.utils.utils import is_port_inuse  # noqa: E402
from .base import create_config, setup_argparse  # noqa: E402
from .run_cli import run_cli  # noqa: E402
from .run_app import run_once, run_forever  # noqa: E402


def run():
    """feeluown entry point"""

    args = setup_argparse().parse_args()
    config = create_config()

    # we are trying to run some commands
    if args.cmd is not None:

        if args.cmd == 'genicon':
            return run_cli(args)

        # if daemon is started, we send commands to daemon directly
        # we simple think the daemon is started as long as
        # the port 23333 is in use
        if is_port_inuse(23333):
            return run_cli(args)

        # If daemon is not started, (some) commands can be meaningless,
        # such as `status`, `toggle`, `next`, etc. However, some other
        # commands can still be usefule. For instance, when people
        # want to fetch a song's playable url or see the lyric of a song,
        # they may run `fuo show fuo://xxx/songs/12345`. When people
        # want to make an audition of some music, they run
        # `fuo play fuo://xxx/songs/12345`. Under these circumstances,
        # we should try to make feeluown work as they expected to.
        # Currently, we have three such commands:
        cmds = ('show', 'play', 'search')
        if args.cmd in cmds:
            return run_once(args, config)

        raise SystemExit("can't connect to fuo daemon.")

    return run_forever(args, config)
