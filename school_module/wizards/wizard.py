from odoo import api, fields, models, _

class FeeWizard(models.TransientModel):
    _name = "fee.wizard"
    _description = "fee wizard"
    import logging
    _logger = logging.getLogger(__name__)

    curr_payment = fields.Char("Amount Paid", required=True)
    Date = fields.Date(string="Date")

    def payment_record(self):
        self.ensure_one()
        active_model = self.env.context.get("active_model", False)
        # _logger.info("--------------------------===========---%r-------------",active_model)
        active_id = self.env.context.get("active_id", 0)
        if self.curr_payment and active_id and active_model=="school.fee":
            self.env["school.fee.line"].create({
                "school_fee_id":active_id,
                "curr_payment":self.curr_payment,
                "date_paid":self.Date
                # _logger.info("--------------------------===========---%r-------------",curr_payment)

            })
             






























    # def action_sold(self):
    #     self.ensure_one()
    #     active_model = self.env.context.get("active_model", False)
    #     active_id = self.env.context.get("active_id", 0)
    #     if active_model == "estate.model" and active_id:
    #         active_obj = self.env["estate.model"].browse(active_id)
    #         if active_obj:
    #             active_obj.cancel_reason = self.reason
    #             active_obj.state = "sold"
                # active_obj.bedrooms=2

                # active_obj.write({
                #     "cancel_reason": self.reason,
                #     "state": "canceled"
                # })

         