import openai
import argparse

# Define a function to generate a response using OpenAI
def generate_response(prompt, api_key):
    openai.api_key = api_key
    model_engine = "text-davinci-003" # Replace with your preferred model engine
    prompt = f"{prompt.strip()}\nAI:"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    message = response.choices[0].text
    message = message.replace("AI:", "").strip()
    return message

# Define a function to handle incoming messages
def handle_message(message, api_key):
    response = generate_response(message, api_key)
    return response

# Define main entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chat with GPT using OpenAI')
    parser.add_argument('--api_key', metavar='API_KEY', type=str, required=True,
                        help='the OpenAI API key to use')
    parser.add_argument('message', metavar='M', type=str, nargs='+',
                        help='the message to send to GPT')
    args = parser.parse_args()

    api_key = args.api_key
    message = ' '.join(args.message)
    response = handle_message(message, api_key)

    print(response)
