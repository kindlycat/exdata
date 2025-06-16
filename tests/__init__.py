from collections.abc import Iterable

from openpyxl import Workbook, load_workbook

from exdata import Row, Sheet, XlsxExporter
from exdata.struct import Default


def make_workbook(
    data: Iterable[Row],
    formats: dict | None = None,
    column_width: dict | None = None,
    autofit_max_width: int | None = Default,
) -> Workbook:
    exporter = XlsxExporter(
        sheets=[
            Sheet(
                data=data,
                name='Test',
                column_width=column_width or {},
                autofit_max_width=autofit_max_width,
            ),
        ],
        formats=formats,
    )
    return load_workbook(exporter.export(), rich_text=True)
