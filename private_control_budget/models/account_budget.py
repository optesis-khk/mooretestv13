from odoo import api, fields, models, _
from odoo.tools import ustr
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class CrossoveredBudget(models.Model):
    _inherit = "crossovered.budget"

    #line_ids = fields.One2many('account.budget.line', 'budget_id', string="Account Budget Lines")
  #  @api.multi
    def button_export_xlsx(self):
        self.ensure_one()
        report_type = 'xlsx'
        return self._export(report_type)

    def _export(self, report_type):
        """Default export is PDF."""
        model = self.env['report_crossovered_budget']
        report = model.create(self._prepare_report_crossovered_budget())
        report.compute_data_for_report()
        return report.print_report(report_type)

    def _prepare_report_crossovered_budget(self):
        self.ensure_one()
        lines = []
        for line in self.crossovered_budget_line:
            lines.append((0, 0, {
                                    'general_budget': line.general_budget_id.name,
                                    'account_analytic': line.analytic_account_id.name,
                                    'planned_amount': line.planned_amount,
                                    'engage_amount': line.engage_amount,
                                    'practical_amount': line.practical_amount,
                                    'available_amount': line.available_amount

                                }))
        _logger.info(lines)
        return {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'company_id': self.company_id.id,
            'line_ids': lines,
        }

class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    engage_amount = fields.Float(compute='_compute_engage_amount', string='Montant Engage', digits=0, store = False)
    available_amount = fields.Float(compute='_compute_available_amount', string='Montant Disponible', digits=0)

  #  @api.multi
    
    def _compute_engage_amount(self):
        #self.ensure_one()
        for line in self:
            result = 0.0
            id_order = 0
            acc_ids = line.general_budget_id.account_ids.ids
           
            if not acc_ids:
                raise UserError(_("The Budget '%s' has no accounts!") % ustr(line.general_budget_id.name))
            date_to = line.date_to
            date_from = line.date_from
            if line.analytic_account_id.id:
                self.env.cr.execute("""
                    SELECT SUM(price_subtotal)
                    FROM purchase_order_line
                    WHERE account_analytic_id=%s
                        AND (date_planned between %s AND %s)
                        AND account_id=ANY(%s) AND (state='purchase' OR state='done')""",
                (line.analytic_account_id.id, date_from, date_to, acc_ids,))
                result = self.env.cr.fetchone()[0] or 0.0
            line.engage_amount = result
          

    #@api.multi
    def _compute_available_amount(self):
        for line in self:
            if line.practical_amount > 0:
                if line.engage_amount >= line.practical_amount:
                    line.available_amount = line.planned_amount - line.engage_amount
                else:
                    line.available_amount = line.planned_amount - line.practical_amount
            else:
                if line.engage_amount >= -line.practical_amount:
                    line.available_amount = line.planned_amount - line.engage_amount
                else:
                    line.available_amount = line.planned_amount + line.practical_amount

class AccountBudgetLine(models.Model):
    _name = 'account.budget.line'
    _description = 'Budget Line'
    _order = 'date desc, id desc'

    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)

    name = fields.Char('Description', required=True)
    date = fields.Date('Date', required=True, index=True, default=fields.Date.context_today)
    unit_amount = fields.Float('Quantite', default=0.0)
    general_budget_id = fields.Many2one('account.budget.post', 'Poste budgétaire')
    account_id = fields.Many2one('account.analytic.account', 'Analytic Account', required=True, ondelete='restrict', index=True)
    user_id = fields.Many2one('res.users', string='User', default=_default_user)
    tag_ids = fields.Many2many('account.analytic.tag', string='Tags', copy=True)
    company_id = fields.Many2one(related='account_id.company_id', string='Company', store=True, readonly=True)
    amount = fields.Monetary(currency_field='company_currency_id', string="Montant Engage")
    planned_amount = fields.Float(string='Montant Prevu', digits=0)
    available_amount = fields.Float(string='Montant Disponible', digits=0)
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    product_id = fields.Many2one('product.product', string='Product')
    general_account_id = fields.Many2one('account.account', string='Financial Account', readonly=True)
    move_id = fields.Many2one('purchase.order.line', string='Move Line', ondelete='cascade', index=True)
    code = fields.Char(size=8)
    ref = fields.Char(string='Ref.')
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True,
        help='Utility field to express amount currency')
    partner_id = fields.Many2one('res.partner', string='Fournisseur', store=True, readonly=True)
