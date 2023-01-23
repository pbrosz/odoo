from datetime import datetime, timedelta

from dateutil.utils import today

from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', index=True, required=True)
    property_id = fields.Many2one('estate.property', string='Property', index=True, required=True)
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
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
