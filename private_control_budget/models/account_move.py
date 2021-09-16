from odoo import fields, models, api, _

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    available =  fields.Float(string='Montant budget restant',compute="_get_available", digits=0 , default="0",store=False)

   # planned =  fields.Float(string='Montant budget prevu',compute="_get_planned", digits=0 , default="0")

   # @api.multi
    @api.depends('account_id','analytic_account_id')
    def _get_available(self):
        self.available = 0
        for record in self:
            if record.account_id and record.analytic_account_id:
                for line in record.analytic_account_id.crossovered_budget_line:
                    if record.account_id in line.general_budget_id.account_ids:
                        record.available = line.available_amount
                        break

    #@api.multi
    @api.depends('account_id','analytic_account_id')
    def _get_planned(self):
        self.planned = 0
        for record in self:
            if record.account_id and record.analytic_account_id:
                for line in record.analytic_account_id.crossovered_budget_line:
                    if record.account_id.id in line.general_budget_id.account_ids.ids:
                        record.planned = line.planned_amount
                        break


    @api.onchange('credit','analytic_account_id')
    def _budget_control(self):
        if self.credit and self.analytic_account_id:
            ok = self.available - self.credit
            if ok < 0:
                message = _('Attention votre budget est insuffisant vour effectuer l\'achat')
                mess= {
                            'title': _('Budget insuffisant'),
                            'message' : message
                        }
                return {'warning': mess}
