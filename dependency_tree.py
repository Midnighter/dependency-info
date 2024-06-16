from __future__ import annotations

import sys
from functools import lru_cache
from typing import NamedTuple

import rich.repr
from rich.console import RenderableType
from rich.text import Text
from textual.message import Message, MessageTarget
from textual.widgets import Tree, TreeNode

from depinfo.domain import DependencyReport, Package


class Requirement(NamedTuple):

    package: Package
    level: int


class DependencyTree(Tree[Requirement]):
    @rich.repr.auto
    class RequirementClick(Message, bubble=True):
        def __init__(self, sender: MessageTarget, requirement: Requirement) -> None:
            self.requirement = requirement
            super().__init__(sender)

    def __init__(
        self,
        report: DependencyReport,
        max_depth: int,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(
            report.root.name,
            Requirement(package=report.root, level=0),
            name=name,
            id=id,
            classes=classes,
        )
        self._report = report
        self._max_depth = max_depth
        # self.root.tree.guide_style = "black"

    def render_node(self, node: TreeNode[Requirement]) -> RenderableType:
        return self.render_tree_label(
            node,
            node.data.level < self._max_depth and bool(node.data.package.requirements),
            node.expanded,
            node.is_cursor,
            node.id == self.hover_node,
            self.has_focus,
        )

    @lru_cache(maxsize=1024 * 32)
    def render_tree_label(
        self,
        node: TreeNode[Requirement],
        allow_expansion: bool,
        is_expanded: bool,
        is_cursor: bool,
        is_hover: bool,
        has_focus: bool,
    ) -> RenderableType:
        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }
        label = Text(node.label) if isinstance(node.label, str) else node.label
        if is_hover:
            label.stylize("underline")
        if allow_expansion:
            label.stylize("bold")
            icon_label = Text(f"🐍 ", no_wrap=True, overflow="ellipsis") + label
        else:
            label.highlight_regex(r"\..*$", "italic")
            icon_label = Text("", no_wrap=True, overflow="ellipsis") + label

        if is_cursor and has_focus:
            cursor_style = self.get_component_styles("tree--cursor").rich_style
            label.stylize(cursor_style)

        icon_label.apply_meta(meta)
        return icon_label

    def on_styles_updated(self) -> None:
        self.render_tree_label.cache_clear()

    def on_mount(self) -> None:
        self.call_later(self.load_requirements, self.root)

    async def load_requirements(self, node: TreeNode[Requirement]):
        for pkg in node.data.package.requirements:
            node.add(
                pkg,
                Requirement(
                    package=self._report.packages[pkg], level=node.data.level + 1
                ),
            )
        node.loaded = True
        node.expand()
        self.refresh(layout=True)

    async def on_tree_control_node_selected(
        self, message: Tree.NodeSelected[Requirement]
    ) -> None:
        await self.emit(self.RequirementClick(self, message.node.data))
        if message.node.data.level < self._max_depth:
            if not message.node.loaded:
                await self.load_requirements(message.node)
                message.node.expand()
            else:
                message.node.toggle()
