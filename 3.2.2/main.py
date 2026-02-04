from textual.widgets import Header, Label, Input, Button 
from textual.containers import Center, Horizontal
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from post import Post

class Main(Screen):

    app: "SocialMedia"

    def compose(self) -> ComposeResult:
        yield Header()
        if len(self.app.posts) == 0:
            with Center():
                yield Label("No Posts have been created!")
            with Center():
                yield Button("Make Post")

    def on_button_pressed(self, button: Button.Pressed) -> None:
        self.app.pop_screen()
        self.app.push_screen("PostCreation")

class PostCreation(Screen):

    app: "SocialMedia"

    def compose(self):
        yield Header()
        with Center():
            yield Label("Post Creation")
        with Center():
            with Horizontal():
                yield Button("Cancel", "warning")
                yield Button("Post", "success")

class Login(Screen):

    app: "SocialMedia"

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Label("Please enter a username:")
        with Center():
            yield Input()
        
    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.app.username = event.value
        event.input.clear()
        self.app.pop_screen()
        self.app.push_screen("Main")
        self.app.sub_title = event.value

class SocialMedia(App):

    posts:reactive[list] = reactive([])

    username:reactive[str] = reactive("")

    CSS_PATH = "main.tcss"

    def on_mount(self) -> None:
        self.title = "Social Media App"
        self.theme = "gruvbox"
        self.install_screen(Login(), name = "Login")
        self.install_screen(Main(), name = "Main")
        self.install_screen(PostCreation(), name = "PostCreation")
        self.push_screen("Login")


if __name__ == "__main__":
    app = SocialMedia()
    app.run()