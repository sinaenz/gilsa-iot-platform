from rest_framework import status
from rest_framework.exceptions import APIException


class UserAlreadyExist(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'این شماره قبلا در سیستم ثبت شده است'
    default_code = 'already_exist'


class VerificationIsRequired(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'verify'
    default_code = 'verify'


class UserVerificationFailed(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'کد وارد شده نادرست است'
    default_code = 'verification_failed'


class UserSendSmsFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'ارسال ناموفق پیامک'
    default_code = 'sms_send_failed'


class UserLoginFailed(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'شماره و یا رمز عبور اشتباه است'
    default_code = 'login_failed'


class UserChangePasswordFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'ابتدا درخواست فراموشی رمز را ارسال کنید'
    default_code = 'change_password_failed'
