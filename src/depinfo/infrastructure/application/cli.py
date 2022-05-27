# Copyright (c) 2022, Moritz E. Beber
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import logging
from typing import List, Optional

from depinfo.domain import DependencyReport

from .display_service_factory import DisplayServiceFactory, DisplayType


MAX_DEPTH = 5


def parse_arguments(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Define and immediately parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Display a package's dependencies, platform, and Python "
        "information.",
    )
    parser.add_argument(
        "package_name",
        metavar="PACKAGE",
        help="The package's distribution name.",
    )
    default_build_tools = "conda,flit,hatch,mamba,pbr,pip,poetry,setuptools,wheel"
    parser.add_argument(
        "--build-tools",
        help=f"A comma separated list of Python package managers "
        f"(default {default_build_tools}).",
        default=default_build_tools,
    )
    default_max_depth = 1
    parser.add_argument(
        "-d",
        "--max-depth",
        type=int,
        help=f"The maximum desired depth of nested dependencies to show "
        f"(default {default_max_depth}). Should be >= 0 and <{MAX_DEPTH}.",
        default=default_max_depth,
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Display information as markdown tables (default false).",
    )
    default_log_level = "WARNING"
    parser.add_argument(
        "-l",
        "--log-level",
        help=f"The desired log level (default {default_log_level}).",
        choices=("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"),
        default=default_log_level,
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    """Coordinate argument parsing, input validation, and program execution."""
    args = parse_arguments(argv)
    logging.basicConfig(level=args.log_level, format="[%(levelname)s] %(message)s")
    assert args.max_depth >= 0, "The maximum depth must be >=0."
    assert args.max_depth < MAX_DEPTH, "Don't exaggerate!"
    report = DependencyReport.from_root(
        args.package_name,
        [token.strip() for token in args.build_tools.split(",")],
        max_depth=args.max_depth,
    )
    if args.markdown:
        service = DisplayServiceFactory.create(DisplayType.Markdown, report)
    else:
        service = DisplayServiceFactory.create(DisplayType.Simple, report)
    service.display(max_depth=args.max_depth)
