from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def manager_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type==1,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    
    return actual_decorator