from dateutil.relativedelta import relativedelta
from dateutil.utils import today

from odoo import fields, models, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Estate Property Type")
    buyer_id = fields.Many2one('res.partner', string='Buyer', index=True, copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=today() + relativedelta(months=+3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute="_compute_best_price")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )
    active = fields.Boolean(default=True)
    total_area = fields.Integer(compute="_compute_total_area")
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offerReceived', 'Offer Received'),
            ('offerAccepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        copy=False,
        default='new'
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_set_sold_property(self):
        for record in self:
            if record.state != "canceled":
                record.state = "sold"
            else:
                raise UserError("Canceled properties cannot be sold.")

    def action_cancel_property(self):
        for record in self:
            if record.state != "sold":
                record.state = "canceled"
            else:
                raise UserError("Sold properties cannot be canceled.")
