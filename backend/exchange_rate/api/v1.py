from ninja import Router

router = Router()

@router.get('/')
def get_exchange_rate(request):
    return {'message': 'Hello from V1'}