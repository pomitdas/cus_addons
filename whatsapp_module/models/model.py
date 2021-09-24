from odoo import api,fields,models, _


class WhatsappModel(models.Model):
    _name = "contact.model"
    _description="Contact model"
    _rec_name = "name"

    name=fields.Char(string="Name",required=True)
    date_of_birth=fields.Date(string="Date Of Birth")
    age=fields.Integer(string="Age")
    street=fields.Char(string="Street")
    city=fields.Char(string="City")
    zip_code=fields.Integer(string="Zip")
    Mobile=fields.Char(string="Mobile")
    state_id=fields.Many2one("res.country.state",string="State", domain="[('country_id', '=',country_id )]")
    country_id=fields.Many2one("res.country",string="Country")
    email=fields.Char(string="Email")
    pro=fields.Many2one( "res.users",string="Pro")

    def send_email_fun(self):
        template_id=self.env.ref("whatsapp_module.email_template_for").id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id,force_send=True)
        
    



