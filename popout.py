import re
import sys
import json
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Map color names from JSON to colorama constants
COLOR_MAP = {
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "cyan": Fore.CYAN,
    "magenta": Fore.MAGENTA,
    "white": Fore.WHITE,
    "reset": Style.RESET_ALL
}

def load_syntax_config(config_path):
    """Load the syntax highlighting configuration from a JSON file."""
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(Fore.RED + f"Error loading syntax configuration: {e}")
        sys.exit(1)

def apply_highlighting(content, syntax_config):
    """
    Highlight content based on patterns and colors defined in the syntax configuration.
    """
    patterns = [(re.compile(syntax["pattern"]), COLOR_MAP[syntax["color"]])
                for syntax in syntax_config.values()]
    
    position = 0
    while position < len(content):
        # Find the next match from all patterns
        next_match = None
        next_color = None

        for pattern, color in patterns:
            match = pattern.search(content, position)
            if match and (not next_match or match.start() < next_match.start()):
                next_match = match
                next_color = color
        
        if not next_match:
            # Print remaining content as normal text
            print(Fore.WHITE + content[position:], end='')
            break

        # Print content before the match
        print(Fore.WHITE + content[position:next_match.start()], end='')

        # Print the matched content with its color
        print(next_color + next_match.group(), end='')

        # Update position to continue after the match
        position = next_match.end()

def read_file(file_path):
    """Read and return the content of the input file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(Fore.RED + f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(Fore.RED + f"Error reading file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check for correct arguments
    if len(sys.argv) != 3:
        print(Fore.RED + f"Usage: python {sys.argv[0]} FILE.html Syntax.json")
        sys.exit(1)
    
    html_file = sys.argv[1]
    syntax_file = sys.argv[2]

    # Load the syntax configuration
    syntax_config = load_syntax_config(syntax_file)

    # Read the input HTML file
    html_content = read_file(html_file)

    # Apply syntax highlighting
    print("HTML Syntax Highlighter\n")
    apply_highlighting(html_content, syntax_config)
