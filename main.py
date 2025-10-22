import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import *
from call_function import available_functions, call_function




def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")


    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    iters = 0
    while True:
        iters += 1
        if iters > 20:
            print(f"Maximum interactions ({20}) reached.")
            sys.exit(1)
        try:
            content_return = generate_content(client, messages, verbose)

            if content_return:
                print("Final response:")
                print(content_return)
                break

        except Exception as e:
            print(f"Error in generate_content: {e}")








def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model = 'gemini-2.0-flash-001',
        contents = messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call results")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response}")
        function_responses.append(function_call_result.parts[0])
    


    messages.append(types.Content(role="user", parts=function_responses))


    if not function_responses:
        raise Exception("no function responses generated, exiting")

        

if __name__ == "__main__":
    main()
