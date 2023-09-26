
import openai
import json
from hyphenate import hyphenate_word

def run_conversation(api_key, word, language="American English"):
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": f'What is the syllabification of the word \'{word}\' in {language}'}]
    functions = [
        {
            "name": "hyphenate_word",
            "description": "Separate into syllables (hyphenate) the given word",
            "parameters": {
                "type": "object",
                "properties": {
                    "language": {
                        "type": "string",
                        "description": "The ISO 639-1 code of the language to which the word belongs, e.g. en",
                    },
                    "region": {
                        "type": "string",
                        "description": "The ISO 3166-1 Alpha-2 code of the region to which the word belongs, e.g. gb",
                    },
                    "word": {
                        "type": "string",
                        "description": "The word that the user wants to hyphenate, e.g. tomato",
                    },
                },
                "required": ["language", "word"],
            },
        }
    ]
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "hyphenate_word": hyphenate_word,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(
            language=function_args.get("language"),
            region=function_args.get("region"),
            word=function_args.get("word"),
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response


print(run_conversation("<YOUR API KEY HERE>", "associates", "British English"))
