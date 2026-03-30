# simple wrapper around the OpenAI responses API
# make sure you have the official `openai` package installed
# and set the OPENAI_API_KEY environment variable.

from colorama import Fore

try:
    # correct class name; older versions used `OpenAI`, not `OpenAi`
    from openai import OpenAI
except ImportError:
    print(Fore.RED + "The openai package is not installed. "
                  "Run `pip install openai` and try again.")
    raise

# instantiate client after import succeeded
client = OpenAI()

# prompt the user
prompt = input("What would you like to do: ")

try:
    # use the Responses API and a valid model name
    res = client.responses.create(
        model="gpt-4o-mini",  # change to a model you have access to
        input=prompt
    )
    # print result text, handling older/newer response shapes
    output = getattr(res, "output_text", None) or \
             (res.output[0].content[0].text if res.output else "")
    print(output)
except Exception as e:
    print(Fore.RED + f"Request failed: {e}")

