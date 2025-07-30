from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HameshaPurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    po_approval_status = fields.Selection([
        ('open', 'Open'),
        ('pending_approval_manager', 'Waiting Approval - Manager'),
        ('pending_approval_dept_head', 'Waiting Approval - Dept. Head'),
        ('pending_approval_cfo', 'Waiting Approval - CFO'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='PO Approval Status', default='open', tracking=True)

    reject_note = fields.Text('Reject Note', tracking=True)

    def btn_submit_approval(self):
        """
        Action to submit approval
        """
        amount = self.amount_total
        min = 5000000
        max = 20000000
        groups = False

        # Delegate Condition
        if amount < min:
            self.po_approval_status = 'pending_approval_manager'
            groups = 'hamesha_po_approval.group_po_manager'
        elif min <= amount <= max:
            self.po_approval_status = 'pending_approval_dept_head'
            groups = 'hamesha_po_approval.group_po_dept_head'
        else:
            self.po_approval_status = 'pending_approval_cfo'
            groups = 'hamesha_po_approval.group_po_cfo'

        group = self.env.ref(groups)
        users = group.users

        mail_template = self.env.ref('hamesha_po_approval.mail_template_po_submit')
        for user in users:
            if user.partner_id.email:
                mail_template.sudo().send_mail(
                    self.id,
                    email_values={
                        'email_to': user.partner_id.email,
                    },
                    force_send=True
                )
        

    def btn_approve(self):
        """
        Approve PO based on role
        """
        self.ensure_one()

        user = self.env.user

        if self.po_approval_status == 'pending_approval_manager':
            if not user.has_group('hamesha_po_approval.group_po_manager'):
                raise UserError("Access denied: only Managers can approve at this stage.")
            self.po_approval_status = 'approved'
            self.message_post(body="Approved by Manager (%s)" % user.name)
        elif self.po_approval_status == 'pending_approval_dept_head':
            if not user.has_group('hamesha_po_approval.group_po_dept_head'):
                raise UserError("Access denied: only Dept. Head can approve at this stage.")
            self.po_approval_status = 'pending_approval_cfo'
            self.message_post(body="Approved by Dept Head (%s), Waiting for CFO approval." % user.name)
        elif self.po_approval_status == 'pending_approval_cfo':
            if not user.has_group('hamesha_po_approval.group_po_cfo'):
                raise UserError("Access denied: only CFO can approve at this stage.")
            self.po_approval_status = 'approved'
            self.message_post(body="Approved by CFO (%s)" % user.name)
        else:
            raise UserError("Purchase Order not valid for approval")
        
    def btn_reject(self):
        """
        Reject the PO with wizard, so user can input in pop up section
        """
        return {
            'name': 'Reject PO',
            'type': 'ir.actions.act_window',
            'res_model': 'reject.po.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_rejection_reason': '', 'active_id': self.id},
        }
