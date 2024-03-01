import os


injected_script = """
    <script>
        mermaid.initialize({startOnLoad:true});
        document.querySelectorAll('pre.mermaid, pre>code.language-mermaid').forEach($el => {
        if ($el.tagName === 'CODE')
            $el = $el.parentElement
        $el.outerHTML = `
            <div class="mermaid">${$el.textContent}</div>
        `
        })
    </script>
    """


class Plugin:
    def import_head(self):
        return "<script src='static/js/mermaid.min.js'></script>"
    
    def add_script(self):
        return injected_script

    def __init__(self, config):
        self.name = "Mermaid integration"
        self.plugname = "mermaid"
        self.this_location = os.path.dirname(__file__)
        
    def get_plugin_name(self) -> str:
        """
        returns the name of the plugin
        """
        return self.name
