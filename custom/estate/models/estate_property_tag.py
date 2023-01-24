from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_tag_name_unique', 'UNIQUE(name)',
         'Property tag name must be unique')
    ]
