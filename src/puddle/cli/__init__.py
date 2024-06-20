import click
from puddle.__about__ import __version__
import puddle.llm as llm
import puddle.models.openai as openai
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

@puddle.command(name = "dalle")
@click.argument("prompt", type=str)
@click.option("--model", default="dall-e-3", type=str, help="Model ['dall-e-2', 'dall-e-3']")
@click.option("--quality", default="standard", type=str, help="Quality ['standard', 'hd']")
@click.option("--size", default="1024x1024", type=str, help="Size (e.g., '1024x1024')")
@click.option("--user", default="George Washington", type=str, help="User name")
@click.option("--basename", default="dalle", type=str, help="Base output filename")
def dalle_cmd(prompt, model, quality, size, user, basename):
    response = llm.dalle(
        prompt,
        model=model,
        quality=quality,
        size=size,
        user=user
    )
    openai.write_img(response, basename)

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
