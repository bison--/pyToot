

class TootRendererBase:
    def __init__(self, toot: dict, retoot=None):
        self.toot: dict = toot
        self.retoot: dict = retoot

    def render(self):
        raise NotImplementedError()

    def _render_toot(self):
        raise NotImplementedError()

    def _render_retoot(self):
        raise NotImplementedError()

    def _render_media_attachments(self):
        raise NotImplementedError()
