from firebase import firebase
fb_app = firebase.FirebaseApplication('https://your_storage.firebaseio.com', authentication=None)
result = fb_app.get('/users', None, {'print': 'pretty'})
print (result)
# {'error': 'Permission denied.'}

authentication = firebase.FirebaseAuthentication('THIS_IS_MY_SECRET', 'ozgurvt@gmail.com', extra={'id': 123})
fb_app.authentication = authentication
print (authentication.extra)
# {'admin': False, 'debug': False, 'email': 'ozgurvt@gmail.com', 'id': 123, 'provider': 'password'}

user = authentication.get_user()
print (user.firebase_auth_token)


# with query
fb_app = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)
result = fb_app.get('/users/2', None, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
