from odoo import api, fields, models, _

class WhatsappWizard(models.TransientModel):
    _name = "whatsapp.wizard"
    _description = "whatsapp wizard"

    import logging
    _logger = logging.getLogger(__name__)

    phone_no = fields.Char("Phone", required=True)
    text=fields.Text('Msg')


    def send_msg(self):
        pass

    

