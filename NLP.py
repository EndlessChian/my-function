# coding: utf-8
import os
import base64
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdknlp.v2.region.nlp_region import NlpRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdknlp.v2 import *

# https://nlp-ext.cn-north-4.myhuaweicloud.com/v1/{project_id}/nlg/summarization/domain

def SummaryDomain(request, title, content, length):
    request.body = SummaryDomainReq(
        type=0,
        content=content,
        lang="zh",
        title=title,
        length_limit=length,
    )
    # "https://{endpoint}/v1/{project_id}/nlg/summarization/domain"
    """{
     "Authorization": "******",
     "X-Sdk-Content-Sha256": "UNSIGNED-PAYLOAD",
     "X-Security-Token": "******",
     "User-Agent": "API Explorer",
     "Host": "nlp-ext.cn-north-4.myhuaweicloud.com",
     "X-Language": "zh-cn",
     "X-Project-Id": "2d9fe0246ff147f28564b09c4d3554d5",
     "X-Sdk-Date": "20231029T143140Z",
     "Content-Type": "application/json"
    }"""
    response = client.run_summary_domain(request)
    """{
     "Server": "api-gateway",
     "X-Request-Id": "755606bdd067f47e51fb4f21cefa3885",
     "Connection": "keep-alive",
     "Content-Length": "151",
     "X-ModelArts-Trace-ID": "755606bdd067f47e51fb4f21cefa3885",
     "X-ModelArts-Latency": "291",
     "X-ModelArts-Service-Version": "1.0.82",
     "Date": "Sun, 29 Oct 2023 14:31:40 GMT",
     "Content-Type": "application/json;charset=UTF-8"
    }"""
    print(response.to_dict()["summary"])
    """{
     "summary": "北京，10月24日—为庆祝第78个联合国日，联合国驻华系统24日在北京的联合国大楼举办了一场特别活动。"
    }"""

if __name__ == "__main__":
    ak = "SWU3YHY09IVYBCIGDLYL"
    sk = "tdUaqzX0T1RmFnUWAwkg7c6D9pL9DJVeSkaR5XjX"

    credentials = BasicCredentials(ak, sk)

    client = NlpClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(NlpRegion.value_of("cn-north-4")) \
        .build()

    try:
        request = RunSummaryDomainRequest()
        SummaryDomain(request, "以“为可持续发展目标即刻行动”为主题的联合国日庆祝活动在北京联合国大楼举办", """
北京,10月24日—为庆祝第78个联合国日,联合国驻华系统24日在北京的联合国大楼举办了一场特别活动。超过170位嘉宾受邀出席,包括中国政府代表、各国大使、联合国驻华各机构代表,以及来自学术界、企业界、民间团体和其他相关领域的合作伙伴。

Guests at the 78th United Nations Day
图片说明:庆祝第78个联合国日特别活动现场嘉宾
10月24日的联合国日是《联合国宪章》于1945年正式生效的周年纪念。每年一度的庆祝活动提供了一个契机,让我们重申过去78年内一直指导着联合国和国际社会的《联合国宪章》的宗旨及原则。

今年联合国日的主题是“为可持续发展目标即刻行动”,旨在为加速推进可持续发展目标进入新阶段提高意识、促进对话、动员力量,进一步彰显联合国在和平与安全、人权和发展三大支柱领域的号召力。

联合国秘书长安东尼奥·古特雷斯在全球视频致辞中表示:“联合国以永恒的价值观和原则为指导,但绝不能止步不前。因此,我们必须不断加强工作方法,以21世纪的眼光看待我们所做的一切。”

Video message from Mr. Antonio Guterres, UN Secretary-General
图片说明:联合国秘书长安东尼奥·古特雷斯的视频致辞
中华人民共和国外交部副部长马朝旭阁下作为贵宾,连同其他中国政府代表出席了本次活动,体现了中国对联合国一如既往的支持。

中华人民共和国外交部副部长马朝旭阁下在致辞中首先祝贺联合国成立78周年,并表示当前世界比以往任何时候都更加需要一个强有力的联合国。他强调,中方将一如既往地支持联合国驻华机构坚持发展优先,深度参与中国式现代化进程,全力推动中国同联合国合作取得新的更大成效。

His Excellency Mr. Ma Zhaoxu, Executive Vice Minister of Foreign Affairs, Ministry of Foreign Affairs of the People’s Republic of China
图片说明:中华人民共和国外交部副部长马朝旭阁下致辞
联合国驻华协调员常启德以及联合国驻华各机构代表全程出席此次活动。常启德先生在致辞中呼吁为可持续发展目标、健康的环境、更好的经济、公正的社会以及人们合作的世界重振多边主义。

联合国驻华协调员常启德在致辞中说:“我们的多边系统正面临前所未有的重重压力,部分地区危机和其他全球挑战有可能使其分崩离析,但在这些裂痕面前我们绝不能束手就擒。唯有通过国际合作,以及一个焕发活力且更为强大的联合国和多边体系,我们才能携手找到这些问题对应的方案,并将他们逐一解决。”

Mr. Siddharth Chatterjee, UN Resident Coordinator in China
图片说明:联合国驻华协调员常启德致辞
为介绍联合国为落实合作框架、实现可持续发展目标以及不让任何一个人掉队所做的工作和努力,联合国驻华各机构在活动现场还向来宾展示了相关出版物、报告以及其他材料。

Exhibition of publications from UN Entities
图片说明:联合国各驻华机构出版物展示
活动致辞结束后,中西融合的视听盛宴携带着团结的希望与祝福在舞台绽放。现场嘉宾不仅欣赏了潮州儿童合唱团演唱的《天下一心》、古琴表演、琵琶表演,还聆听了《欢乐颂》四重奏。

Guests viewing performance at the 78th UN Day
图片说明:嘉宾正在观看第78个联合国日的现场表演
联合国驻华系统诚挚感谢所有合作伙伴的付出,并衷心感谢所有嘉宾出席今年的联合国日活动。""", 200)

    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)

