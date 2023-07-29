import sys
from inc import helper
from inc.Cacher import Cacher
import conf_loader as conf

try:
    import img2unicode
except ModuleNotFoundError:
    pass


class TerminalImage:
    OPTIMIZER_DUAL_BLOCK = 'dual_block'
    OPTIMIZER_HALF = 'half'
    OPTIMIZER_SPACE = 'space'
    OPTIMIZER_QUAD_DUAL = 'quad_dual'
    OPTIMIZER_EXACT_DUAL_BLOCK = 'exact_dual_block'
    OPTIMIZER_EXPERIMENTAL = 'ex'

    def __init__(self):
        if not conf.TERMINAL_IMAGES:
            return

        self.optimizer = None

        if not TerminalImage.is_valid_render(conf.TERMINAL_IMAGE_OPTIMIZER):
            helper.print_color(
                'Invalid TERMINAL_IMAGES_OPTIMIZER ({0}), using default: {1}'.format(
                    conf.TERMINAL_IMAGE_OPTIMIZER,
                    TerminalImage.OPTIMIZER_DUAL_BLOCK
                ),
                helper.Color.YELLOW
            )
            conf.TERMINAL_IMAGE_OPTIMIZER = TerminalImage.OPTIMIZER_DUAL_BLOCK

        if conf.TERMINAL_IMAGE_OPTIMIZER == TerminalImage.OPTIMIZER_DUAL_BLOCK:
            self.optimizer = img2unicode.FastGenericDualOptimizer("block")
        elif conf.TERMINAL_IMAGE_OPTIMIZER == TerminalImage.OPTIMIZER_HALF:
            self.optimizer = img2unicode.HalfBlockDualOptimizer()
        elif conf.TERMINAL_IMAGE_OPTIMIZER == TerminalImage.OPTIMIZER_SPACE:
            self.optimizer = img2unicode.SpaceDualOptimizer()
        elif conf.TERMINAL_IMAGE_OPTIMIZER == TerminalImage.OPTIMIZER_QUAD_DUAL:
            self.optimizer = img2unicode.FastQuadDualOptimizer()
        elif conf.TERMINAL_IMAGE_OPTIMIZER == TerminalImage.OPTIMIZER_EXACT_DUAL_BLOCK:
            # best results, but slow
            self.optimizer = img2unicode.ExactGenericDualOptimizer("block")
        elif conf.TERMINAL_IMAGE_OPTIMIZER == TerminalImage.OPTIMIZER_EXPERIMENTAL:
            # used for faster mode testing
            helper.print_color('EXPERIMENTAL IMAGE OPTIMIZER', helper.Color.YELLOW)
            self.optimizer = img2unicode.BaseDualOptimizer()

        self.cacher = Cacher()

    @staticmethod
    def is_valid_render(renderer):
        return renderer in [
            TerminalImage.OPTIMIZER_DUAL_BLOCK,
            TerminalImage.OPTIMIZER_HALF,
            TerminalImage.OPTIMIZER_SPACE,
            TerminalImage.OPTIMIZER_QUAD_DUAL,
            TerminalImage.OPTIMIZER_EXACT_DUAL_BLOCK,
            TerminalImage.OPTIMIZER_EXPERIMENTAL
        ]

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
