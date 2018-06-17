#!/usr/bin/env python

# Imports =====================================================================

import click

from pyzub.subfiles import SRTFile

# Params ======================================================================

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# CLI =========================================================================


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='0.1.5')
def main():
    pass


@main.command()
@click.argument('filepath')
@click.option('--hours', default=0.0)
@click.option('--minutes', default=0.0)
@click.option('--seconds', default=0.0)
@click.option('--milliseconds', default=0.0)
@click.option('--microseconds', default=0.0)
@click.option('--overwrite', is_flag=True,
              help='Modifies the subtitle file in place.')
@click.option('--verbose', is_flag=True,
              help='Displays a progress bar and a message when finished.')
def slide(**kwargs):

    filepath = kwargs['filepath']

    subfile = SRTFile(filepath)

    subfile.slide(hours=kwargs['hours'],
                  minutes=kwargs['minutes'],
                  seconds=kwargs['seconds'],
                  milliseconds=kwargs['milliseconds'],
                  microseconds=kwargs['microseconds'],
                  progress_bar=kwargs['verbose'])

    if kwargs['overwrite'] is True:

        subfile.dump(filepath)

    else:
        aux = filepath.rfind('.srt')

        if aux != -1:
            filepath_new = filepath.split('.')
            filepath_new.insert(-1, '_MODIFIED.')
            filepath_new = ''.join(filepath_new)

        subfile.dump(filepath_new)

    if kwargs['verbose'] is True:
        print('Done sliding your sub!')

# Main ========================================================================


if __name__ == '__main__':
    main()
