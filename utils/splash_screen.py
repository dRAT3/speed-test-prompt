import time
from colorama import init, Fore
from itertools import cycle

# Initialize Colorama
init()
def cycle_hex_and_colors():
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
   Ld.preloaing...\\     0x2c
    """
]


# Loop through frames to simulate the animation
try:
    while True:
        for i, frame in enumerate(frames):
            print('\033c', end='')  # Clear the console (works in many terminals)
            print(frame)
            time.sleep(.111)  # Adjust timing as necessary
except KeyboardInterrupt:
    print('\033c', end='')  # Clear the console on exit
    print("Animation stopped.")
