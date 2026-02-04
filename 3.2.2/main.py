from textual.widgets import Header, Label, Input, Button 
from textual.containers import Center, Horizontal, Vertical
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
        else:
            with Center():
                yield Label(str(self.app.posts[0]))

    def on_button_pressed(self, button: Button.Pressed) -> None:
        self.app.pop_screen()
        self.app.push_screen("PostCreation")
    
    def updatePosts(self):
        self.app.notify("Posts updated")
        
    def on_mount(self) -> None:
        self.watch(self.app, "posts", self.updatePosts) 

class PostCreation(Screen):

    app: "SocialMedia"

    def compose(self):
        yield Header()
        with Vertical():
            with Center():
                yield Label("Post Creation")
            with Center():
                yield Input(id = "message", placeholder = "Enter message...")
            with Horizontal():
                yield Button("Cancel", "warning")
                yield Button("Post", "success")

    def on_button_pressed(self, button: Button.Pressed) -> None:
        inputField:Input = self.query_one("#message", Input)
        if (button.button.label == "Post"):
            if (inputField.value):
                self.app.posts += [Post(self.app.username, inputField.value)]
            else:
                return

        inputField.clear()
        self.app.pop_screen()
        self.app.push_screen("Main")

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

    username:reactive[str] = reactive("")

    posts:reactive[list[Post]] = reactive([])

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