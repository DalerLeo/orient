# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountPayment(models.Model):
    _inherit = "account.payment"

    contract_id = fields.Many2one('sale.contract', 'Contract', copy=False, check_company=True)
    sale_order_id = fields.Many2one('sale.order', 'Sale Order', copy=False, check_company=True)
