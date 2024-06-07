from openai import OpenAI

import puddle.prompts as pp

def configure_ask(model = "gpt-3.5-turbo"):
    """
    Make a function that will answer text questions with text answers.
    """

    def ask(system_prompt : str, user_prompt : str = pp.default_system_prompt) -> str:

        client = OpenAI()

        completion = client.chat.completions.create(
          model=model,
          messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
          ]
        )

        response = completion.choices[0].message.content

        if response is not None:
            return response
        else:
            raise ValueError("No response")

    return ask
