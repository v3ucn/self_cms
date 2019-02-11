# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :
import logging
import time
from qfcommon.web import core
from qfcommon.web import template
from tools import checkIsLogin
import config
from qfcommon.base.dbpool import with_database
import json

log = logging.getLogger()

class OfficialAccountsConfig(core.Handler):
    @checkIsLogin
    def GET(self):
        uname = self.get_cookie('uname')
        data = {}
        data['uname'] = uname
        data['chnlcode_config'] = config.CHNLCODE_CONFIG
        self.write(template.render('OfficialAccountsConfig.html', data=data))


class GetSelectData(core.Handler):
    @checkIsLogin
    @with_database(['wxmp_customer','qf_mis','qf_qudao'])
    def POST(self):
        try:
            datas = {}
            # 微信名称和appID
            where = {'status' : 1}
            if getattr(config, 'WX_MANAGE_APPIDS', None) is not None:
                where['appid'] = ('in', config.WX_MANAGE_APPIDS)
            mp_conf = self.db['wxmp_customer'].select(
                table='mp_conf', fields=['appid', 'nick_name'],
                where=where
            )
            datas['id_names'] = mp_conf

            # datas['id_names'] = results_mp_conf
            # 全部的省份信息
            results_area_p = self.db['qf_mis'].select(table='tools_area',fields=['id','area_name'])
            datas['provinces'] = results_area_p
            pro_nameArr = []
            pro_idArr = []
            for result in results_area_p:
                pro_idArr.append(result.get('id'))
                pro_nameArr.append(result.get('area_name'))
            id_pro = dict(zip(pro_nameArr,pro_idArr))
            datas['id_pro'] = id_pro
            # mcc一级
            results_mcc_a = self.db['qf_mis'].select(table='tools_mcca', fields=['id', 'mcca_name'])
            datas['mcca'] = results_mcc_a
            mcca_idArr = []
            mcca_nameArr = []
            for result in results_mcc_a:
                mcca_idArr.append(result.get('id'))
                mcca_nameArr.append(result.get('mcca_name'))
            # 封装成ID为key name为value的字典格式
            id_mcca = dict(zip(mcca_idArr, mcca_nameArr))
            datas['id_mcca'] = id_mcca
            # 渠道信息
            result_groupids = self.db['qf_qudao'].select(table='qd_profile',fields=['qd_uid','name'])
            old = self.db['qf_mis'].select(table='channel_crm',fields=['channelid','channelname'])
            for xy in old:
                result_groupids.append({'qd_uid':xy['channelid'],'name':xy['channelname']})
            datas['groupids'] = result_groupids
            group_idArr = []
            group_nameArr = []
            for result in result_groupids:
                group_idArr.append(result.get('qd_uid'))
                group_nameArr.append(result.get('name'))
            groupid_names = dict(zip(group_idArr, group_nameArr))
            datas['groupid_names'] = groupid_names
            # mcc二级
            result_mccs = self.db['qf_mis'].select(table='tools_mcc', fields=['id','mcc_name'])
            mcc_idArr = []
            mcc_nameArr = []
            for result in result_mccs:
                mcc_idArr.append(result.get('id'))
                mcc_nameArr.append(result.get('mcc_name'))
            # 封装成ID为key name为value的字典格式
            id_mcc = dict(zip(mcc_idArr,mcc_nameArr))
            datas['id_mcc'] = id_mcc

            results_city_num = self.db['qf_mis'].select(table='tools_areacity', fields=['area_id', 'count(area_id) as total'],
                                                      other='group by area_id')
            pro_totalArr = []
            pro_arr = []
            for data in results_city_num:
                pro_totalArr.append(data.get('total'))
                pro_arr.append(data.get('area_id'))
            pro_total = dict(zip(pro_arr,pro_totalArr))
            # 每个省份id和这个id下的城市数量的关系字典
            datas['pro_total'] = pro_total

            results_mcc_num = self.db['qf_mis'].select(table='tools_mcc', fields=['mcca_id', 'count(*) as total'],
                                                   other='group by mcca_id')
            total_arr = []
            mcca_arr = []
            for data in results_mcc_num:
                total_arr.append(data.get('total'))
                mcca_arr.append(data.get('mcca_id'))
            mcca_total = dict(zip(mcca_arr,total_arr))
            # 每个一级行业id和该行业下的二级行业的数量的关系字典
            datas['mcca_total'] = mcca_total

        except:
            return json.dumps({'code':0,'msg':'数据获取失败，请刷新重试！','data':{}})
        return json.dumps({'code':200,'msg':'success','data':datas})


class GetCity(core.Handler):
    @checkIsLogin
    @with_database(['qf_mis'])
    def POST(self):
        params = self.req.input()
        area_no = params.get('area_no')
        datas = {}
        try:
            results_area_c = self.db['qf_mis'].select(table='tools_areacity', fields=['city_name', 'area_id'], where={'area_id':area_no})
            datas['citys'] = results_area_c
        except:
            return json.dumps({'code':0,'msg':'fail','data':{}})
        return json.dumps({'code':200,'msg':'success','data':datas})


class GetMcc(core.Handler):
    @checkIsLogin
    @with_database(['qf_mis'])
    def POST(self):
        params = self.req.input()
        mcca_id = params.get('mcca_id')
        datas = {}
        try:
            results_mcc = self.db['qf_mis'].select(table='tools_mcc',fields=['id','mcc_name'],where={'mcca_id':mcca_id})
            datas['mccs'] = results_mcc
        except:
            return json.dumps({'code': 0, 'msg': 'fail', 'data': {}})
        return json.dumps({'code':200,'msg':'success','data':datas})


class OfficialAccountsManage(core.Handler):
    @checkIsLogin
    def GET(self):
        uname = self.get_cookie('uname')
        data = {}
        data['uname'] = uname
        self.write(template.render('OfficialAccountsManage.html', data=data))


class GetAppID(core.Handler):
    '''获取公众号列表'''

    @checkIsLogin
    @with_database(['wxmp_customer'])
    def POST(self):
        data = self.req.input()

        mode = data.get('mode', 'all')
        where = {'status' : 1}
        if mode == 'wx_manage':
            if getattr(config, 'WX_MANAGE_APPIDS', None) is not None:
                where['appid'] = ('in', config.WX_MANAGE_APPIDS)

        try:
            mp_conf = self.db['wxmp_customer'].select(
                table='mp_conf', fields='appid, nick_name',
                where=where
            )
        except:
            return json.dumps({'code': 0, 'msg': 'fail', 'data': {}})

        return json.dumps({'code':200,'msg':'success','data':{'appid' : mp_conf}})


class test(core.Handler):
    @checkIsLogin
    def POST(self):
        params = self.req.inputjson()
        draw = params.get('draw')
        start = int(params.get('start'))
        length = int(params.get('length'))
        arr = []
        for i in range(start,start+length):
            data = {}
            data['userid'] = 1000+i
            data['username'] = '钱方好近'
            data['mcc'] = 10001
            data['pro'] = '北京市'
            data['city'] = '北京市'
            data['qudao'] = 190897
            data['qudao_type'] = 3
            data['last_time'] = '2018-03-13 23:12:34'
            data['attention_name'] = '钱方好近'
            data['xifen'] = '20%'
            data['attention_time'] = '2018-03-13 23:12:34'
            arr.append(data)
        recordsTotal = 2000
        recordsFiltered = 2000
        uids = []
        for i in range(5000):
            uids.append(i+1000)

        # results_wft = self.db['qf_weifutong'].select(table='amchnl_bind',fields=['id','userid'])
        # print results_wft

        return json.dumps({'draw': draw, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsFiltered,'data':arr,'code':200, 'uids':uids},ensure_ascii=False)


class MerchantConfig(core.Handler):
    @checkIsLogin
    def GET(self):
        uname = self.get_cookie('uname')
        data = {}
        data['uname'] = uname
        data['chnlcode_config'] = config.CHNLCODE_CONFIG
        data['dis_all'] = getattr(config, 'IS_DIS_ALL', True)

        self.write(template.render('MerchantConfig.html', data=data))


class testManage(core.Handler):
    @checkIsLogin
    def POST(self):
        params = self.req.inputjson()
        draw = params.get('draw')
        start = int(params.get('start'))
        length = int(params.get('length'))
        arr = []
        for i in range(start,start+length):
            data = {}
            data['id'] = i
            data['time'] = '2018-03-01'
            data['appname'] = '钱方好近'
            data['appid'] = 'wx3487265879658356'
            data['shop_num'] = 50
            data['weixin_num'] = 40
            data['fensi_num'] = 190897
            data['xifen'] = '20%'
            data['total'] = 300000
            arr.append(data)
        recordsTotal = 2000
        recordsFiltered = 2000
        ids = []
        for i in range(2000):
            ids.append(i)

        return json.dumps({'draw': draw, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsFiltered,'data':arr,'code':200, 'ids':ids},ensure_ascii=False)


class GetMerchantConfigSelectData(core.Handler):
    @checkIsLogin
    @with_database(['wxmp_customer','qf_mis','qf_qudao','qf_fund2','qf_core'])
    def POST(self):
        try:
            datas = {}

            where = {'status' : 1}
            if getattr(config, 'WX_MANAGE_APPIDS', None) is not None:
                where['appid'] = ('in', config.WX_MANAGE_APPIDS)
            # 微信名称和appID
            results_mp_conf = self.db['wxmp_customer'].select(
                table='mp_conf', fields=['appid', 'nick_name'],
                where=where
            )

            mp_conf = []
            wechat_id = []
            wechat_name = []
            for data in results_mp_conf:
                # if data.get('appid') and data.get('nick_name'):
                mp_conf.append(data)
                wechat_id.append(data.get('appid'))
                wechat_name.append(data.get('nick_name'))
            datas['id_names'] = mp_conf
            datas['IDtoName'] = dict(zip(wechat_id,wechat_name))
            # datas['id_names'] = results_mp_conf
            # 全部的省份信息
            results_area_p = self.db['qf_mis'].select(table='tools_area',fields=['id','area_name'])
            datas['provinces'] = results_area_p
            pro_nameArr = []
            pro_idArr = []
            for result in results_area_p:
                pro_idArr.append(result.get('id'))
                pro_nameArr.append(result.get('area_name'))
            id_pro = dict(zip(pro_nameArr,pro_idArr))
            datas['id_pro'] = id_pro
            # mcc一级
            results_mcc_a = self.db['qf_mis'].select(table='tools_mcca', fields=['id', 'mcca_name'])
            datas['mcca'] = results_mcc_a
            mcca_idArr = []
            mcca_nameArr = []
            for result in results_mcc_a:
                mcca_idArr.append(result.get('id'))
                mcca_nameArr.append(result.get('mcca_name'))
            # 封装成ID为key name为value的字典格式
            id_mcca = dict(zip(mcca_idArr, mcca_nameArr))
            datas['id_mcca'] = id_mcca

            # 渠道信息
            qwhere = None
            # if not getattr(config, 'IS_DIS_ALL', True):
            #     qwhere = {'qu.type' : ('in', (4, 5, 6))}

            result_groupids = self.db['qf_qudao'].select_join(
                table1='qd_profile qp', table2='qd_user qu',
                on={'qp.qd_uid' : 'qu.qd_uid'},
                fields=['qp.qd_uid', 'qp.name'],
                where = qwhere
            )
            old = self.db['qf_mis'].select(table='channel_crm', fields=['channelid', 'channelname'])
            datas['groupids'] = result_groupids
            for v in old:
                datas['groupids'].append({'qd_uid':v['channelid'],'name':v['channelname']})

            groupid = []
            groupname = []
            for result in result_groupids:
                groupid.append(result.get('qd_uid'))
                groupname.append(result.get('name'))
            groupIDtoName = dict(zip(groupid,groupname))
            datas['groupIDtoName'] = groupIDtoName

            # mcc二级
            result_mccs = self.db['qf_mis'].select(table='tools_mcc', fields=['id','mcc_name'])
            mcc_idArr = []
            mcc_nameArr = []
            for result in result_mccs:
                mcc_idArr.append(result.get('id'))
                mcc_nameArr.append(result.get('mcc_name'))
            # 封装成ID为key name为value的字典格式
            id_mcc = dict(zip(mcc_idArr,mcc_nameArr))
            datas['id_mcc'] = id_mcc

            fund2_result = self.db['qf_core'].select(table='channel', fields=['code', 'name'])
            fund2_dic = {}
            for i in fund2_result:
                try:
                    keystr = int(i.get('code', 0))
                    fund2_dic[keystr] = i['name']
                except Exception, e:
                    pass
            datas['chnlidToName'] = fund2_dic
        except Exception, e:
            return json.dumps({'code':0,'msg':'数据获取失败，请刷新重试！','data':{}})
        return json.dumps({'code':200,'msg':'success','data':datas})
