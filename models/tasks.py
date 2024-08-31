from odoo import models, fields, api
from datetime import datetime
class Task(models.Model):

    _name = 'todo.task'
    _description = 'To-Do Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    task_name = fields.Char(tracking=1)
    assign_to = fields.Many2one('res.partner', string='Assign To', tracking=1)
    description = fields.Text(tracking=1)
    due_date = fields.Datetime(tracking=1)
    task_name_repeat = fields.Char(string="Repeated Task Name", compute="_compute_task_name_repeat", store=True)
    status = fields.Selection([
        ('new', 'New'),
        ('progress', 'IN Progress'),
        ('completed', 'Completed'),
    ])

    @api.depends('status', 'task_name')
    def _compute_task_name_repeat(self):
        for record in self:
            if record.status == 'completed':
                record.task_name_repeat = record.task_name
            else:
                record.task_name_repeat = False


    def due_date_greater(self):
        if self.due_date and self.due_date < datetime.now():
            return{
                'warning': {'title' : 'warning', 'message': "The Task Can't be in the past"}
            }

    def new_action(self):
        for rec in self:
            rec.status = 'new'

    def progress_action(self):
        for rec in self:
            rec.write(
                {'status': 'progress'}
            )

    def completed_action(self):
        for rec in self:
            rec.status = 'completed'