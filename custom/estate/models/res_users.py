from odoo import models, fields


class Users(models.Model):
    _name = 'res.users'
    _inherit = ['res.users']

    property_ids = fields.One2many('estate.property', 'salesperson_id', string="Properties")