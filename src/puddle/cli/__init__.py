# SPDX-FileCopyrightText: 2024-present Zebulun Arendsee <arendsee@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import click

from puddle.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="puddle")
def puddle():
    click.echo("Hello world!")
