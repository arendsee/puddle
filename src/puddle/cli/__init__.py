import click
from puddle.__about__ import __version__
from puddle.llm import ask

@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=False)
@click.version_option(version=__version__, prog_name="puddle")
def puddle():
    pass

@puddle.command(name = "ask")
@click.argument("prompt", type=str)
def ask_cmd(prompt):
    print(ask(prompt))
