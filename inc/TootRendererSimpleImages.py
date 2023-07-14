from .TootRendererSimple import TootRendererSimple
from .TerminalImage import TerminalImage

terminal_image = TerminalImage()


class TootRendererSimpleImages(TootRendererSimple):
    def _render_media_attachments(self):
        for attachment in self.toot.get("media_attachments", []):
            if attachment["type"] == 'image':
                terminal_image.render_image(attachment["url"])

            print(attachment["type"] + ":", attachment["url"])
            print("Description:", attachment["description"])
