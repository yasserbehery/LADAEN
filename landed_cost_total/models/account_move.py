from odoo import fields, models, api


class StockValuationAdjustmentLines(models.Model):
    _inherit = 'stock.valuation.adjustment.lines'

    move_ids = fields.Many2one('stock.landed.cost')
    is_computes = fields.Boolean(string="Add origin value?")
    is_computes2 = fields.Boolean(string="Add Additional landed cost?")


class AccountMoveInherit(models.Model):
    _inherit = 'stock.landed.cost'

    totals = fields.One2many('stock.valuation.adjustment.lines', 'move_ids', string='Landed Cost Total')
    amount_total = fields.Monetary(string="Landed Cost Total")
    # custom_total = fields.Monetary(compute="compute_total")
    custom_total = fields.Monetary(compute="compute_total_new")

    # @api.depends('amount_total', 'totals.is_computes', 'custom_total')
    # def compute_total(self):
    #     for rec in self:
    #         if rec.valuation_adjustment_lines.filtered(lambda line: line.is_computes).mapped('former_cost'):
    #             rec.custom_total = sum(rec.valuation_adjustment_lines.filtered(lambda line: line.is_computes).mapped('former_cost'))
    #         else:
    #             rec.custom_total = False

    @api.onchange('amount_total', 'totals.is_computes', 'custom_total', 'totals.former_cost', 'additional_landed_cost')
    def compute_total_new(self):
        for rec in self:
            sum = 0
            sum2 = 0
            if rec.valuation_adjustment_lines:
                for line in rec.valuation_adjustment_lines:
                    if line.former_cost and line.is_computes:
                        # sum = sum + line.former_cost + line.additional_landed_cost
                        sum += line.former_cost
                    if line.additional_landed_cost and line.is_computes2:
                        sum2 += line.additional_landed_cost
            rec.custom_total = sum + sum2
