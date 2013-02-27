import sublime, sublime_plugin

from parsehex import *

class IntelhexCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """
        Main plugin logic
        """
        view = self.view
        regions = view.sel()
        filename = view.file_name()

        # Text is selected: if there are more than 1 region or region one and it's not empty
        if len(regions) > 1 or not regions[0].empty():
            for region in view.sel():
                if not region.empty():
                    s = view.substr(region)
                    s = self.decode_intel_hex(s, filename)
                    view.replace(edit, region, s)
        else:
            # Nothing selected: format all text into a new window
            window = self.view.window()
            new_view = window.new_file()
            new_view.set_scratch(True)

            alltextreg = sublime.Region(0, view.size())
            s = view.substr(alltextreg)
            s = self.decode_intel_hex(s, filename)
            new_view.replace(edit, alltextreg, s)

    def decode_intel_hex(self, lines, filename):
        d = IntelHexDecoder()
        c = []
        c.append("# Decoded Intel Hex file " + filename)
        for line in lines.split('\n'):
            res = d.decode_line(line.strip())
            if res is None:
                c.append(line)
            else:
                c.append(res)

        return '\n'.join(c)
