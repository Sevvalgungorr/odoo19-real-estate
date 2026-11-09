from odoo import models, fields, api
from odoo.exceptions import UserError,ValidationError
from odoo.tools import float_compare,float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Gayrimenkul Tablosu"

    name = fields.Char(required = True)
    description = fields.Text()
    date_availability = fields.Date(string="Availability Date")
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    has_garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area")
    property_type_id=fields.Many2one("estate.property.type",string="Gayrimenkul Tipi")
    buyer_id=fields.Many2one("res.partner")
    sales_person_id= fields.Many2one("res.users")
    offer_ids=fields.One2many("estate.property.offer","property_id")
    best_price=fields.Float(compute="_compute_best_price",string="En İyi Teklif")
    tag_ids=fields.Many2many("estate.property.tag")
    state=fields.Selection(
       selection=[('new','yeni'),('offer_received','teklif alındı'),('offer_accepted','teklif kabul edildi'),('sold','satıldı'),('cancelled','iptal edildi'),

       ],default='new',required=True)


    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price=max(record.offer_ids.mapped("price"))
            else:
                record.best_price=0.0

    def sell_property(self):
        for record in self:
           
                if record.state=="cancelled":
                    raise UserError("iptal edilmiş gayrimenkuller satılamaz")
                else:
                    record.state='sold'
    def cancel_property(self):
        for record in self:
           
                if record.state=="sold":
                    raise UserError("satılmıs gayrimenkuller iptal edilemez")
                else:
                    record.state='cancelled'  

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'Beklenen fiyat 0 dan büyük olmalı.',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Satış fiyatı 0 dan büyük veya eşit olmalı.',
    )           
    #satıs fiyatı beklenen fiyatın yüzde 90 ındn asağı olamaz 
    #satıs fiyatyı 0 olmamalı bu kuralın çalışması için 
    @api.constrains("expected_price","selling_price")
    def _check_valid_selling_price(self):
        for record in self:
            if (float_compare(record.selling_price,0.9*record.expected_price,precision_digits=2)<0 and
            not float_is_zero(record.selling_price,precision_digits=2)):
                raise ValidationError("satıs fiyatı beklenen fiyatın yüzde 90 ından az olamaz")


