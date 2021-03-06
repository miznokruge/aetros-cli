from __future__ import absolute_import
from __future__ import print_function

import sys
import logging
import os

import aetros.const

__version__ = const.__version__

command_summaries = [
    ['start', 'Starts a job of a model in current working directory'],
    ['predict', 'Runs a prediction locally'],
    ['upload-weights', 'Uploads weights as new or existing job.'],
    ['prediction-server', 'Spawns a http server that handles incoming data as input and predicts output.'],
    ['server', 'Spawns a job server that handles jobs managed through AETROS Trainer.'],
    ['run', 'Executes a command on an AETROS server.'],
    ['api', 'Executes a API call through SSH connection.'],
    ['push-job', 'Pushes a local job to AETROS Trainer.'],
]

def parseopts(args):
    if len(args) == 0:
        description = [''] + ['%-27s %s' % (i, j) for i, j in command_summaries]
        print("usage: aetros [command]")
        print("v%s\n" %(const.__version__))
        print(('Possible commands:\n' + (
            '\n'.join(description))))

        sys.exit(1)

    cmd_name = args[0]

    # all the args without the subcommand
    cmd_args = args[1:]

    return cmd_name, cmd_args


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    cmd_name, cmd_args = parseopts(args)
    if cmd_name == '--version':
        print(aetros.const.__version__)
        sys.exit(0)

    from aetros.commands.ApiCommand import ApiCommand
    from aetros.commands.PushJobCommand import PushJobCommand
    from aetros.commands.ServerCommand import ServerCommand
    from aetros.commands.UploadWeightsCommand import UploadWeightsCommand
    from aetros.commands.PredictCommand import PredictCommand
    from aetros.commands.PredictionServerCommand import PredictionServerCommand
    from aetros.commands.StartCommand import StartCommand
    from aetros.commands.RunCommand import RunCommand

    commands_dict = {
        'start': StartCommand,
        'predict': PredictCommand,
        'upload-weights': UploadWeightsCommand,
        'prediction-server': PredictionServerCommand,
        'server': ServerCommand,
        'run': RunCommand,
        'api': ApiCommand,
        'push-job': PushJobCommand,
    }

    log_level = 'INFO'
    if os.getenv('DEBUG') == '1':
        log_level = 'DEBUG'

    logger = logging.getLogger('aetros-'+cmd_name)

    import coloredlogs
    coloredlogs.install(level=log_level, logger=logger)

    if cmd_name not in commands_dict:
        print(("Command %s not found" % (cmd_name,)))
        sys.exit(1)

    level = 'INFO'
    if '-v' in args:
        level = 'DEBUG'

    logger = logging.getLogger('aetros-'+cmd_name)
    coloredlogs.install(level=level, logger=logger)
    command = commands_dict[cmd_name](logger)

    code = command.main(cmd_args)
    sys.exit(code)
