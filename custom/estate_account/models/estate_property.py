from odoo import fields, models, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold_property(self):
        self.env['account.move'].create({
            'move_type': 'out_invoice',
            "partner_id": self.buyer_id.id,
            "line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": self.best_price * 0.06
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100
                })
            ]
        })

        return super().action_set_sold_property()

