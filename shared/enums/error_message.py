from enum import Enum

class ErrorMessageEnum(Enum):
    USER_EXISTS = "user_exists"
    COMPANY_EXISTS = "company_exists"
    COMPANY_DOESNT_EXISTS = "company_doesnt_exists"
    USER_NOT_FOUND = "user_not_found"
    INVALID_CREDENTIALS = "invalid_credentials"
    UNAUTHORIZED = "unauthorized"
    INVALID_VERIFICATION_CODE = "invalid_verification_code"
    PASSWORDS_DOESNT_MATCH = "passwords_doesnt_match"
    FILE_NOT_FOUND = "file_not_found"
    PAYMENT_EXCEEDS_PAYABLE_AMOUNT = "payment_exceeds_payable_amount"
    EMPLOYEE_ALREADY_HAS_SALARY = "employee_already_has_salary"
    BAD_REQUEST = "bad_request"