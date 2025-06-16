import pytest

from exdata.struct import Cell, Column, Row


@pytest.mark.parametrize(
    ('data', 'expected_rows', 'expected_columns'),
    [
        ([Cell('1')], 1, 1),
        ([Cell('1', x_offset=2, y_offset=2)], 3, 3),
        ([Cell('1', rows=3, columns=3)], 3, 3),
        (
            [
                Cell('1', rows=3, columns=3, x_offset=2),
                Cell('2', rows=4, columns=3, x_offset=2),
            ],
            7,
            5,
        ),
        (
            [
                Row(
                    [
                        Cell('1'),
                        Cell('2'),
                    ]
                )
            ],
            1,
            2,
        ),
        (
            [
                Row(
                    [
                        Cell('1'),
                        Column(
                            [
                                Row(
                                    [
                                        Cell('2.1'),
                                        Column(
                                            [
                                                Cell('3.1'),
                                                Cell('3.2'),
                                            ]
                                        ),
                                    ]
                                ),
                                Cell('2.2'),
                            ]
                        ),
                    ]
                ),
            ],
            3,
            3,
        ),
        (
            [
                Row(
                    [
                        Cell('1'),
                        Column(
                            [
                                Cell('2.1'),
                                Row(
                                    [
                                        Cell('2.2'),
                                        Column(
                                            [
                                                Cell('3.1'),
                                                Cell(
                                                    value='3.2',
                                                    rows=2,
                                                    columns=2,
                                                    x_offset=2,
                                                    y_offset=2,
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                )
            ],
            6,
            6,
        ),
    ],
)
def test_column_size(
    data: list[Cell | Row],
    expected_rows: int,
    expected_columns: int,
) -> None:
    column = Column(data=data)

    assert column.size.rows == expected_rows
    assert column.size.columns == expected_columns
