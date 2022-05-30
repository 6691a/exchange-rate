from ninja import Router


router = Router()

from ...tasks import send_exchange_rate

@router.get("test/")
def test(request):
    send_exchange_rate()
    return 200
