from odoo import models, fields

class HameshaRejectApprovalWizard(models.TransientModel):
    _name = 'reject.po.wizard'
    _description = 'Reject Purchase Order Wizard'

    rejection_reason = fields.Text('Rejection Reason', required=True)

    def action_reject(self):
        po = self.env['purchase.order'].browse(self.env.context.get('active_id'))
        po.write({
            'po_approval_status': 'rejected',
            'reject_note': self.rejection_reason,
        })
        po.message_post(body="Rejected by %s. Reason: %s" % (
            self.env.user.name, self.rejection_reason
        ))
