from datetime import datetime, timedelta

from dateutil.utils import today

from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', index=True, required=True)
    property_id = fields.Many2one('estate.property', string='Property', index=True, required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date is None:
                create_date = fields.Date().today()
            else:
                create_date = fields.Date().to_date(record.create_date)

            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.create_date is None:
                create_date = fields.Date().today()
            else:
                create_date = fields.Date().to_date(record.create_date)

            record.validity = (record.date_deadline - create_date).days
