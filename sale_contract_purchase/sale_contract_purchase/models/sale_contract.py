# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _


class SaleContract(models.Model):
    _inherit = "sale.contract"

    purchase_order_line_ids = fields.One2many('purchase.order.line', string='Purchase Order Lines', copy=False,
                                              compute='_compute_purchase_order_lines')

    purchase_order_ids = fields.One2many('purchase.order', 'contract_id', string='Purchase Orders')

    contract_purchase_total = fields.Float(compute='_compute_purchase_order_lines', string="Contract Purchase Total", digits='Account')
    contract_purchase_tax_total = fields.Float(compute='_compute_contract_purchase_tax_total', string="Contract Purchase Taxes", digits='Account')

    purchase_order_count = fields.Integer(compute='_compute_purchase_order_count', readonly=True)

    def _compute_purchase_order_count(self):
        for contract in self:
            contract.purchase_order_count = len(contract.purchase_order_ids)

    def _compute_purchase_order_lines(self):
        for contract in self:
            order_lines = contract.purchase_order_ids.filtered(
                lambda order: order.state in ('purchase', 'done')
            ).mapped('order_line')

            if order_lines:
                contract.purchase_order_line_ids = [(4, line.id) for line in order_lines]
            else:
                contract.purchase_order_line_ids = False

    def _compute_contract_purchase_total(self):
        for account in self:
            account.contract_total = sum(line.price_total for line in account.purchase_order_line_ids)

    def _compute_contract_purchase_tax_total(self):
        for account in self:
            account.contract_tax_total = sum(line.price_tax for line in account.purchase_order_line_ids)
