from odoo import models,fields
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):

    _name="estate.property.offer"
    _description="Gayrimenkul Teklif Tablosu"

    price=fields.Float()
    partner_id=fields.Many2one("res.partner",required=True)
    property_id=fields.Many2one("estate.property",required=True)
    status=fields.Selection(
    selection=[('accepted','kabul edildi'),('refused','reddedildi')]
    )
    def accept_offer(self):
        for record in self:
            if record.property_id.state=='offer_accepted':
                raise UserError("bu gayrimenkulün zaten kabul edilmiş bir teklifi var")
            record.status='accepted'
            record.property_id.write({
               "buyer_id":record.partner_id.id,
               "selling_price":record.price,
               "state":"offer_accepted",
            })

    def refuse_offer(self):
        for record in self:
            if record.status=='accepted':
                raise UserError("kabul edilmiş teklifler reddedilemez")
            else:
                 record.status='refused'

    _check_offer_price=models.Constraint(
        'CHECK(price>0)',
        'teklifler 0 dan büyük olmalı',
    )