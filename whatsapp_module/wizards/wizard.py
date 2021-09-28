from odoo import api, fields, models, _
import requests

import logging
_logger = logging.getLogger(__name__)

class WhatsappWizard(models.TransientModel):
    _name = "whatsapp.wizard"
    _description = "whatsapp wizard"


    mob = fields.Char(related='name_id.Mobile', string='Mobile',store=True)
    # phone_no = fields.Char("Phone", required=True)
    text= fields.Text('Msg',required=True)
   
    name_id= fields.Many2one("contact.model",string='name')


    # def send_msg(self):
    def send_msg(self):
        self.ensure_one()
        active_model = self.env.context.get("active_model", False)
        active_id = self.env.context.get("active_id", 0)

        if self.text and active_id and active_model=="contact.model":
            # _logger.info("-------------------txt-------===========---%r-------------",self.text)
            text_data=self.text
            phn=self.mob
            # _logger.info("-------------------phn-------===========---%r-------------",self.mob)
            # _logger.info("-------------------phn-------===========---%r-------------",phn)


        API_KEY = "g6rzwz1gxbrrecwi"
        URL = 'https://api.chat-api.com/instance341392/sendMessage?token=' + API_KEY
        response_post = requests.post(
        URL,
        {
        "body": text_data ,
        "phone": phn,
    
        }
        )
        _logger.info("--------%r-------------",response_post)
        _logger.info("--------%r-------------",response_post.text)

    




class WhatsappMenuWizard(models.TransientModel):
    _name = "whatsapp.menu.wizard"
    _description = "whatsapp menu wizard"

    recipients =fields.Many2many("contact.model",string="Recipients",required=True)
    message=fields.Char(string="Message",required=True)
    

    def send_whatsapp_msg(self):

        # self.ensure_one()
        # active_model = self.env.context.get("active_model", False)
        # active_id = self.env.context.get("active_id", 0)
        # if active_id and active_model=="whatsapp.menu":
        #     text_data=self.message

        phn_lst=[]
        for i in self.recipients:
            phn_lst.append(i.Mobile)
        #     _logger.info("-------------------recip-------===========---%r-------------",i.Mobile)
        # _logger.info("-------------------recip-------===========---%r-------------",lst)


        
        text_data=self.message
        API_KEY = "g6rzwz1gxbrrecwi"
        URL = 'https://api.chat-api.com/instance341392/sendMessage?token=' + API_KEY
        for i in phn_lst:
            response_post = requests.post(
            URL,
            {
            "body": text_data ,
            "phone": i,
        
            }
            )

            _logger.info("--------%r-------------",response_post)
            _logger.info("--------%r-------------",response_post.text)