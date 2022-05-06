from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def main(request):
    return render(request, "main.html")


from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


def channels(request):
    # channel_layer.group_send(
    #     "USA", {
    #         type:
    #         "text":
    #     }
    # )
    # print(channel_layer)
    return render(request, "main.html")
