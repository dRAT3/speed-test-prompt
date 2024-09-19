import os
import time
import typer
import threading
from colorama import Fore, init
from itertools import cycle

# Initialize colorama for cross-platform support
init(autoreset=True)

# Typer app instance
app = typer.Typer()

stop_animation = False  # Global flag to stop the animation
stop_spinner = False     # Global flag to stop the spinner
logs = []  # List to store log messages

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_art(frame, loading=False):
    """Function to print the ASCII art animation."""
    bits = '1101100001'
    toggled_bits = ''.join(b if (frame // 5) % 2 == 0 else ' ' for b in bits)
    hex_value = f"0x{frame % 256:02x}"  # Cycle through 00 to ff

    # Color cycling for funky effects
    colors = cycle([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE])
    
    if loading:
        # Simulate "pinking" effect by alternating between magenta and red
        color1 = Fore.MAGENTA if frame % 2 == 0 else Fore.RED
        color2 = Fore.MAGENTA if frame % 2 == 1 else Fore.RED
        color3 = Fore.MAGENTA if frame % 3 == 0 else Fore.RED
    else:
        # Regular funky colors
        color1 = next(colors)
        color2 = next(colors)
        color3 = next(colors)

    art = f"""          
     {color1}O       O         Observe
     {color1}O      OOO     /
   {color2}O O    O O O    /
    {color2}O O O    O   --

       {color3}/        \\________
      {color3}/            \\    
     {color3}/              \\        
   {color1}{toggled_bits}     {color2}{hex_value}
    """
    # Instead of clearing the screen, print only in the top portion
    print(art)

def animate_art(loading=False, speed=0.1):
    """Function to run the animation in a separate thread."""
    global stop_animation
    frame = 0
    while not stop_animation:
        print_art(frame, loading)
        time.sleep(speed)
        frame += 1

def print_logs():
    """Prints all accumulated logs without clearing them."""
    global logs
    # Since logs should accumulate, print them once and update the logs section only
    for log in logs:
        print(log)

def spinner_animation():
    """Function to run the spinner in a separate thread."""
    global stop_spinner
    spinner = cycle(['|', '/', '-', '\\'])  # Simple spinner
    while not stop_spinner:
        print(f"Spinner: {next(spinner)}", end='\r')  # Print spinner on the same line
        time.sleep(0.1)  # Adjust speed of the spinner

@app.command()
def run_loading_animation(speed: float = 0.1):
    """
    Runs the loading animation and prints logs with a spinner simultaneously.

    Parameters:
    speed: The delay between frames (in seconds).
    """
    global stop_animation, stop_spinner
    stop_animation = False
    stop_spinner = False
    
    # Initial clear screen
    clear_screen()

    # Start the animation in a separate thread
    animation_thread = threading.Thread(target=animate_art, args=(True, speed))
    animation_thread.start()

    # Start the spinner in a separate thread
    spinner_thread = threading.Thread(target=spinner_animation)
    spinner_thread.start()

    # Simulate log printing while the animation runs
    global logs
    for i in range(10):  # Simulating 10 log entries
        time.sleep(1)  # Delay to simulate work being done
        log_message = f"Log message {i+1}: Something is processing..."
        logs.append(log_message)
        if i == 0:
            print("\n" * 8)  # Reserve space for the animation to be above the logs
        print_logs()  # Print logs below the reserved animation area

    # Stop the animation after logs are printed
    stop_animation = True
    stop_spinner = True
    animation_thread.join()  # Wait for the animation thread to finish
    spinner_thread.join()    # Wait for the spinner thread to finish

    # Final message
    print("Loading complete. All processes finished!")

# Entry point for Typer CLI
if __name__ == "__main__":
    app()
