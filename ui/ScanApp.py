from textual.app import App, ComposeResult
from textual.widgets import Header, Label
from textual.containers import Horizontal

class ScanApp(App):
    CSS_PATH = "styl.tcss"
    TITLE = "ScanApp"
    SUB_TITLE = "V1 - test"
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="testowa_sekcja"):
            yield Label("Testowy1", id="lewy")
            yield Label("", id="przerwa")
            yield Label("Testowy2", id="prawy")
   
    def on_button_pressed(self) -> None:
        self.exit()



if __name__ == "__main__":
    app = ScanApp()
    app.run()
