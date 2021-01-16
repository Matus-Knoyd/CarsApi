MESSAGES  = {
    'token_expired': 'The token has expired.',
    'invalid_token': 'Signature verification failed.',
    'authorization_required': 'Request does not contain an access token',
    'fresh_token_required': 'The token is not fresh.',
    'token_revoked': 'The token has been revoked.',
    'admin_required': 'Admin privilege required.',
    'association_created_updated': 'Association created/updated sucesfully!',
    'owner_not_found': 'Owner not found.',
    'owner_created': 'Owner created successfully.',
    'owner_already_exists': 'A owner with that identity already exists.',
    'owners_not_found': 'Owners not found.',
    'car_not_found': 'Car not found.',
    'car_created': 'Car created successfully.',
    'car_deleted': 'Car deleted.',
    'cars_not_found': 'Cars not found.',
    'car_vin_exists': 'A car with that vin-number already exists.',
    'user_created': 'User created successfully.',
    'user_not_found': 'User not found.',
    'user_deleted': 'User deleted.',
    'user_username_exists': 'A user with that username already exists.',
    'login_for_details': 'Login to get more details!',    
    'invalid_credentials': 'Invalid credentials!',
    'logged_out': 'Successfully logged out.'
}

def get_message(name):
    return MESSAGES.get(name, 'Message not implemennted!')
