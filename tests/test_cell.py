import pytest

from exdata.struct import Cell


@pytest.mark.parametrize(
    ('cell', 'rows', 'columns'),
    [
        (Cell('1'), 1, 1),
        (Cell('1', rows=2, columns=1), 2, 1),
        (Cell('1', rows=1, columns=2), 1, 2),
        (Cell('1', rows=2, columns=2), 2, 2),
        (Cell('1', x_offset=1, y_offset=1), 2, 2),
        (Cell('1', x_offset=1, y_offset=1, rows=2, columns=2), 3, 3),
    ],
)
def test_cell_size(cell: Cell, rows: int, columns: int) -> None:
    assert cell.size.rows == rows
    assert cell.size.columns == columns
