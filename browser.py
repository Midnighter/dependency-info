"""
Code browser example.

Run with:

    python code_browser.py PATH

"""

import sys
from textwrap import dedent

from rich.markdown import Markdown
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Footer, Header, Static
from textual import events

from depinfo.domain import DependencyReport
from dependency_tree import DependencyTree


class DependencyBrowser(App):
    """Textual code browser app."""

    CSS_PATH = "browser.css"
    BINDINGS = [
        # ("↑", "up", "Up"),
        # ("↓", "down", "Down"),
        # ("←", "collapse", "Collapse"),
        # ("→", "expand", "Expand"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Compose our UI."""
        self.title = "Dependency Browser"
        self.set_class(True, "-show-tree")
        max_depth = int(sys.argv[2])
        report = DependencyReport.from_root(sys.argv[1], [], max_depth=max_depth)
        yield Header()
        yield Container(
            Vertical(DependencyTree(report, max_depth), id="tree-view"),
            Vertical(Static(id="code", expand=True), id="code-view"),
        )
        yield Footer()

    def on_dependency_tree_node_selected(
        self, event: DependencyTree.NodeSelected
    ) -> None:
        """Called when the user selects a requirement in the tree."""
        code_view = self.query_one("#code", Static)
        package = event.requirement.package
        content = Markdown(
            dedent(
                f"""
                # {package.name}

                Version: {'not installed?' if package.version is None else package.version}
                """
            )
        )
        code_view.update(content)
        self.query_one("#code-view").scroll_home(animate=False)
        self.sub_title = package.name

    def on_dependency_tree_requirement_click(
        self, event: DependencyTree.RequirementClick
    ) -> None:
        """Called when the user clicks a requirement in the tree."""
        code_view = self.query_one("#code", Static)
        package = event.requirement.package
        content = Markdown(
            dedent(
                f"""
                # {package.name}

                Version: {'not installed?' if package.version is None else package.version}
                """
            )
        )
        code_view.update(content)
        self.query_one("#code-view").scroll_home(animate=False)
        self.sub_title = package.name

    def action_up(self, event: events.Key) -> None:
        """"""
        tree = self.query_one("#tree-view", expect_type=DependencyTree)
        tree.key_up(event)

    def action_down(self, event: events.Key) -> None:
        """"""
        tree = self.query_one("#tree-view", expect_type=DependencyTree)
        tree.key_down(event)

    def action_collapse(self) -> None:
        """"""
        tree = self.query_one("#tree-view", expect_type=DependencyTree)
        tree.expand(False)

    def action_expand(self) -> None:
        """"""
        tree = self.query_one("#tree-view", expect_type=DependencyTree)
        tree.expand(True)


if __name__ == "__main__":
    app = DependencyBrowser()
    app.run()
