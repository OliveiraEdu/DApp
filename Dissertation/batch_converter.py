import os
import re
import base64
from IPython.display import Image, display
import requests
import matplotlib.pyplot as plt
import icecream as ic


# Initialize IceCream for logging (optional)
ic.configureOutput(includeContext=True)

def parse_markdown(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find all Mermaid blocks in the Markdown file
    mermaid_blocks = re.findall(r'```mermaid\n(.*?)\n```', content, re.DOTALL)
    ic.logging(f"Mermaid blocks found: {len(mermaid_blocks)}")
    return mermaid_blocks

def mm(graph):
    graphbytes = graph.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    img_url = "https://mermaid.ink/img/" + base64_string
    response = requests.get(img_url)
    
    # Save the image to a local file
    if not os.path.exists('images'):
        os.makedirs('images')
    
    filename = f"graph_{base64_string[:10]}.png"  # Add your code here


def main():
    pass
def parse_markdown(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
        matches = re.findall('```mermaid', text)
    # This should be a regular expression to find code blocks in the Markdown language
    mermaid\n```', text, re.IGNORECASE)
    return matches


if __name__ == "__main__":
    file_path = "test.md"
    parse_markdown(file_path)
# Your goal is to make the function that finds all ```mermaid blocks in a given markdown file and returns them. Could you please help me with this?
    FileNotFoundError: [Errno 2] No such file or directory: 'yourfile'