import os
import inkex
from lxml import etree
from copy import deepcopy

try:
    from base64 import decodebytes
except ImportError:
    from base64 import decodestring as decodebytes

class ExportVisibleLayers(inkex.EffectExtension):
    """Exports the visible layers as SVG file"""
    def __init__(self):
        super(ExportVisibleLayers, self).__init__()

    def add_arguments(self, pars):
        pars.add_argument(
            "-d",
            "--directory",
            dest="directory",
            default=os.path.expanduser("~"),
            help="Existing destination directory",
        )
        pars.add_argument(
            "-f",
            "--file",
            dest="file_name",
            default="export.svg",
            help="File to export",
        )
        pars.add_argument(
            "-o",
            "--overwrite",
            type=inkex.Boolean,
            default=False,
            help="Overwrite existing exports?",
        )

    def effect(self):
        if not os.path.isdir(self.options.directory):
            os.makedirs(self.options.directory)

        path = os.path.join(self.options.directory, self.options.file_name)
        resDocument = deepcopy(self.document)
        root = resDocument.getroot();
        layers = resDocument.findall(inkex.addNS('g', 'svg'))
        layers2remove = []
        for layer in layers:
            if layer.groupmode == 'layer':
                if layer.style == 'display: none':
                    root.remove(layer)
        if not self.options.overwrite and os.path.exists(path):
            inkex.errormsg('Error: file exists: ' + path)
        else:
            with open(path, 'w') as fhl:
                fhl.write(etree.tostring(resDocument, encoding="unicode"))
        return self.document

if __name__ == '__main__':
    ExportVisibleLayers().run()
