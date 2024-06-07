# coding: utf-8
import logging

import base64
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.http.http_config import HttpConfig
from huaweicloudsdkcore.http.http_handler import HttpHandler
from huaweicloudsdkvpc.v2 import VpcClient, ListVpcsRequest
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
from huaweicloudsdkcore.exceptions import exceptions

# 导入指定云服务的库 huaweicloudsdk{service}
from huaweicloudsdkocr.v1.region.ocr_region import OcrRegion
from huaweicloudsdkocr.v1 import *


if __name__ == "__main__":
    # 配置认证信息
    # 如果未填写project_id，SDK会自动调用IAM服务查询所在region对应的项目id
    credentials = BasicCredentials("JJDT6GQW4TLFNQTRP2O2", "pJFvDyG6PnIADpQvBzdwdSTliUrxQuy66oohNuI8", project_id="099eaa1f7000f50e2f3fc0047844717f") \
        .with_iam_endpoint(
        "https://iam.cn-north-4.myhuaweicloud.com")  # 配置SDK内置的IAM服务地址，默认为https://iam.myhuaweicloud.com

    # # 使用默认配置
    # http_config = HttpConfig.get_default_config()
    # # 配置是否忽略SSL证书校验， 默认不忽略
    # http_config.ignore_ssl_verification = True
    # # 配置CA证书文件
    # http_config.ssl_ca_cert = '/path/to/certfile'
    # # 默认连接超时时间为60秒，读取超时时间为120秒，可根据需要配置
    # http_config.timeout = (60, 120)
    # # 根据需要配置网络代理
    # http_config.proxy_protocol = 'http'
    # http_config.proxy_host = 'proxy.huaweicloud.com'
    # http_config.proxy_port = 80
    # http_config.proxy_user = 'username'
    # http_config.proxy_password = 'password'


    # 注册监听器用于打印原始的请求和响应信息, 请勿用于生产环境
    def response_handler(**kwargs):
        response = kwargs.get("response")
        request = response.request

        info = "> Request %s %s HTTP/1.1" % (request.method, request.path_url) + "\n"
        if len(request.headers) != 0:
            info = info + "> Headers:" + "\n"
            for each in request.headers:
                info = info + "    %s: %s" % (each, request.headers[each]) + "\n"
        info = info + "> Body: %s" % request.body + "\n\n"

        info = info + "< Response HTTP/1.1 %s " % response.status_code + "\n"
        if len(response.headers) != 0:
            info = info + "< Headers:" + "\n"
            for each in response.headers:
                info = info + "    %s: %s" % (each, response.headers[each],) + "\n"
        info = info + "< Body: %s" % response.content
        print(info)


    # http_handler = HttpHandler().add_response_handler(response_handler)

    # 创建服务客户端
    # 配置认证信息
    # 配置地区, 如果地区不存在会抛出KeyError
    # HTTP配置
    # 配置请求日志输出到控制台
    # 配置请求日志输出到文件
    # 配置HTTP监听器
    client = OcrClient.new_builder() \
        .with_credentials(credentials) \
    .with_region(VpcRegion.value_of("cn-north-4")) \
    .build()
    # .with_http_config(http_config) \
    # .with_stream_log(log_level=logging.INFO) \
    # .with_file_log(path="test.log", log_level=logging.INFO) \
    # .with_http_handler(http_handler) \
    # .build()# 增加region依赖
    # 初始化指定云服务的客户端 {Service}Client ，以初始化OCR服务的 OcrClient 为例

# 发送请求并获取响应
try:
    # 以调用通用表格识别接口 RecognizeGeneralTable 为例
    # request = RecognizeGeneralTableRequest()
    request.body = GeneralTableRequestBody(
        url="https://img-blog.csdnimg.cn/img_convert/2caf89d1cc044e3da9a2bd2c5a8f8018.png",
        detect_direction=True,
        single_orientation_mode=False,

        character_mode=False,
    )
    response = client.recognize_general_table(request)
    print(response)
    # 异常处理
except exceptions.ClientRequestException as e:
    print(e.status_code)
    print(e.request_id)
    print(e.error_code)
    print(e.error_msg)