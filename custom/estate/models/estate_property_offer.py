from datetime import datetime, timedelta

from dateutil.utils import today

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', index=True, required=True)
    property_id = fields.Many2one('estate.property', string='Property', index=True, required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'Offer price must be strictly positive')
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            date_created = fields.Date().today()

            if record.create_date:
                date_created = fields.Date().to_date(record.create_date)

            record.date_deadline = date_created + timedelta(days=record.validity)

    @api.model
    def create(self, vals):
        property_load = self.env['estate.property'].browse(vals['property_id'])

        if property_load.best_price > vals['price']:
            raise ValidationError("Offer cannot be lower than best offer.")

        property_load.state = "offer_received"

        return super().create(vals)

    def _inverse_deadline(self):
        for record in self:
            date_created = fields.Date().today()

            if record.create_date:
                date_created = fields.Date().to_date(record.create_date)

            record.validity = (record.date_deadline - date_created).days

    def action_accept(self):
        for record in self:
            if any(status == "accepted" for status in record.property_id.offer_ids.mapped("status")):
                raise UserError("Only one offer can be accepted.")

            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
