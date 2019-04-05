from rest_framework import status
from rest_framework.exceptions import APIException


class DeviceVerificationFailed(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'device not found or is verified before'
    default_code = 'verification_failed'


class DeviceNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'could not find device with given device_id'
    default_code = 'device_not_found'
