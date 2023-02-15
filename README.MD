# Oddam
*Oddam is a Django web application where users can donate to institutions or charities of their choosing.*
## Main features:
- Landing page designed to encourage using the application.
- Administrator profile
- Login page
- Review of submitted gifts
- User profile
- Registration
- Login (using the same form as for administrators)
- Adding donations
- Reviewing submitted donations

## Additional functionalities:
- Marking a gift as delivered (archiving)
- Editing one's own profile
- Account confirmation/activation via an email message sent to the address provided during registration
- Handling of forgotten passwords
- Validation of correct input of two identical passwords
- Validation of the management of administrators (e.g. prevention of deletion of the last existing administrator)
- Handling of a contact form

## Instalation: 
# Docker: 
Clone the repository:
```bash
https://github.com/M-Wasilewski92/Oddam-w-dobre-rece.git 
```
Set up environmental variables in .env file located in project root.

DJ_SECRET_KEY= "Secret Key" 
You can generete Django secret or get one frome thi website: https://djecrety.ir/

DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
Use this path 

DJ_DEBUG=1

Build up container:
```BASH
  docker-compose up --build
```
 
Superuser already created within initial migrations
```
username='Admin@admin.com',
email='Admin@admin.com',
password='StrongAdminPassword1!
```
User are also created:
```
username='Test@user.com',
email='Test@user.com',
password='StrongUserPassword1!'
```