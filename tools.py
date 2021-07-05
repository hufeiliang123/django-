# @Time : 2021/7/4 10:36 上午
# @Author : Bais
# @Email : 17343001493@163.com
# @File : tools.py
import re


class Verify:
    RE_CHINESE = re.compile(r'^[\u4e00-\u9fa5]{1,8}$')
    RE_PASSWORD = re.compile(r'^[\d\w]{2,17}$')

    @classmethod
    def verify_str(cls, str):
        if ' ' in str:
            str = str.replace(' ', '')
            print(str)
        if str != 'null':
            verify_one = cls.RE_CHINESE.findall(str)

            verify_two = cls.RE_PASSWORD.findall(str)

            if len(verify_two) or len(verify_one):
                return str

    @classmethod
    def verify_phone(cls, phone):
        ret = re.match(r'^1[35678]\d{9}$', phone)
        if ret:
            return phone

    @classmethod
    def verify_email(cls, email):
        ret = re.match(r'^[\d\w]{7,20}@+[\d\w]+\.com$', email)
        if ret:
            return email


if __name__ == '__main__':
    print(Verify.verify_str("好  iiii"))
    print(Verify.verify_phone('"'))
    print(Verify.verify_email("li_122344422@*qq.com"))
