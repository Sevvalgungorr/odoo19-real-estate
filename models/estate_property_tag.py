from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Gayrimenkul Etiketi"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")

    _unique_type_name=models.Constraint(
        'UNIQUE(name)',
        'gayrimenkul tipi tekdüze olmalı',
    )

