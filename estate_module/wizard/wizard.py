from odoo import api, fields, models, _

class DemoWizard(models.TransientModel):
    _name = "demo.wizard"
    _description = "Demo wirard"


    reason = fields.Char("Reason", required=True)

    def action_sold(self):
        self.ensure_one()
        active_model = self.env.context.get("active_model", False)
        active_id = self.env.context.get("active_id", 0)
        if active_model == "estate.model" and active_id:
            active_obj = self.env["estate.model"].browse(active_id)
            if active_obj:
                active_obj.cancel_reason = self.reason
                active_obj.state = "sold"
                # active_obj.bedrooms=2

                # active_obj.write({
                #     "cancel_reason": self.reason,
                #     "state": "canceled"
                # })

         