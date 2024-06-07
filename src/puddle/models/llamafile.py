import puddle.prompts as pp
import subprocess

def configure_ask(llamafile : str):
    """
    Make a function that will answer text questions with text answers.
    """

    def ask(system_prompt : str, user_prompt : str = pp.default_system_prompt) -> str:

        response = subprocess.run([llamafile, "-p", f"{system_prompt}\n{user_prompt}"], stdout=True)

        return response.stdout.decode("ascii")

    return ask
