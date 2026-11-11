{
    "name": "Cleanmart Document Format",
    "summary": "Informe «Factura con recibo». Añade el sello ISO 14001 en la cabecera de las facturas de Cleanmart y oculta la comunicación de pago",
    "version": "19.0.1.0.0",
    "category": "Accounting",
    "author": "Xtendoo",
    "license": "LGPL-3",
    "depends": ["account", "web"],
    "data": [
        "views/report_invoice_document.xml",
        "views/report_invoice_receipt.xml",
    ],
    "installable": True,
    "application": False,
}
