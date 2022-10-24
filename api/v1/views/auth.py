from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.models import Customer
from database.schemas import CustomerAuthSchema, BaseCustomerSchema, CustomerResultSchema, CustomerCreationSchema
from database.session import get_session
from security.hasher import Hasher
from security.jwt import JWT


auth_router = APIRouter(
    prefix='/auth',
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/token')


async def get_current_user(token=Depends(oauth2_scheme), session=Depends(get_session)) -> Customer:
    decoded_token = JWT.decode_token(token)
    username = decoded_token.get('username')
    user_from_db: Customer = await Customer.get_by_username(username, session)

    if not user_from_db:
        raise HTTPException(
            status_code=400, detail='This user does not exists')

    if not user_from_db.is_active:
        raise HTTPException(status_code=400, detail='This user is inactive')

    return user_from_db


async def change_password(token: str, customer: Customer = Depends(get_current_user), session=Depends(get_session)):
    pass


@auth_router.post('', status_code=201)
async def register_new_user(data: CustomerCreationSchema = Depends(CustomerCreationSchema.as_form), session=Depends(get_session)):
    customer = await Customer.exists(data.username, session=session)

    if customer:
        raise HTTPException(
            status_code=400, detail=f'User with username "{data.username}" already exists')

    if data.password != data.password_2:
        raise HTTPException(status_code=400, detail='Passwords does not match')

    try:
        result = await Customer.create(session=session, username=data.username, password=data.password)
    except Exception as e:
        raise e
    else:
        return {'success': True}


@auth_router.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)):
    user_from_db: Customer = await Customer.get_by_username(form_data.username, session)

    if not user_from_db or not Hasher.verify_password(
            form_data.password,
            user_from_db.password):
        raise HTTPException(
            status_code=400, detail='Incorrect username or password')

    user = CustomerAuthSchema.from_orm(user_from_db)

    access_token = JWT.gen_new_access_token(user.dict())

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post('')
async def forgot_password(username: str = Form(), session=Depends(get_session)):
    customer: Customer = Customer.get_by_username(username, session)
    if not Customer:
        raise HTTPException(status_code=400, detail='This customer does not exists')
    
    # password reset URL = generate_password_reset_url()
    # send_email_to_user(customer.email)
    return {'success': True}


@auth_router.get('/me')
async def me(current_user=Depends(get_current_user)):
    user = CustomerResultSchema.from_orm(current_user)
    return {'current_user': user}
