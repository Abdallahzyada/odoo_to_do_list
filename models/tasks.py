from odoo import models, fields, api
from datetime import datetime

from odoo.exceptions import ValidationError


class Task(models.Model):

    _name = 'todo.task'
    _description = 'To-Do Task'
    _rec_name = 'task_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(default="New Task", readonly=1)
    task_name = fields.Char('Task Name',tracking=1)
    assign_to_id = fields.Many2one('res.partner', string='Assign To', tracking=1)
    description = fields.Text(tracking=1)
    due_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    estimated_time = fields.Integer()
    task_name_repeat = fields.Char(string="Repeated Task Name", compute="_compute_task_name_repeat", store=True)
    status = fields.Selection([
        ('new', 'New'),
        ('progress', 'IN Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ])

    line_ids = fields.One2many('task.line', 'task_id')
    total_time = fields.Integer(compute='_compute_total_time')
    active = fields.Boolean(default=True)

    @api.depends('line_ids', 'estimated_time', 'line_ids.time')
    def _compute_total_time(self):
        for rec in self:
            if rec.line_ids:
                for line in rec.line_ids:
                    rec.total_time += line.time
                    if rec.total_time > rec.estimated_time:
                        raise ValidationError('Too Much Time!')
            else:
                rec.total_time = rec.total_time

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

    def action_new(self):
        for rec in self:
            rec.status = 'new'

    def action_progress(self):
        for rec in self:
            rec.write(
                {'status': 'progress'}
            )

    def action_competed(self):
        for rec in self:
            rec.status = 'completed'

    def action_closed(self):
        for rec in self:
            rec.status = 'closed'


    def check_due_date_late(self):
        tasks_ids = self.search([])
        for rec in tasks_ids:
            if rec.due_date and rec.due_date < fields.date.today():
                if rec.status != 'closed' and rec.status != 'completed':
                    rec.is_late = True


    @api.model
    def create(self, val_list):
        res = super(Task, self).create(val_list)
        if res.ref == 'New Task':
            res.ref = self.env['ir.sequence'].next_by_code('task_seq')
        return res


class TaskLine(models.Model):
    _name = 'task.line'

    date = fields.Date()
    task_id = fields.Many2one('todo.task')
    description = fields.Text()
    time = fields.Integer()

