from odoo import api, fields, models, _
import datetime
from odoo.exceptions import UserError,ValidationError

import logging
_logger = logging.getLogger(__name__)

class SchoolModel(models.Model):
    _name = "school.model"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Details of students"
    _rec_name = "stu_name"
    
    @api.model
    def _get_default_sequence(self):
        return self.env["ir.sequence"].next_by_code("student.sequence")


    name = fields.Char(string="Name", default=_get_default_sequence,readonly= True)
    stu_name=fields.Char(string="Name" ,required="True")
    date_of_birth=fields.Date(string="DOB")

    age=fields.Char(compute="_get_age",string="Age")
    active=fields.Boolean(string="Active",default=True)

    gender=fields.Selection([('male','Male'),('female',"Female")],default="male")
    image=fields.Binary(string="Image")
    email=fields.Char(string="Email")
    phone=fields.Char(string="Phone No")
    registration_number=fields.Integer(string="Registration number" ,required="True")
    date_registration=fields.Date(string="Registered Date")

    # note =fields.Text(string="Text")
    street=fields.Char(string="Address")
    city=fields.Char(string="City")
    zip_code=fields.Integer(string="Zip")
    state=fields.Selection([('new','New'),('current','Current'),('pass_out','Pass out')],default='new',string="State")
    
    state_id=fields.Many2one("res.country.state",string="State", domain="[('country_id', '=',country_id )]")
    country_id=fields.Many2one("res.country",string="Country")

    # course_id=fields.Many2one('school.course',string="Course")
    subject_ids=fields.Many2many('school.subject',string='Subject')
    course_ids=fields.Many2many('school.course', string="Course")

    # student_id=fields.Many2one("school.course",string="student_id")

    @api.onchange("country_id")
    def _onchange_country_id(self):
        _logger.info("---------_onchange_country_id--------------")
        if self.country_id:
            return {
                "domain": {"state_id": [("country_id", "=", self.country_id.id)]}
            }
        else:
            return {
                "domain": {"state_id": [("country_id", "=", False )]}
            }
    
    def change_new2_curr(self):
        self.state='current'

    def change_cur2_passout(self):
        self.state="pass_out"    

    @api.depends("date_of_birth")
    def _get_age(self):
        today_date=datetime.date.today()

        for rec in self:
            if rec.date_of_birth:
                dateofbirth=fields.Datetime.to_datetime(rec.date_of_birth).date()
                total_age= str(int((today_date - dateofbirth).days /365))
                rec.age=total_age
            else:
                rec.age=0

    def action_confirm(self):
        for rec in self:
            rec.name = self.env["ir.sequence"].next_by_code("student.sequence")

class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name= "tec_name"

    @api.model
    def _get_default_sequences(self):
        return self.env["ir.sequence"].next_by_code("teacher.sequence")


    name = fields.Char(string="Name", default=_get_default_sequences,readonly= True)
    tec_name=fields.Char(string="Teacher Name",required="True")
    date_of_birth=fields.Date(string="DOB")
    age=fields.Integer(compute="_get_age",string="Age")
    gender=fields.Selection([('male','Male'),('female',"Female")],string="Gender", default="male")
    image=fields.Binary(string="Image")
    email=fields.Char(string="Email")
    phone=fields.Char(string="Phone No",size=40)

    street=fields.Char(string="Street")
    city=fields.Char(string="City")
    state_id=fields.Many2one("res.country.state",string="State")
    country_id=fields.Many2one("res.country",string="Country") 
    zip_code=fields.Integer(string="Zip")
    active=fields.Boolean(string="Active")
    department=fields.Char(string="Department")

    # course_ids=fields.One2many('school.course','course_id',string='Course')
    # teacher_id=fields.Many2one('school.course',string="teacher_id")
    courses_id=fields.Many2many(comodel_name='school.course',relation="teacher_course_relations",column1="teacher_id",column2="course_id",string="Course")

    @api.depends("date_of_birth")
    def _get_age(self):
        today_date=datetime.date.today()
        for rec in self:
            if rec.date_of_birth:
                date_of_birth=fields.Datetime.to_datetime(rec.date_of_birth).date()
                total_age= str(int((today_date - date_of_birth).days /365))
                rec.age=total_age
            else:
                rec.age=0

class SchoolCourse(models.Model):
    _name = "school.course"
    _rec_name = "name"

    name=fields.Char(string="Course Name")
    description=fields.Char(string="Description")
    duration=fields.Char(string="Duration")
    time=fields.Selection([('day','Day'),('week','Week'),('month','Month'),('year','year')],stiring="Time")
    fee=fields.Integer(string="Fee")
    department=fields.Selection([('photography','Photography'),('software_development','Software development'),('web_development','Web Development')])
    designation=fields.Char(string="Designation")

    # course_id=fields.Many2one('school.teacher',string='Course')
    student_ids=fields.Many2many('school.model',string='Student')
    teac_id=fields.Many2many(comodel_name='school.teacher',relation="teacher_course_relations",column1="course_id",column2="teacher_id",string="Teacher")
    
class SchoolSubject(models.Model):
    _name= "school.subject"
    _rec_name="sub_name"

    sub_name=fields.Char(string='Name')
    description=fields.Char(string="Description")
    department=fields.Char(string='Department')

    subject_id=fields.Many2one("school.model",string="Sub")

class SchoolFee(models.Model):
    _name= "school.fee"
    _rec_name="student_id"

    student_id=fields.Many2one('school.model',string='Student',required="True")
    course_id=fields.Many2one('school.course',string='Course',required="True",domain="[('student_ids', '=',student_id )]")
    name=fields.Integer("Integer")

    # amount_paid=fields.Integer(related="amount_ids.amount_paid",string='Amount Paid',store="True")
    date_paid=fields.Date(string="Date paid")
    total_fee=fields.Integer(related="course_id.fee",string="Total Fee",store="True")
    amount_pai=fields.Integer(compute="sum_of_all",string="Amount Paid")
    due_fee=fields.Integer(compute="total_due",string='Due Fee')

    amount_ids=fields.One2many('school.fee.line','school_fee_id',string="Amount")

   




    
    @api.depends("amount_ids")
    def sum_of_all(self):
        sum=0
        for rec in self:       
            for i in rec.amount_ids:
                # x = i.amount_paid
                x = i.curr_payment
                sum=sum+x
            rec.amount_pai=sum
     
    @api.depends("amount_pai","total_fee")
    def total_due(self):
        for rec in self:
            rec.due_fee = rec.total_fee - rec.amount_pai

    def pop_up(self):
        return {
            'name':_(" amount"),
            'view_mode': 'form',
            'res_model': 'fee.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

class SchoolFeeLine(models.Model):
    _name= "school.fee.line"
    _rec_name="school_fee_id"

    def _get_default_payment_sequence(self):
        return self.env["ir.sequence"].next_by_code("payment.sequence")

    amount_paid = fields.Integer(string="Amount Paid")

    date_paid = fields.Date(string="Date")
    school_fee_id = fields.Many2one("school.fee",string="School fee")
    curr_payment = fields.Integer(string="Payment")
    payment_seq_id = fields.Char("Payment Id", default=_get_default_payment_sequence)
