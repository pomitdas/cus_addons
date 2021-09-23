from odoo import api, fields, models, _

class estateModel_2(models.Model):
    _inherit = "estate.model"


    first_name = fields.Char(string="First Name")

