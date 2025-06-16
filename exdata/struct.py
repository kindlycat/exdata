from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator


class Default:
    """Placeholder for unset attributes, when `None` is a valid value."""


@dataclass(kw_only=True)
class Size:
    """Represents the size of an element in terms of rows and columns.

    Attributes:
        rows (int): The number of rows occupied.
        columns (int): The number of columns occupied.
    """

    rows: int
    columns: int

    def clear_offset(self, x_offset: int, y_offset: int) -> Size:
        """Removes the provided offset values from the size.

        Args:
            x_offset (int): The x-axis offset.
            y_offset (int): The y-axis offset.

        Returns:
            Size: The adjusted size without the offsets.
        """
        return Size(
            rows=self.rows - y_offset,
            columns=self.columns - x_offset,
        )


@dataclass
class Format:
    """Represents a formatting style by name.

    Attributes:
        name (str): The name of the format.
    """

    name: str


@dataclass
class RichValue:
    """Represents rich text content, including formatting elements.

    Attributes:
        value (list[Any]): A list of rich text and formatting elements.
    """

    value: list[Any]


@dataclass
class Cell:
    """Represents a spreadsheet cell.

    Attributes:
        value (Any): The value stored in the cell.
        format (str | None): The formatting style for the cell.
        columns (int): The number of columns the cell spans.
        rows (int): The number of rows the cell spans.
        x_offset (int): Horizontal offset from its parent.
        y_offset (int): Vertical offset from its parent.
        expand (bool): Whether the cell expands with its parent.
    """

    value: Any
    format: str | None = None
    columns: int = 1
    rows: int = 1
    x_offset: int = 0
    y_offset: int = 0
    expand: bool = True

    @cached_property
    def size(self) -> Size:
        """Computes the total size of the cell including offsets.

        Returns:
            Size: The total size of the cell.
        """
        return Size(
            rows=self.rows + self.y_offset,
            columns=self.columns + self.x_offset,
        )


@dataclass
class Column:
    """Represents a column in a spreadsheet.

    Attributes:
        data (Iterable[Cell | Row | Column]): Initial column data.
        format (str | None): The formatting style for the column.
        x_offset (int): Horizontal offset from its parent.
        y_offset (int): Vertical offset from its parent.
        expand (bool): Whether the column expands with its parent.
    """

    data: Iterable[Cell | Row | Column]
    format: str | None = None
    x_offset: int = 0
    y_offset: int = 0
    expand: bool = True

    def __iter__(self) -> Iterator[Cell]:
        """Iterates over the column's contents.

        Returns:
            Iterator[Cell]: An iterator over the column items.
        """
        yield from self.data

    @cached_property
    def size(self) -> Size:
        """Computes the total size of the column including offsets.

        Returns:
            Size: The computed size.
        """
        rows: int = 0
        columns: int = 0

        for item in self:
            rows += item.size.rows
            columns = max(columns, item.size.columns)

        return Size(
            rows=rows + self.y_offset,
            columns=columns + self.x_offset,
        )


@dataclass
class Row:
    """Represents a row in a spreadsheet.

    Attributes:
        data (Iterable[Cell | Column | Row]): Initial row data.
        heights (list[int] | None): Row heights for each item.
        format (str | None): The formatting style for the row.
        expand (bool): Whether the row expands with its parent.
        x_offset (int): Horizontal offset from its parent.
        y_offset (int): Vertical offset from its parent.
    """

    data: Iterable[Cell | Column | Row]
    heights: list[int] | None = field(default_factory=list)
    format: str | None = None
    expand: bool = True
    x_offset: int = 0
    y_offset: int = 0

    def __iter__(self) -> Iterator[Cell | Column]:
        """Iterates over the row's contents.

        Returns:
            Iterator[Cell | Column]: An iterator over the row items.
        """
        yield from self.data

    @cached_property
    def size(self) -> Size:
        """Computes the total size of the row including offsets.

        Returns:
            Size: The computed size.
        """
        rows: int = 0
        columns: int = 0

        for item in self:
            rows = max(rows, item.size.rows)
            columns += item.size.columns

        return Size(
            rows=rows + self.y_offset,
            columns=columns + self.x_offset,
        )


@dataclass(kw_only=True)
class Sheet:
    """Represents a sheet in a workbook.

    Attributes:
        data (Iterable[Row]): The rows contained in the sheet.
        name (str | None): The name of the sheet.
        format (str | None): The formatting style for the sheet.
        column_width (dict[int, int]): Mapping of column indices to widths.
        autofit_max_width (int | None | Default): Max width for auto-fit
            columns.
    """

    data: Iterable[Row]
    name: str | None = None
    format: str | None = None
    column_width: dict[int, int] = field(default_factory=dict)
    autofit_max_width: int | None | Default = Default

    def __iter__(self) -> Iterator[Row]:
        """Iterates over the sheet's rows.

        Returns:
            Iterator[Row]: An iterator over the sheet rows.
        """
        yield from self.data
