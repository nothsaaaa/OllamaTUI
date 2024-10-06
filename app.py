import requests
import logging
from colorama import Fore, Style
import threading
import time
from request import *
from utils import *

def loading_animation(stop_event):
    animation = "|/-\\"
    idx = 0
    while not stop_event.is_set():
        print(f"\r{animation[idx % len(animation)]}", end="")
        idx += 1
        time.sleep(0.1)

def main():
    figlet("OllamaTUI")
    print("OllamaTUI by Ashlyn (v0.1)")
    print(f"\033[3m{Style.DIM}because ollama isn't enough...\033[0m\n")
    #will not render on terminals without ansi escape codes
    
    formatted_models = fetch_tags()
    models = [model.split('] ')[1] for model in formatted_models]

    # Model selection menu    
    for model in formatted_models:
        print(model)
    
    while True:
        try:
            selected_index = int(input("Select a model number: ")) - 1
            if 0 <= selected_index < len(formatted_models):
                selected_model = models[selected_index]
                break 
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numerical value.")

    model = selected_model
    messages = []
    clear_screen()
    print("Loading model...")
    load(selected_model)
    clear_screen()
    print(f"{Fore.GREEN}MODEL LOADED{Fore.RESET}")
    print("Start chatting (type 'exit' to quit):")

    # Chatloop
    while True:
        user_input = input(f"{Fore.GREEN}> ")
        
        if user_input.lower() == 'exit':
            print(f"{Fore.GREEN}Exiting the chat. Goodbye!{Fore.RESET}")
            break
        
        messages.append({
            "role": "user",
            "content": user_input
        })

        stop_event = threading.Event()
        loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
        loading_thread.start()
        
        response = chat(model, messages, stream=True)
        stop_event.set() # Stop the loading animation
        loading_thread.join() # Wait for the thread to finish
        
        if response:
            final_response = ""
            for res in response:
                if 'message' in res:
                    new_content = res['message']['content']
                    final_response += new_content

                if res.get('done'):
                    break
            
            messages.append({
                "role": "assistant",
                "content": final_response
            })
            
            print(f"\r{Fore.RESET}{final_response}")
        else:
            print("Failed to get a response from the assistant.")

if __name__ == "__main__":
    main()
