Completed work:
+ The function-based view is changed to the class-based view (UserCreateAPIView)
where the user registration (creation) is used.

+ The UserCreateSerializer is created in order to be used with
the UserCreateAPIView.

+ The UserCreateSerializer takes only email and password as fields
for creating the user.

+ The UserCreateSerializer excludes the password from the response.

+ The simplejwt library is used by /auth/token/ API endpoint for obtaining
the access JWT token.
