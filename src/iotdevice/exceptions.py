from rest_framework import status
from rest_framework.exceptions import APIException


class DeviceVerificationFailed(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'device not found or is verified before'
    default_code = 'verification_failed'


class DeviceCommandExecutionFailure(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'command execution_failed'
    default_code = 'device_not_found'


class DeviceNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'could not find device with given device_id'
    default_code = 'device_not_found'


class DeviceCreationFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'could not create device with given device_id'
    default_code = 'device_creation_failed'
