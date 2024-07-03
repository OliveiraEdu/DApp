import base64
from IPython.display import Image, display
import requests
import os

def mm(graph):
    graphbytes = graph.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    img_url = "https://mermaid.ink/img/" + base64_string
    response = requests.get(img_url)
    
    with open(os.path.join("fig_test.jpg"), 'wb') as f:
        f.write(response.content)

def read_md_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Assuming the .md file is named "diagram.md" and is in the same directory as the script
md_filename = os.path.join(os.getcwd(), "test.md")
print(md_filename)
graph = read_md_file(md_filename)
print(graph)

mm(graph)


#-

