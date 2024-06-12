import click
from puddle.__about__ import __version__
import puddle.llm as llm
import puddle.collection as pc
from termcolor import colored

@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=False)
@click.version_option(version=__version__, prog_name="puddle")
def puddle():
    pass

@puddle.command(name = "ask")
@click.argument("prompt", type=str)
def ask_cmd(prompt):
    print(llm.ask(prompt))

def filterblank(txt):
    lines = [x.rstrip() for x in txt.split("\n")]
    return "\n".join([x for x in lines if len(x) > 0])


@puddle.command(name = "lookup")
@click.argument("query", type=str)
@click.option("-n", "--nresults", type=int, default=3, help="Number of results to return")
def lookup_cmd(query, nresults):
    col = pc.opencol()
    results = pc.query(
        collection = col,
        txt = query,
        n = nresults
    )

    N = len(results["ids"])
    for i in range(N):
        M = len(results["ids"][i])
        for j in range(M):
            print("")
            print(colored(results["ids"][i][j], "magenta"))
            if results["documents"]:
                print(filterblank(results["documents"][i][j]))
