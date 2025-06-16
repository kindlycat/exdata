Usage Guide
===========

Basic Usage
-----------

Here's a simple example of how to use exdata to export data to an Excel file:

.. code-block:: python

    from exdata import XlsxExporter, Sheet, Row, Cell

    # Create a sheet with data
    sheet = Sheet(
        name="Sheet1",
        data=[
            Row(data=[
                Cell(value="Name"),
                Cell(value="Age"),
                Cell(value="City")
            ]),
            Row(data=[
                Cell(value="John"),
                Cell(value=30),
                Cell(value="New York")
            ]),
            Row(data=[
                Cell(value="Alice"),
                Cell(value=25),
                Cell(value="London")
            ])
        ]
    )

    # Create and configure the exporter
    exporter = XlsxExporter(
        sheets=[sheet],
    )

    # Export to a file
    with open("output.xlsx", "wb") as f:
        f.write(exporter.export().read())

For more advanced usage examples, including formatting cells, working with multiple sheets,
and rich text formatting, see the :doc:`advanced_usage` section.

For detailed API reference, see the :doc:`api` section. 