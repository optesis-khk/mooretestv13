# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Company(models.Model):
    _inherit = 'res.company'

    three_step_validation =  fields.Boolean(
        'Three Step Approval'
    )
    finance_validation_amount = fields.Monetary(
        'Finance Validation Amount',
        default=0.0
    )
    director_validation_amount = fields.Monetary(
        'Director Validation Amount',
        default=0.0
    )
    email_template_id = fields.Many2one(
        'mail.template',
        string='Purchase Approval Email Template',
    )
    refuse_template_id = fields.Many2one(
        'mail.template',
        string='Purchase Refuse Email Template',
    )
