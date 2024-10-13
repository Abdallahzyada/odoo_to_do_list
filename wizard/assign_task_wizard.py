from odoo import fields, models

class AssignTask(models.TransientModel):
    _name = 'assign.task'

    task_id = fields.Many2many('todo.task')
    assign_to_id = fields.Many2one('res.partner', string='Assign To', tracking=1)

    def check_action(self):
        if self.task_id.status != 'new':
            return {
                'warning': {'title': 'warning', 'message': 'The Status must be new'}
            }