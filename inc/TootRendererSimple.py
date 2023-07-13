from datetime import datetime
import html2text
from .TootRendererBase import TootRendererBase


html_converter = html2text.HTML2Text()
html_converter.body_width = 0


class TootRendererSimple(TootRendererBase):

    def render(self):
        if self.retoot is not None:
            self.__render_retoot()

        self.__render_toot()
        self.__render_media_attachments()

    def _render_toot(self):
        print("Username: @" + self.toot["account"]["username"], "Toot-URL:", self.toot['url'])
        print(*self._get_toot_time(self.toot))

        print()
        print(html_converter.handle(self.toot["content"]).strip())
        print()

    def _render_retoot(self):
        print("** reTOOT **")
        print("Retoot by: @" + self.retoot["account"]["username"], "Retoot-URL:", self.retoot['url'])
        print(*self._get_toot_time(self.retoot))

    def _render_media_attachments(self):
        for attachment in self.toot.get("media_attachments", []):
            print(attachment["type"] + ":", attachment["url"])
            print("Description:", attachment["description"])

    @staticmethod
    def _get_toot_time(toot):
        current_time = datetime.utcnow()
        toot_time = datetime.strptime(toot["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")

        time_difference = current_time - toot_time
        return "Tooted on:", toot_time.strftime("%Y-%m-%d %H:%M:%S"), ' | ', "Ago:", time_difference
