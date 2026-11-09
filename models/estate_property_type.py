from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Gayrimenkul Tipi Tablosu"

    name = fields.Char()
    property_ids=fields.One2many("estate.property","property_type_id")

    _unique_type_name=models.Constraint(
        'UNIQUE(name)',
        'gayrimenkul tipi tekdüze olmalı',
    )