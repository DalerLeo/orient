# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"
    contract_id = fields.Many2one('sale.contract', 'Contract', copy=False, check_company=True)
    is_subcontract = fields.Boolean(default=False)
    subcontract_type = fields.Many2one('sale.subcontract.type', 'Subcontract Type', copy=False)

    def _cancel_order_from_contract(self):
        self.ensure_one()
        self.action_cancel()

    def update_existing_contracts(self):
        """
        Update contracts already linked to the order by updating or creating lines.

        :rtype: list(integer)
        :return: ids of modified contracts
        """
        res = []
        for order in self:
            if order.contract_id:
                res.append(order.contract_id)
            else:
                continue

            contract = order.contract_id

            if contract.sale_order_auto_cancel:
                sale_orders = self.env['sale.order'].search([
                    ('contract_id', '=', self.contract_id.id),
                    ('id', '!=', self.id),
                    ('state', '!=', 'cancel'),
                ])
                for sale_order in sale_orders:
                    sale_order._cancel_order_from_contract()

            subcontract_count = self.env['sale.subcontract'].search_count([
                ('contract_id', '=', contract.id),
                ('sale_order_id', '=', order.id),
            ])
            if order.is_subcontract and subcontract_count == 0:
                self.env['sale.subcontract'].create({
                    'contract_id': contract.id,
                    'sale_order_id': order.id,
                    'subcontract_type': order.subcontract_type.id,
                    'name': self.env['sale.subcontract'].search_count([('contract_id', '=', contract.id)]) + 1
                })

        return res

    def _action_confirm(self):
        """Update and/or create subscriptions on order confirmation."""
        res = super(SaleOrder, self)._action_confirm()
        self.update_existing_contracts()
        return res

    def action_confirm(self):
        if self.filtered(lambda s: not s.contract_id):
            raise UserError(_('Cannot confirm order without contract'))
        res = super(SaleOrder, self).action_confirm()
        return res

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['contract_id'] = self.contract_id
        return invoice_vals
