import re


NOTEBOOK_HTML_PATHS = [
    'templates/components.html',
    'templates/models.html',
]  # paths for a script ran from Makefile location (project root)

CLASS_STYLES = {
    'class="prompt input_prompt"': 'class="prompt input_prompt uk-text-small uk-text-muted"',
    'class="prompt output_prompt"': 'class="prompt output_prompt uk-text-small uk-text-muted"',
    'class="output"': 'class="prompt uk-text-small uk-text-muted"',
    '<a class="anchor-link".*>&#182;</a>': '',
    '<span class="c1">': '<span class="c1 uk-text-muted">',
    '<span class="ow">': '<span class="ow uk-text-bold">',  # keywords
    '<span class="kn">': '<span class="kn uk-text-bold">',  # keywords
    '<span class="k">': '<span class="k uk-text-bold">',  # keywords
    '<span class="p">': '<span class="p uk-text-bold">',  # keywords
    '<span class="mi">': '<span class="mi uk-text-primary">',  # constants
    '<span class="s2">': '<span class="s2 uk-text-primary">',  # strings
    '<span class="n">': '<span class="n uk-text-emphasis">',  # names
    '<span class="nb">': '<span class="nb uk-text-emphasis">',  # names
    '<pre>': '<pre><code>',
    '</pre>': '</code></pre>',
}


def replace_in_file(pattern, repl, filepath):
    text = "".join(open(filepath, "r").readlines())
    substituted = re.sub(pattern, repl, text)
    open(filepath, "w").write(substituted)

def apply_class_styles(html_paths=NOTEBOOK_HTML_PATHS, class_styles=CLASS_STYLES):
    for path in html_paths:
        for class_key in class_styles:
            replace_in_file(class_key, class_styles[class_key], path)


if __name__ == '__main__':
    apply_class_styles()
