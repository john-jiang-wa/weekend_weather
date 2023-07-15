import argparse
import code2flow
import os
import json
import mermaid

def get_py_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.py')]

def code_to_mermaid(directory):
    code2flow.code2flow(get_py_files(directory), 'tmp.json')

    with open('tmp.json') as f:
        content = json.load(f)

    json_str = json.dumps(content)

    data = json.loads(json_str)

    nodes = data["graph"]["nodes"]
    edges = data["graph"]["edges"]

    mermaid_script = "graph TD;\n"

    for node_id, node in nodes.items():
        mermaid_script += f"{node_id}(\"{node['label']}\")\n"

    for edge in edges:
        mermaid_script += f"{edge['source']}-->{edge['target']};\n"
        
    os.remove("tmp.json")
    return mermaid_script
    
def mermaid_to_html(mermaid_script, output_file):
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mermaid Diagram</title>
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        <script>mermaid.initialize({{startOnLoad:true}});</script>
    </head>
    <body>
        <div class="mermaid">
            {mermaid_script}
        </div>
    </body>
    </html>
    """

    html_content = html_template.format(mermaid_script=mermaid_script)

    with open(output_file, 'w') as f:
        f.write(html_content)    

def main():
    parser = argparse.ArgumentParser(description='Generate a Mermaid flowchart from Python code.')
    parser.add_argument('--directory', type=str, required=True, help='The directory of the Python code.')
    parser.add_argument('--output', type=str, required=True, help='The output path for the HTML file.')
    args = parser.parse_args()

    mermaid_script = code_to_mermaid(args.directory)
    mermaid_to_html(mermaid_script, args.output)

if __name__ == '__main__':
    main()
