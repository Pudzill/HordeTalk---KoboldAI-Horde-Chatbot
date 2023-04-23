import asyncio
from text_generation import generate_text
from colorama import Fore, Style, init
import sys
import time
import re
from profanityfilter import ProfanityFilter

init(autoreset=True)  # initialize colorama

pf = ProfanityFilter()

def print_loading_bar():
    animation = "|/-\\"
    idx = 0

    while not print_loading_bar.finished:
        sys.stdout.write("\r" + Fore.MAGENTA + "Generating " + animation[idx % len(animation)] + " ")
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1

async def main():
    chat = False # off because it takes a hundred years to generate anything with the chat based models.
    printing = False
    timeout = 45
    user_text = ""
    prompt = "User: Hello!\nAssistant: Greetings! I am your friendly virtual AI. How can I assist you today?\n"

    print(Fore.MAGENTA + prompt)

    print(Fore.GREEN + "Welcome to "+ Style.BRIGHT + Fore.BLUE + "HordeTalk" + Style.RESET_ALL + Fore.GREEN + ", the free AI-powered chat assistant!\n")
    
    print(Fore.GREEN + "Commands:")
    print(Fore.GREEN + "  restart - Restart the conversation completely")
    print(Fore.GREEN + "  retry   - Remove the last User and Assistant messages, allowing you to enter new text.")
    print(Fore.GREEN + "  prompt  - Print the current prompt being sent to the AI")
    print(Fore.GREEN + "  exit    - Exit the chat\n")

    print(Fore.RED + Style.BRIGHT + "Reminder: AI-generated content may not always be accurate or reliable. Please approach the information with a critical mindset and verify the content's validity before relying on it. Remember to use the AI responsibly and ethically.\n")

    while True:
        print(Fore.YELLOW + "User: ", end="")
        user_text = input().strip()

        if user_text.lower() == '':
            print(Fore.RED + "Error: You must enter some text. Please try again.")
            continue
        
        if user_text.lower() == 'debug':
            printing = not printing
            print("Debug mode toggled, currently " + str(printing))
            continue
        
        if user_text.lower() == 'exit':
            print(Fore.RED + "Exiting the chat...")
            break

        if user_text.lower() == 'retry':
            prompt_lines = prompt.split("\n")
            if len(prompt_lines) <= 3:
                print(Fore.RED + "You cannot use the 'retry' command at the beginning of the conversation. Please enter your message.")
            else:
                print(Fore.RED + "Retried. Last User and Assistant messages have been removed. Please retype your message. Type 'prompt' for current prompt.")
                prompt = "\n".join(prompt_lines[:-3]) + "\n"
            continue
      
        if user_text.lower() == 'prompt':
            print(Fore.MAGENTA + prompt)
            continue
      
        if user_text.lower() == 'restart':
            prompt = "User: Hello!\nAssistant: Greetings! I am your friendly virtual AI. How can I assist you today?\n"
            print(Fore.RED + "\nRestarted conversation.")
            print(Fore.MAGENTA + prompt)
            continue

        prompt += f"User: {user_text}\nAssistant: "
        
        if user_text.lower() != "retry":
            print_loading_bar.finished = False
            asyncio.get_event_loop().run_in_executor(None, print_loading_bar)
        
            generated_text, error = await generate_text(chat, prompt, printing, timeout)
            print_loading_bar.finished = True
            
            # stop the loading bar and clear the line
            sys.stdout.write("\r")
            sys.stdout.flush()

            if error:
                if generated_text == "Timeout: generation took too long":
                    print(Fore.RED + "The AI's response took too long. Please try again.")
                    prompt_lines = prompt.split("\n")
                    prompt = "\n".join(prompt_lines[:-2]) + "\n"
                else:
                    print(Fore.RED + "The AI's response contained inappropriate content. Please rephrase your input.")
                    prompt_lines = prompt.split("\n")
                    prompt = "\n".join(prompt_lines[:-2]) + "\n"
            else:
                # extract the first response before the first assistant response
                pattern = r'^(.*?)(?=User:)'
                result = re.findall(pattern, generated_text, re.MULTILINE | re.DOTALL)
                if result:
                    first_response = result[0].strip()
                    if printing:
                      print("regex")
                else:
                    first_response = generated_text.strip()
                    if printing:  
                      print("no regex")

                print(Fore.CYAN + f"Assistant: {first_response}")

                # update the prompt to match the printed output
                prompt = prompt[:-len("Assistant: ")] + f"Assistant: {first_response}\n"

asyncio.run(main())
