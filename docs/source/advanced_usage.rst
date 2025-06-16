Advanced Usage
==============

Buffer Usage
~~~~~~~~~~~~

By default, XlsxExporter uses BytesIO buffer to store the Excel data in memory. This is convenient for most use cases,
but if you're working with large files or want to optimize memory usage, you can use file-based buffers instead.

The XlsxExporter accepts different types of buffers for writing the Excel data:

.. code-block:: python

    from exdata import XlsxExporter, Sheet, Row, Cell
    from pathlib import Path
    import io

    # Create a simple sheet for examples
    sheet = Sheet(
        name="Sheet1",
        data=[
            Row(data=[
                Cell(value="Data"),
                Cell(value="Value")
            ])
        ]
    )

    # 1. Using a file path (string) - recommended for large files
    exporter = XlsxExporter(
        sheets=[sheet],
        buffer="output.xlsx",
        workbook_options={'in_memory': False}
    )
    exporter.export()

    # 2. Using a Path object - recommended for large files
    exporter = XlsxExporter(
        sheets=[sheet],
        buffer=Path("output.xlsx"),
        workbook_options={'in_memory': False}
    )
    exporter.export()

    # 3. Using a BytesIO buffer - default behavior
    buffer = io.BytesIO()
    exporter = XlsxExporter(
        sheets=[sheet],
        buffer=buffer
    )
    buffer = exporter.export()
    # Now you can use the buffer, for example:
    with open("output.xlsx", "wb") as f:
        f.write(buffer.read())

    # 4. Using a file object - recommended for large files
    with open("output.xlsx", "wb") as f:
        exporter = XlsxExporter(
            sheets=[sheet],
            buffer=f,
            workbook_options={'in_memory': False}
        )
        exporter.export()

Formatting Cells
~~~~~~~~~~~~~~~~

You can format cells using the built-in formatting options:

.. code-block:: python

    from exdata import XlsxExporter, Sheet, Row, Cell, Format

    # Define formats
    formats = {
        "header": {
            "bold": True,
            "bg_color": "#CCCCCC",
            "align": "center"
        }
    }

    # Create a sheet with formatted data
    sheet = Sheet(
        name="Sheet1",
        data=[
            Row(data=[
                Cell(value="Name", format="header"),
                Cell(value="Age", format="header"),
                Cell(value="City", format="header")
            ]),
            Row(data=[
                Cell(value="John"),
                Cell(value=30),
                Cell(value="New York")
            ])
        ]
    )

    # Create and configure the exporter with formats
    exporter = XlsxExporter(
        sheets=[sheet],
        formats=formats,
        workbook_options={'in_memory': True}
    )

    # Export to a file
    with open("formatted.xlsx", "wb") as f:
        f.write(exporter.export().read())

Multiple Sheets
~~~~~~~~~~~~~~~

You can work with multiple sheets in the same workbook:

.. code-block:: python

    from exdata import XlsxExporter, Sheet, Row, Cell

    # Create first sheet
    sheet1 = Sheet(
        name="Data1",
        data=[
            Row(data=[
                Cell(value="Data 1"),
                Cell(value="Value 1")
            ]),
            Row(data=[
                Cell(value="A"),
                Cell(value=100)
            ]),
            Row(data=[
                Cell(value="B"),
                Cell(value=200)
            ])
        ]
    )

    # Create second sheet
    sheet2 = Sheet(
        name="Data2",
        data=[
            Row(data=[
                Cell(value="Data 2"),
                Cell(value="Value 2")
            ]),
            Row(data=[
                Cell(value="X"),
                Cell(value=300)
            ]),
            Row(data=[
                Cell(value="Y"),
                Cell(value=400)
            ])
        ]
    )

    # Create and configure the exporter with multiple sheets
    exporter = XlsxExporter(
        sheets=[sheet1, sheet2],
        workbook_options={'in_memory': True}
    )

    # Export to a file
    with open("multi_sheet.xlsx", "wb") as f:
        f.write(exporter.export().read())

Rich Text Formatting
~~~~~~~~~~~~~~~~~~~~

You can use rich text formatting for more complex cell content:

.. code-block:: python

    from exdata import XlsxExporter, Sheet, Row, Cell, Format, RichValue

    # Define formats
    formats = {
        "bold": {"bold": True},
        "red": {"color": "red"}
    }

    # Create a sheet with rich text
    sheet = Sheet(
        name="Rich Text",
        data=[
            Row(data=[
                Cell(value=RichValue([
                    "This is ",
                    Format("bold"),
                    "bold",
                    " and this is ",
                    Format("red"),
                    "red"
                ]))
            ])
        ]
    )

    # Create and configure the exporter
    exporter = XlsxExporter(
        sheets=[sheet],
        formats=formats,
        workbook_options={'in_memory': True}
    )

    # Export to a file
    with open("rich_text.xlsx", "wb") as f:
        f.write(exporter.export().read())

Working with Rows and Columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Rows and columns can be customized with various properties like offsets, heights, and expansion behavior:

.. code-block:: python

    from exdata import XlsxExporter, Sheet, Row, Column, Cell

    # Create a sheet with customized rows and columns
    sheet = Sheet(
        name="Custom Layout",
        data=[
            # Row with custom height and offset
            Row(
                data=[
                    Cell(value="Header 1"),
                    Cell(value="Header 2")
                ],
                heights=[30],  # Set row height to 30
                y_offset=1,    # Start from second row
                x_offset=1     # Start from second column
            ),
            # Column with custom width and offset
            Column(
                data=[
                    Cell(value="Data 1", columns=2),  # Cell spans 2 columns
                    Cell(value="Data 2")
                ],
                x_offset=2,    # Start from third column
                y_offset=2     # Start from third row
            ),
            # Row with expandable cells
            Row(
                data=[
                    Cell(value="Expanding", expand=True),  # Cell will expand
                    Cell(value="Fixed", expand=False)      # Cell won't expand
                ],
                expand=True  # Row will expand to fill available space
            )
        ]
    )

    # Create and configure the exporter
    exporter = XlsxExporter(sheets=[sheet])

    # Export to a file
    with open("custom_layout.xlsx", "wb") as f:
        f.write(exporter.export().read())

Nested Structures
~~~~~~~~~~~~~~~~~

You can create complex layouts by nesting rows and columns:

.. code-block:: python

    from exdata import XlsxExporter, Sheet, Row, Column, Cell

    # Create a complex nested structure
    sheet = Sheet(
        name="Nested Layout",
        data=[
            # Main row with nested column
            Row(
                data=[
                    Cell(value="Main Header"),
                    # Nested column
                    Column(
                        data=[
                            Cell(value="Sub Header 1"),
                            Cell(value="Sub Data 1")
                        ],
                        x_offset=1
                    )
                ]
            ),
            # Row with nested row
            Row(
                data=[
                    Cell(value="Section"),
                    # Nested row
                    Row(
                        data=[
                            Cell(value="Nested 1"),
                            Cell(value="Nested 2")
                        ],
                        x_offset=1
                    )
                ]
            )
        ]
    )

    # Create and configure the exporter
    exporter = XlsxExporter(sheets=[sheet])

    # Export to a file
    with open("nested_layout.xlsx", "wb") as f:
        f.write(exporter.export().read())

Size and Offset Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~

Here's a detailed example of using size and offset properties:

.. code-block:: python

    from exdata import XlsxExporter, Sheet, Row, Cell, Size

    # Create a sheet demonstrating size and offset properties
    sheet = Sheet(
        name="Size and Offset",
        data=[
            # Row with cells of different sizes
            Row(
                data=[
                    Cell(
                        value="Large Cell",
                        rows=2,      # Spans 2 rows
                        columns=2,   # Spans 2 columns
                        x_offset=1,  # Starts at column 2
                        y_offset=1   # Starts at row 2
                    ),
                    Cell(
                        value="Small Cell",
                        rows=1,
                        columns=1,
                        x_offset=3,  # Starts at column 4
                        y_offset=1   # Starts at row 2
                    )
                ],
                heights=[20, 30]  # Different heights for each row
            ),
        ]
    )

    # Create and configure the exporter
    exporter = XlsxExporter(sheets=[sheet])

    # Export to a file
    with open("size_offset.xlsx", "wb") as f:
        f.write(exporter.export().read())

Expansion Behavior
~~~~~~~~~~~~~~~~~~

The `expand` property controls how elements grow to fill available space. It can be set on rows, columns, and cells:

- When `expand=True` (default) on a row/column, it will grow to fill the available space in its parent container
- When `expand=True` (default) on a cell, it will grow to fill the available space in its parent row/column
- When `expand=False`, the element maintains its specified size

Here's an example demonstrating different expansion behaviors:

.. code-block:: python

    from exdata import XlsxExporter, Sheet, Row, Column, Cell

    sheet = Sheet(
        name="Expansion Example",
        data=[
            # Row with first cell expansion
            Row(
                data=[
                    # This cell will expand to fill available space
                    Cell(value="Expanded Cell"),  # expand=True by default
                    Column([
                        Cell(value="Column Cell 1"),
                        Cell(value="Column Cell 2"),
                    ]),
                    Cell(value="Fixed Cell", expand=False)
                ]
                # expand=True by default
            ),
            # Column with first cell expansion
            Column(
                data=[
                    # These cells will maintain their size
                    Cell(value="Expanded Cell", expand=False),
                    Row([
                        Cell(value="Row Cell 1"),
                        Cell(value="Row Cell 2"),
                    ]),
                    # This cell will expand to fill available space
                    Cell(value="Fixed Cell"), # expand=True by default
                ]
                # expand=True by default
            ),
        ]
    )

    # Create and configure the exporter
    exporter = XlsxExporter(sheets=[sheet])

    # Export to a file
    with open("expansion.xlsx", "wb") as f:
        f.write(exporter.export().read())
