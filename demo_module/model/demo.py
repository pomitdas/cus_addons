from odoo import api, fields, models, _
import logging
_logger =logging.getLogger(__name__)

class DemoModel(models.Model):
    _name = "demo.model"
    _description = "Demo Model"
    _rec_name = "name1"

    name1 = fields.Char(string="Name",required=True,help="hElp string")
    description = fields.Text(string="Description")
    is_boolean = fields.Boolean(string="Boolean")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    image = fields.Binary(string="Image")
    age = fields.Integer(string="Age", default=20)
    weight=fields.Integer(string="weight")
    html_field=fields.Html(string="Html Field")
    char_count =fields.Integer(compute="_computer_char_count" ,string="Char Count",store=True)
    new_gender = fields.Selection(related='gender',string="New_gender",store=True)
    state=fields.Selection( [('draft','Draft'),('pending','Pending'),('approved',"approved"),('canceled','Canceled')],string='State',default='draft')
    # html_field = fields.Html(string="Html Field")

    filter_age=fields.Integer(compute="_age_filter",string="greater the 20")



    ma_one=fields.Many2one('res.partner', string="many_2_one")

    partner_id=fields.Many2one(comodel_name="demo.new", string="customer")
    skill_ids =fields.One2many("demo.new","demo_model_ids", string="one-many")
    tag_ids=fields.Many2many("demo.new", string="Tags")

    one_many=fields.One2many("demo.new","demo_new_ids", string="one_many")



    desc=fields.Text(string="Description")
    boolean1=fields.Boolean(string="pomit")
    boolean2=fields.Boolean(string="shashwat")
    # add_name =fields.Text(compute="dess" ,string="Char Count",store=True)

    

    tab1=fields.Char("tab fields")
    tab2=fields.Char("tab2 fields")
    tab3=fields.Char("tab3 fields")
    
    @api.onchange("boolean1","boolean2")
    def dess(self):
        if self.boolean1:
            self.desc="pomit"
        else:
            self.desc="das"
        # if self.boolean2:
        #     self.dess=self.dess+"shashwat"
        


    @api.depends("age")
    def _age_filter(self):
        for i in self:
            if i.age>20:
                i.filter_age=1
            else:
                i.filter_age=0


    @api.onchange("is_boolean")
    def onchange_is_boolean(self):
        if self.is_boolean:
            self.description="description is set"
        else:
            self.description="desc not set"

    @api.depends("description")
    def _computer_char_count(self):
        _logger.info("-----------------%r-------------",self)
        for  rec in self:
            if rec.description:
                rec.char_count=len(rec.description)
            else:
                rec.char_count=0
    
    
    def action_pending(self):
        self.state="pending"

    def action_approved(self):
        self.state="approved"

    def action_canceled(self):
        self.state="canceled"

    def action_draft(self):
        self.state="draft"

    def add_button(self):
        self.env["demo.new"].create({
            "name":self.name1,
            "des":self.description,
            "phn":self.age
        })

    # def search(self):
    #     obj = self.env["demo.new"].search([])
    #     obj1 = self.env["demo.new"].search(["des",'=',self.id])
    #     _logger.info("==========%r------------",[obj])

    def update_button(self):
        ob = self.env["demo.new"].search([("id_",'=',self.id)])
        if ob:
            ob.write({
                "name":"hello",
            })
    def  unlink_skill(self):
        ob=self.env["demo.new"].search( [('id_' ,'=' , self.id)] )
        if ob:
            ob.unlink ()


class DemoNew(models.Model):
    _name="demo.new"
    _description="create new model"

    name=fields.Char("NEW name")
    des=fields.Text("des text")
    phn=fields.Integer("phn no")
    id_=fields.Integer("id_no")

    demo_model_ids = fields.Many2one("demo.model" ,string="Skkills")
    demo_new_ids=fields.Many2one('demo.model',string="new_ids")
    
    option_id=fields.Many2one('res.partner', string="m_option")
