import io
from pathlib import Path
from typing import IO

from xlsxwriter import Workbook
from xlsxwriter.worksheet import Format as XlsxFormat, Worksheet

from exdata.struct import (
    Cell,
    Column,
    Default,
    Format,
    RichValue,
    Row,
    Sheet,
    Size,
)


class XlsxExporter:
    """Exports sheets to an XLSX file format.

    This class handles formatting, column width settings, and workbook
    options for exporting sheets.

    Attributes:
        workbook_options (dict): Options for configuring the workbook.
    """

    workbook_options: dict

    def __init__(
        self,
        *,
        sheets: list[Sheet],
        formats: dict | None = None,
        workbook_options: dict | None = None,
        buffer: IO | Path | str | None = None,
    ) -> None:
        """Initializes the XLSX exporter.

        Args:
            sheets (list[Sheet]): The sheets to be included in the export.
            formats (dict | None): Formatting options for cells.
            workbook_options (dict | None): Workbook configuration.
            buffer (io.IOBase | Path | str | None): A buffer for workbook
                storage.
        """
        self.sheets = sheets
        self.formats = formats or {}

        self.workbook_options = workbook_options
        if self.workbook_options is None:
            self.workbook_options = {'in_memory': True}

        self.buffer = buffer or io.BytesIO()

        self.workbook = Workbook(self.buffer, options=self.workbook_options)

        self._formats = {}
        self.init_formats(self.workbook)

    def export(self) -> IO:
        """Exports the sheets as an XLSX file.

        Returns:
            bytes: The binary representation of the exported workbook.
        """
        for sheet in self.sheets:
            self.write_sheet(workbook=self.workbook, sheet=sheet)

        self.workbook.close()

        if hasattr(self.buffer, 'seek'):
            self.buffer.seek(0)

        return self.buffer

    def init_formats(self, workbook: Workbook) -> None:
        """Initializes formatting styles for the workbook.

        Args:
            workbook (Workbook): The workbook where formats are applied.
        """
        for format_name, format_properties in self.formats.items():
            self._formats[format_name] = workbook.add_format(format_properties)

    def get_format(self, name: str | None) -> XlsxFormat | None:
        """Retrieves a predefined format by its name.

        Args:
            name (str | None): The name of the format.

        Returns:
            XlsxFormat | None: The requested format, or None if name is not
                provided.
        """
        if name is None:
            return None

        return self._formats[name]

    def write_rich(
        self,
        worksheet: Worksheet,
        row_number: int,
        col_number: int,
        value: RichValue,
        cell_format: XlsxFormat | None = None,
    ) -> int:
        """Writes rich text content into a cell.

        Args:
            worksheet (Worksheet): The target worksheet.
            row_number (int): Row index for the cell.
            col_number (int): Column index for the cell.
            value (RichValue): Rich text to write.
            cell_format (str | None): Formatting options.

        Returns:
            int: Status code of the write operation.
        """
        result = []

        for item in value.value:
            if isinstance(item, Format):
                result.append(self.get_format(item.name))
            else:
                result.append(str(item))

        if cell_format:
            result.append(cell_format)

        return worksheet.write_rich_string(
            row_number,
            col_number,
            *result,
        )

    @staticmethod
    def write_row(
        worksheet: Worksheet,
        row_number: int,
        col_number: int,
        row: Row,
        content_size: Size,
        cell_format: str | None = None,
    ) -> bool:
        """Writes a row of data into the worksheet.

        Args:
            worksheet (Worksheet): The target worksheet.
            row_number (int): The row index where data will be written.
            col_number (int): The column index for the first cell.
            row (Row): The row object containing the data.
            content_size (Size): The total size of the row content.
            cell_format (str | None): Formatting options.

        Returns:
            bool: True if successful, False otherwise.
        """
        row_number += row.y_offset
        col_number += row.x_offset
        cell_format = row.format or cell_format

        content_size: Size = content_size.clear_offset(
            x_offset=row.x_offset,
            y_offset=row.y_offset,
        )
        row_size: Size = row.size.clear_offset(
            x_offset=row.x_offset,
            y_offset=row.y_offset,
        )

        for item in row:
            item_size = item.size
            if row.expand and item.expand:
                item_size = Size(
                    rows=content_size.rows,
                    columns=(
                        content_size.columns
                        - row_size.columns
                        + item_size.columns
                        if content_size.columns > row_size.columns
                        else item_size.columns
                    ),
                )
                content_size.columns -= item_size.columns

            worksheet.write(
                row_number,
                col_number,
                item,
                item_size,
                cell_format,
            )

            col_number += item_size.columns

        for i, height in enumerate(row.heights):
            worksheet.set_row(row=row_number + i, height=height)

        return True

    @staticmethod
    def write_column(
        worksheet: Worksheet,
        row_number: int,
        col_number: int,
        column: Column,
        content_size: Size,
        cell_format: str | None = None,
    ) -> bool:
        """Writes a column of data into the worksheet.

        Args:
            worksheet (Worksheet): The target worksheet.
            row_number (int): The row index where the column starts.
            col_number (int): The column index where data will be written.
            column (Column): The column object containing the data.
            content_size (Size): The total size of the column content.
            cell_format (str | None): Formatting options.

        Returns:
            bool: True if successful, False otherwise.
        """
        row_number += column.y_offset
        col_number += column.x_offset
        cell_format = column.format or cell_format

        content_size: Size = content_size.clear_offset(
            x_offset=column.x_offset,
            y_offset=column.y_offset,
        )
        column_size: Size = column.size.clear_offset(
            x_offset=column.x_offset,
            y_offset=column.y_offset,
        )

        for item in column:
            item_size = item.size
            if column.expand and item.expand:
                item_size = Size(
                    rows=(
                        content_size.rows - column_size.rows + item_size.rows
                        if content_size.rows > column_size.rows
                        else item_size.rows
                    ),
                    columns=content_size.columns,
                )
                content_size.rows -= item_size.rows

            worksheet.write(
                row_number,
                col_number,
                item,
                item_size,
                cell_format,
            )

            row_number += item_size.rows

        return True

    def write_cell(
        self,
        worksheet: Worksheet,
        row_number: int,
        col_number: int,
        cell: Cell,
        content_size: Size,
        cell_format: str | None = None,
    ) -> int:
        """Writes a single cell to the worksheet.

        Args:
            worksheet (Worksheet): The target worksheet.
            row_number (int): The row index where the cell is written.
            col_number (int): The column index where data will be written.
            cell (Cell): The cell object containing data and formatting.
            content_size (Size): The size constraints for the cell.
            cell_format (str | None): Formatting options.

        Returns:
            int: Status code of the write operation.
        """
        cell_format = self.get_format(cell.format or cell_format)

        row_number += cell.y_offset
        col_number += cell.x_offset

        content_size: Size = content_size.clear_offset(
            x_offset=cell.x_offset,
            y_offset=cell.y_offset,
        )

        last_row = row_number + content_size.rows - 1
        last_col = col_number + content_size.columns - 1

        if last_row > row_number or last_col > col_number:
            worksheet.merge_range(
                first_row=row_number,
                first_col=col_number,
                last_row=last_row,
                last_col=last_col,
                data=None,
                cell_format=cell_format,
            )

        return worksheet.write(row_number, col_number, cell.value, cell_format)

    def write_sheet(self, workbook: Workbook, sheet: Sheet) -> None:
        """Writes an entire sheet to the workbook.

        Args:
            workbook (Workbook): The target workbook.
            sheet (Sheet): The sheet object containing data and settings.
        """
        worksheet = workbook.add_worksheet(name=sheet.name)
        worksheet.add_write_handler(RichValue, self.write_rich)
        worksheet.add_write_handler(Row, self.write_row)
        worksheet.add_write_handler(Cell, self.write_cell)
        worksheet.add_write_handler(Column, self.write_column)

        row_number = 0
        for row in sheet:
            worksheet.write(
                row_number,
                0,
                row,
                row.size,
                sheet.format,
            )

            row_number += row.size.rows

        if sheet.autofit_max_width is not None:
            autofit_kwargs = {}
            if sheet.autofit_max_width is not Default:
                autofit_kwargs = {'max_width': sheet.autofit_max_width}

            worksheet.autofit(**autofit_kwargs)

        for column, size in sheet.column_width.items():
            worksheet.set_column(
                first_col=column,
                last_col=column,
                width=size,
            )
