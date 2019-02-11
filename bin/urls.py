# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :

import file
from views import index
from views import users
from views import roles
from views import api
from views import login
from views import rate
from views import merchants
from views import push_message
from views import start_page
from views import trade
from views import tradeCode
from views import fund
from views import audit_black
from views import register_audit
from views import registerAuditDetail
from views import sms_record
from views import sms_template
from views import infoChange
from views import mpconf
from views import tag
from views import sales

from views import app_api
from views import mchnt_api
from views import official_accounts
from views import mchnt_change_log

urls = (
    # views
    ('^/$', index.Index),
    ('^/index$', index.Index),
    ('^/users$', users.Page),
    ('^/roles$', roles.Page),
    ('^/upload$', file.UploadFile),
    ('^/login$', login.Login),
    ('^/login_safe$', login.Login_safe),
    ('^/reset_pwd$', login.Reset_PWD),
    ('^/exit$', login.LoginOut),
    ('^/rate$', rate.Page),
    ('^/merchants$', merchants.Page),
    ('^/push_template$', push_message.ret2template),
    ('^/push_list$', push_message.push_list),
    ('^/start_page_list$', start_page.start_page_list),
    ('^/push_list_api$', push_message.push_list_api),
    ('^/push_act$', push_message.push_act),
    ('^/trade$', trade.Page),
    ('^/trade_code$', tradeCode.Page),
    ('^/fund', fund.Page),
    ('^/audit_black', audit_black.Page),
    ('^/register_audit$', register_audit.Page),
    ('^/register_audit_detail$', registerAuditDetail.Page),
    ('^/sms_record', sms_record.Page),
    ('^/audit_getgroups$', register_audit.GetGroups),
    ('^/sms_template', sms_template.Page),
    ('^/info_change$',infoChange.Page),
    ('^/app_rule_insert',app_api.app_rule_insert),
    ('^/app_rule_update',app_api.app_rule_update),
    ('^/app_rule_list',app_api.app_rule_list),
    ('^/app_list',app_api.app_list),
    ('^/app_excel',app_api.appExcel),
    ('^/get_app_config',app_api.get_app_config),
    ('^/app_mchnt_list',mchnt_api.mchnt_list),
    ('^/app_mchnt_history',mchnt_api.mchnt_history),
    ('^/app_mchnt_change',mchnt_api.mchnt_change),
    ('^/app_mchnt_excel',mchnt_api.tradeExcel),
    ('^/app_rule_getone',app_api.app_rule_getone),
    ('^/official_accounts_config$',official_accounts.OfficialAccountsConfig),
    ('^/get_select_data$',official_accounts.GetSelectData),
    ('^/get_city$',official_accounts.GetCity),
    ('^/get_mccs$',official_accounts.GetMcc),
    ('^/official_accounts_manage$',official_accounts.OfficialAccountsManage),
    ('^/mchnt_change_log$',mchnt_change_log.mchntchangelog),
    ('^/mchnt_change_log_list',mchnt_change_log.mchnt_change_log_list),
    ('^/sales_audit_list',sales.Sales_Audit_List),
    ('^/sales_audit',sales.Sales_Audit),
    ('^/sales_do_audit',sales.Sales_Do_Audit),
    ('^/sales_download',sales.Sales_Download),
    ('^/salesexcel',sales.SalesExcel),
    ('^/upload_ajax',sales.Upload_Ajax),
    ('^/mchnt_log_tradeExcel',mchnt_change_log.mchnt_log_tradeExcel),
    ('^/merchant_config$',official_accounts.MerchantConfig),
    ('^/get_merchant_config_data$',official_accounts.GetMerchantConfigSelectData),
    ('^/test$',official_accounts.test),
    ('^/testManage$',official_accounts.testManage),
    ('/getAppID$',official_accounts.GetAppID),
    ('/get_channel$',trade.GetData),
    ('^/set_mpconf$',mpconf.Index),
    ('^/set_mpconf_list$',mpconf.List),
    ('^/set_mpconf_manage$',mpconf.Manage),
    ('^/tag$',tag.Index),
    ('^/tag_list$',tag.List),
    ('^/tag_manage$',tag.Manage),

    # api
    ('^/api/v1/users$', api.Users),
    ('^/api/v1/roles$', api.Roles),
    ('^/api/v1/permissions$', api.Permissions),
    ('^/api/v1/p_r_map$', api.PermissionRoleMap),
    ('^/api/v1/rate$', api.Rate),
    ('^/api/v1/rate_history$', api.RateHistory),
    ('^/api/v1/merchants$', api.Merchants),
    ('^/api/v1/voucher$', api.Voucher),
    ('^/api/v1/channel$', api.Channel),
    ('^/api/v1/base_info$', api.BaseInfo),
    ('^/api/v1/Relation$', api.Relation),
    ('^/api/v1/fee_ratio$', api.FeeRatio),
    ('^/api/v1/pay_info', api.PayInfo),
    ('^/api/v1/terminal', api.Termbind),
    ('^/api/v1/qudao_info$', api.qudaoInfo),
    ('^/api/v1/idcard_relation$', api.IDRelation),
    ('^/api/v1/trade$', api.Trade),
    ('^/api/v1/trade_total$', api.tradeTotal),
    ('^/api/v1/trade_detail$', api.tradeDetail),
    ('^/api/v1/trade_excel$', api.tradeExcel),
    ('^/api/v1/qrcode$', api.QRCode),
    ('^/api/v1/fund$', api.Fund),
    ('^/api/v1/account$', api.Account),
    ('^/api/v1/audit_black', api.AuditBlack),
    ('^/api/v1/register_auditList$', api.RegisterAuditList),
    ('^/api/v1/sms_record', api.SMSRecord),
    ('^/api/v1/register_auditDetailData$', api.RegisterAuditDetail),
    ('^/api/v1/auditDetailMore$', api.auditDetailMore),
    ('^/api/v1/auditResult$', api.auditResult),
    ('^/api/v1/sms_template', api.SMSTemplate),

)
