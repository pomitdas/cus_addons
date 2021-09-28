from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError

# import logging
# _logger = logging.getLogger(__name__)


class EstateModel(models.Model):
    _name = "estate.model"
    _description = "Estate Model"
    _rec_name = "title"

    @api.model
    def _default_partner_id(self):
        # _logger.info("--------%r------", self)
        return self.env.user.partner_id.id

   
    # student=fields.Monetary(string="Student Fee",index=True)
    tags=fields.Char(string="Tags")

    title = fields.Char(string="Title",required=True,help="write title of the property")
    property_type = fields.Char(string='Property Type')
    postcode=fields.Integer(string='Postcode')
    bedrooms=fields.Integer(string='Bedrooms')
    living_area=fields.Float(string='Living Area(sqm)')
    expected_price=fields.Float(string="Expected price")
    selling_price=fields.Float(string="Selling price")

    Description=fields.Char(string="Description")
    facades=fields.Boolean(string="Facades")
    Garden=fields.Boolean(string="Garden")
    Garage=fields.Boolean(string="Garage")
    state=fields.Selection([('new','New'),('offer_received','Offer_Received'),('Offer_accepted','Offer_Accepted'),('sold','Sold')] ,string="State",default='new')

    partner=fields.Char(string="Partner")
    validity=fields.Integer(string="Validity(days)")
    deadline=fields.Date(string="Deadline")

    buyer_id=fields.Many2one('estate.new',string='Seller')
    seller_id=fields.One2many('estate.new','man_one_id' ,string='Buyer')
    
    offers_ids=fields.One2many('estate.offer','offer_id',string="OFFER")
    cancel_reason=fields.Char("Cancel reason")
   
    
    tag_ids=fields.Many2many("estate.new","estate_new_relation",column1="estate_model_id",column2="estate_new_id")


    garden_area=fields.Integer(string='Garden area')
    total_area=fields.Float(compute="sum_of_all_area",string="Total area")

    tab_description=fields.Char(string="Description")
    tab_offer=fields.Char("Offer")
    tab_other_info=fields.Char("Other_info")

    bst_price=fields.Integer(compute="max_offer",string='Best price')

    partner_id = fields.Many2one("res.partner", "Partner", required="1", default=_default_partner_id)






    @api.onchange('title')
    def practise(self):
        # obj3=self.env['estate.model'].search([])
        # _logger.info("------%r---------------------------",obj3)
        # lst=obj3.search([])
        # print(lst)
        # _logger.info("------%r-------------------------------",lst)

        if self.ids:
            # _logger.info("------%r---------------------------",self.ids)

            if self.title:
                # _logger.info("------%r---------------------------",self.title)
                self.postcode=123321
                self.PRICE=878787878787


    def action_negotiate():
        if self.ids:
            # _logger.info("------%r---------------------------",self.ids)
            if self:
                # _logger.info("------%r---------------------------",self.ids.title)
                self.postcode=988888


        # for rec in self:
        #     obj=self.search([('status','=','accepted'),('id','!=',rec.id),()])
        #     if obj:
        #          objs.write({
        #             "status":"refused"
        #         })

    def set_to_refused(self): 
        for rec in self:
            if rec.offers_ids:
                # _logger.info("-----------------------------------------------%r-------------",rec.offers_ids)
                non_refused_offers = rec.offers_ids.filtered(lambda x:x.status != "refused")
                # _logger.info("-----------------------------------------------%r-------------",non_refused_offers)
                if non_refused_offers:
                    non_refused_offers.write({
                        "status":"refused"
                    })


    # @api.depends("buy")
    # def sellvalue(self):
    #     for rec in self:
    #         rec.sp = 0
    #         for offer in rec.buy:
    #             _logger.info("=========Search==========%r---------------------",offer.offer)
    #             if offer.status == "Accepted":
    #                 rec.sp = offer.offer


    @api.depends("offers_ids")
    def max_offer(self):
        lst=[]
        for rec in self:
            for off in rec.offers_ids:
                x = off.price
                lst.append(x)
            max_price=max(lst or [9999])
            rec.bst_price=max_price
    
            # _logger.info("-----------------%r-------------",lst)
                # maximum=max(x)
                # i.PRICE=maximum
                
                

    def add_button(self):
        self.env["estate.new"].create({
            "sold_property":self.property_type,
            "sold_postcode":self.postcode
        })

    def UNlink_button(self):
        unlink_obj=self.env["estate.new"].search([("add","=" , self.title)])
        if unlink_obj:
            unlink_obj.unlink()

    
    # @api.constrains("title")
    # def _check_title(self):
    #     for i in self:
    #         objs=self.search([("title","=",i.title)])
    #         if len(objs)>=2:
    #             raise ValidationError(_("multiple value"))

    @api.constrains("title","property_type")
    def _check_title_property_type(self):
        for i in self:
            obj=self.search([("property_type",'=',i.property_type),("title",'=',i.title)])
            # obj1=self.search([("title",'=',i.title)])
            # z=obj + obj1
            if len(obj)>=2:
                raise ValidationError(_("multiple value"))

    


    @api.depends("garden_area")
    def sum_of_all_area(self):
        for i in self:
            i.total_area=i.garden_area + i.living_area
    
    @api.onchange('Garden')
    def onchange_garden_area(self):
        if self.Garden==False:
            self.garden_area=0
        

    def state_new(self):
        self.state="new"
    def state_offer_received(self):
        self.state="offer_received"
    def state_Offer_accepted(self):
        self.state="Offer_accepted"
    # def state_sold(self):
    #     self.state="sold"




    def state_sold(self):
        return {
            'name':_("Why you want to sell"),
            'view_mode': 'form',
            # 'view_id': self.env.ref("demo_module.demo_wizard_form_view").id,
            'res_model': 'demo.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.model
    def create(self, vals):
        # _logger.info("------------------create-------%r----%r---", self, vals)
        if not vals.get("Description", False):
            vals.update({"Description": "Testing....."})
        return super(EstateModel, self).create(vals)
        

    class EstateNewModel(models.Model):
        _name="estate.new"
        _rec_name="sold_property"

        sold_property=fields.Char(string='Sold Property')
        sold_postcode= fields.Char(string='Postcode',required=True)

        man_one_id=fields.Many2one('estate.model',string="Many_1")

        

    class EstatePropertyOffer(models.Model):
        _name="estate.offer"
        _rec_name="price"

        property_type=fields.Char(string='Property Type')
        price =fields.Integer(string='Price')
        status=fields.Selection([('accepted','Accepted'),('refused','Refused')])
        check=fields.Char(string='Check')
        offer_id=fields.Many2one('estate.model',string='Offer')

        @api.constrains("status")
        def one_time_accept(self):
            for rec in self:
                obj=self.search([("status",'=',"accepted"),('id','!=',rec.id),("offer_id.id",'=',rec.offer_id.id)])
                if obj and rec.status=="accepted":
                    raise ValidationError(_("multiple accept not allow"))

        def change_on_click(self):
            for rec in self:
                objs=self.search([("status","=","accepted"),('id','!=',rec.id),("offer_id.id",'=',rec.offer_id.id)])
                if objs:
                    objs.write({
                    "status":"refused"
                })
                rec.status="accepted"

        # class About_property(models.Model):
        #     _name="about.estate"
        #     _rec_name=""


        











        # def change_on_click(self):
        #     for rec in self:
        #         obj=self.search([('id','!=',rec.id),('offer_id.id','=',rec.offer_id.id)])
        #         if obj.status="accepted"
        #             pass
        #         else:
        #             obj.write({
        #                 "status":"refused"
        #             })






    

        