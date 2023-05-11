import sys
from inc.Cacher import Cacher
import conf_loader as conf
try:
    import img2unicode
except ModuleNotFoundError:
    pass


class TerminalImage:
    def __init__(self):
        if not conf.TERMINAL_IMAGES:
            return

        self.optimizer = img2unicode.FastGenericDualOptimizer("block")
        self.cacher = Cacher()

    def render_image(self, image_path):
        if not conf.TERMINAL_IMAGES:
            return

        renderer = img2unicode.Renderer(
            default_optimizer=self.optimizer,
            max_w=conf.TERMINAL_IMAGE_MAX_WIDTH,
            max_h=conf.TERMINAL_IMAGE_MAX_HEIGHT
        )

        local_image = self.cacher.get_image_cached(image_path)
        if local_image:
            renderer.render_terminal(local_image, sys.stdout)
