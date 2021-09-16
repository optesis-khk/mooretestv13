from odoo import models, fields, api, _

class CrossoveredBudgetReport(models.TransientModel):

    _name = 'report_crossovered_budget'
    _inherit = 'control_budget_abstract'

    date_from = fields.Date()
    date_to = fields.Date()
    company_id = fields.Many2one('res.company')
    line_ids = fields.One2many(comodel_name='report_crossovered_budget_lines', inverse_name='report_id')

  #  @api.multi
    def print_report(self, report_type):
        self.ensure_one()
        if report_type == 'xlsx':
            report_name = 'c_b.report_crossovered_budget_xlsx'
        return self.env['ir.actions.report'].search(
            [('report_name', '=', report_name),
             ('report_type', '=', report_type)],
            limit=1).report_action(self, config=False)

  #  @api.multi
    def compute_data_for_report(self,
                                with_line_details=True,
                                with_partners=True):
        self.ensure_one()

class CrossoveredBudgetLines(models.TransientModel):

    _name = 'report_crossovered_budget_lines'
    _inherit = 'control_budget_abstract'

    report_id = fields.Many2one('report_crossovered_budget',
        ondelete='cascade',
        index=True
    )

    general_budget = fields.Char()
    account_analytic = fields.Char()
    planned_amount = fields.Float()
    engage_amount = fields.Float()
    practical_amount = fields.Float()
    available_amount = fields.Float()
