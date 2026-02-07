from textual.widget import Widget
from textual.widgets import Header, Label, Input, Button, Footer
from textual.containers import Center, Horizontal, Vertical, VerticalGroup
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from post import Post

class PostWidget(VerticalGroup):

    DEFAULT_CSS = '''
        PostWidget {
            width: 60;
            border: solid $secondary;
            border-title-color: $primary;
        } 

        PostWidget:focus {
            background: $surface;
        }

        Label {
            margin: 1 2;
            text-wrap: wrap;
            width: 100%;
            height: auto;
        }
    '''

    def __init__(self, post: Post) -> None:
        super().__init__()
        self.post = post
        self.border_title = self.post.userName
        timestamp = str(self.post.timestamp)
        timestamp = timestamp[0:timestamp.rfind(":")]
        self.border_subtitle = timestamp
        self.can_focus = True

    def compose(self) -> ComposeResult:
        yield Label(self.post.message)

class Main(Screen):
    app: "SocialMedia"

    BINDINGS = [
        ("x", "remove_post", "Remove Post"),
        ("a", "add_post", "Add Post"),
        ("down", "focus_next", "Focus next post"),
        ("up", "focus_previous", "Focus previous post"),
        ("l", "logout", "Logout")
    ]

    posts: reactive[int] = reactive(0, recompose = True)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        if len(self.app.posts) == 0:
            with Center():
                yield Label("No Posts have been created!")
            with Center():
                yield Button("Make Post")
        else:
            for post in self.app.posts:
                yield PostWidget(post)

    def on_button_pressed(self, button: Button.Pressed) -> None:
        self.app.pop_screen()
        self.app.push_screen("PostCreation")
    
    def updatePosts(self):
        self.posts = len(self.app.posts)
        
    def on_mount(self) -> None:
        self.watch(self.app, "posts", self.updatePosts) 

    def action_add_post(self) -> None:
        self.app.switch_screen("PostCreation")

    def action_remove_post(self) -> None:
        if isinstance(self.focused, PostWidget):
            self.app.posts.remove(self.focused.post)
            self.focused.remove()
            self.updatePosts()

    def action_logout(self) -> None:
        self.app.sub_title = ""
        self.app.username = ""
        self.app.switch_screen("Login")

    def action_focus_next(self) -> None:
        self.screen.focus_next()

    def action_focus_previous(self) -> None:
        self.screen.focus_previous()


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
        self.app.switch_screen("Main")

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
        self.app.switch_screen("Main")
        self.app.sub_title = event.value

class SocialMedia(App):

    username:reactive[str] = reactive("")

    posts:reactive[list[Post]] = reactive([], always_update = True)

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