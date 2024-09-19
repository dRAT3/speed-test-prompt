import time
from colorama import init, Fore
from itertools import cycle

# Initialize Colorama
init()
loading = True

def cycle_hex_and_colors(state: int, frame: int):
    #
    # Color cycling for funky effects
    #colors = cycle([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE])
    
    if state == 0x00:
        ld = "Loading"
        sp = cycle(["...", ".\\.", ".-.", "./."])

        color1 = Fore.MAGENTA if frame % 2 == 0 else Fore.RED
        color2 = Fore.MAGENTA if frame % 2 == 1 else Fore.RED
        color3 = Fore.MAGENTA if frame % 3 == 0 else Fore.RED

    colors = [color1, color2, color3]
    
    return colors

frames_warning = [
    f"""
      {Fore.RED}O{Fore.RESET}       {Fore.RED}O{Fore.RESET}         Observe
       {Fore.RED}O{Fore.RESET}      {Fore.YELLOW}OOO{Fore.RESET}     /
                     .  .
       {Fore.RED}O{Fore.RESET}       {Fore.RED}O{Fore.RESET}         
       {Fore.RED}O{Fore.RESET}      {Fore.YELLOW}OOO{Fore.RESET}     /
     {Fore.RED}O O{Fore.RESET}    {Fore.YELLOW}O O O{Fore.RESET}    /_____
      {Fore.YELLOW}O O O{Fore.RESET}    {Fore.RED}O{Fore.RESET}   --\\
       /              \\
         /        \\________
        /            \\
       /              \\
   Loading...      0x2c
    """,

    f"""
      {Fore.RED}O{Fore.RESET}       {Fore.RED}O{Fore.RESET}         Observe
       {Fore.RED}O{Fore.RESET}      {Fore.YELLOW}OOO{Fore.RESET}     /
                     .  .
       {Fore.RED}O{Fore.RESET}       {Fore.RED}O{Fore.RESET}         Observe
       {Fore.RED}O{Fore.RESET}      {Fore.YELLOW}OOO{Fore.RESET}     /
     {Fore.RED}O O{Fore.RESET}    {Fore.YELLOW}O O O{Fore.RESET}    /_____
      {Fore.YELLOW}O O O{Fore.RESET}    {Fore.RED}O{Fore.RESET}   --\\
       /              \\
         /        \\________
        /            \\
       /              \\
   Loading...|     0x1c
    """,

    f"""
      {Fore.RED}O{Fore.RESET}       {Fore.RED}O{Fore.RESET}         
       {Fore.RED}O{Fore.RESET}      {Fore.YELLOW}OOO{Fore.RESET}     /
                     .  .
       {Fore.RED}O{Fore.RESET}       {Fore.RED}O{Fore.RESET}         Observe
       {Fore.RED}O{Fore.RESET}      {Fore.YELLOW}OOO{Fore.RESET}     /
     {Fore.RED}O O{Fore.RESET}    {Fore.YELLOW}O O O{Fore.RESET}    /_____
      {Fore.YELLOW}O O O{Fore.RESET}    {Fore.RED}O{Fore.RESET}   --\\
       /              \\
         /        \\________
        /            \\
       /              \\
   Loading.../     0xcc
    """,

    f"""
      {Fore.RED}O{Fore.RESET}       {Fore.RED}O{Fore.RESET}         
       {Fore.RED}O{Fore.RESET}      {Fore.YELLOW}OOO{Fore.RESET}     /
                     .  .
       {Fore.RED}O{Fore.RESET}       {Fore.RED}O{Fore.RESET}         
       {Fore.RED}O{Fore.RESET}      {Fore.YELLOW}OOO{Fore.RESET}     /
     {Fore.RED}O O{Fore.RESET}    {Fore.YELLOW}O O O{Fore.RESET}    /_____
      {Fore.YELLOW}O O O{Fore.RESET}    {Fore.RED}O{Fore.RESET}   --\\
       /              \\
         /        \\________
        /            \\
       /              \\
   Loading...-     0xcd
    """, 
    f"""
      {Fore.RED}O{Fore.RESET}       {Fore.RED}O{Fore.RESET}         
       {Fore.RED}O{Fore.RESET}      {Fore.YELLOW}OOO{Fore.RESET}     /
                     .  .
       {Fore.RED}O{Fore.RESET}       {Fore.RED}O{Fore.RESET}         
       {Fore.RED}O{Fore.RESET}      {Fore.YELLOW}OOO{Fore.RESET}     /
     {Fore.RED}O O{Fore.RESET}    {Fore.YELLOW}O O O{Fore.RESET}    /_____ Observe
      {Fore.YELLOW}O O O{Fore.RESET}    {Fore.RED}O{Fore.RESET}   --\\ 
       /              \\
         /        \\________  Server
        /            \\
       /              \\
   Loading...\\     0x2c
    """]

def main_buffer_cli(sample_size: int, buffer: list[int]):
    try:
        while True:
            for i in range(0, sample_size):
                colors = cycle_hex_and_colors(0x00, i)
                
                print('\033c', end='')  # Clear the console (works in many terminals)
                hex_value = f"0x{i % 256:02x}"  # Cycle through 00 to ff

                print(frames_warning[i])

                time.sleep(.137373737373737373737373737373737373737373737373737373737373737373737373737)  # Adjust timing as necessary

    except KeyboardInterrupt:
        print('\033c', end='')  # Clear the console on exit
        print("Animation stopped.")

main_buffer_cli(5, [0])
