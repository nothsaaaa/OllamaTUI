import requests
import logging
from colorama import Fore
import threading
import time
from request import *
from utils import *

# Define a simple loading animation
def loading_animation(stop_event):
    animation = "|/-\\"
    idx = 0
    while not stop_event.is_set():
        print(f"\r{animation[idx % len(animation)]}", end="")
        idx += 1
        time.sleep(0.1)

def main():
    figlet("OllamaTUI")
    print("OllamaTUI by Ashlyn (v0.1)\n")
    
    formatted_models = fetch_tags()
    models = [model.split('] ')[1] for model in formatted_models]
    
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

    print("Start chatting (type 'exit' to quit):")
    
    while True:
        user_input = input(f"{Fore.GREEN}> ")
        
        if user_input.lower() == 'exit':
            print("Exiting the chat. Goodbye!")
            break
        
        # Append user message to messages
        messages.append({
            "role": "user",
            "content": user_input
        })

        stop_event = threading.Event()
        loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
        loading_thread.start()
        
        response = chat(model, messages, stream=True)
        stop_event.set()  # Stop the loading animation
        loading_thread.join()  # Wait for the thread to finish

        if response:
            final_response = ""
            for res in response:
                if 'message' in res:
                    new_content = res['message']['content']
                    final_response += new_content

                if res.get('done'):
                    break
            
            # Append assistant's response to messages
            messages.append({
                "role": "assistant",
                "content": final_response
            })
            
            print(f"\r{Fore.RESET}{final_response}")
        else:
            print("Failed to get a response from the assistant.")

if __name__ == "__main__":
    main()
