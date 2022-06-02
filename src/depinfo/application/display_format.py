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


"""Provide a controlled vocabulary for display formats."""


from enum import Enum, auto


class AutoNameEnum(Enum):
    """Define an enumeration base class whose fields' names match the values."""

    @staticmethod
    def _generate_next_value_(name: str, _, __, ___) -> str:
        """Use a field's name as its value."""
        return name


class DisplayFormat(AutoNameEnum):
    """Define an enumeration for supported display formats."""

    Simple = auto()
    Markdown = auto()
    Rich = auto()
    Textual = auto()
