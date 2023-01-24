from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")

    _sql_constraints = [
        ('check_type_name_unique', 'UNIQUE(name)',
         'Property type name must be unique')
    ]
