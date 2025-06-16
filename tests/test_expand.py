from exdata import Cell, Column, Row
from tests import make_workbook


def test_cell_with_size_and_offset() -> None:
    """Cell with size and offset.

    +--+--+--+--+---+
    |  |  |  |  | 2 |
    +--+--+--+--+   |
    |  |  |  |  |   |
    +--+--+--+--+   |
    |  |  |  1  |   |
    +--+--+     |   |
    |  |  |     |   |
    +--+--+-----+---+
    """
    wb = make_workbook(
        data=[
            Row(
                [
                    Cell('1', x_offset=2, y_offset=2, rows=2, columns=2),
                    Cell('2'),
                ]
            ),
        ]
    )

    mc = wb['Test'].merged_cells.sorted()

    assert wb['Test']['C3'].value == '1'
    assert mc[0].coord == 'C3:D4'

    assert wb['Test']['E1'].value == '2'
    assert mc[1].coord == 'E1:E4'


def test_row_expand() -> None:
    """Row expand.

    +---+-----------+---+
    | 1 |     2     | 7 |
    |   +-----------+   |
    |   |     3     |   |
    |   +---+---+---+   |
    |   | 4 | 5 | 6 |   |
    +---+---+---+---+---+
    """
    wb = make_workbook(
        data=[
            Row(
                [
                    Cell('1'),
                    Column(
                        data=[
                            Cell('2'),
                            Cell('3'),
                            Row(
                                data=[
                                    Cell('4'),
                                    Cell('5'),
                                    Cell('6'),
                                ]
                            ),
                        ]
                    ),
                    Cell('7'),
                ]
            )
        ],
    )

    mc = wb['Test'].merged_cells.sorted()

    assert wb['Test']['A1'].value == '1'
    assert mc[0].coord == 'A1:A3'

    assert wb['Test']['B1'].value == '2'
    assert mc[1].coord == 'B1:D1'

    assert wb['Test']['B2'].value == '3'
    assert mc[2].coord == 'B2:D2'

    assert wb['Test']['B3'].value == '4'
    assert wb['Test']['C3'].value == '5'
    assert wb['Test']['D3'].value == '6'

    assert wb['Test']['E1'].value == '7'
    assert mc[3].coord == 'E1:E3'


def test_column_expand() -> None:
    """Column expand.

    +--+---+---+---+
    |  |   | 4 | 7 |
    +--+---+   +---+
    |  | 1 |   | 8 |
    +--+---+---+   |
    |  | 2 | 5 |   |
    +--+---+---+---+
    |  | 3 | 6 | 9 |
    +--+---+---+---+
    """
    wb = make_workbook(
        data=[
            Row(
                [
                    Column(
                        data=[
                            Cell(value='1'),
                            Cell(value='2'),
                            Cell(value='3'),
                        ],
                        x_offset=1,
                        y_offset=1,
                    ),
                    Column(
                        data=[
                            Cell(value='4'),
                            Cell(value='5'),
                            Cell(value='6'),
                        ],
                    ),
                    Column(
                        data=[
                            Cell(value='7', expand=False),
                            Cell(value='8'),
                            Cell(value='9'),
                        ],
                    ),
                ]
            )
        ]
    )

    mc = wb['Test'].merged_cells.sorted()

    assert wb['Test']['B2'].value == '1'
    assert wb['Test']['B3'].value == '2'
    assert wb['Test']['B4'].value == '3'

    assert wb['Test']['C1'].value == '4'
    assert mc[0].coord == 'C1:C2'
    assert wb['Test']['C3'].value == '5'
    assert wb['Test']['C4'].value == '6'

    assert wb['Test']['D1'].value == '7'
    assert wb['Test']['D2'].value == '8'
    assert mc[1].coord == 'D2:D3'
    assert wb['Test']['D4'].value == '9'
