from django.shortcuts import render


def main_introduction(req):
    """
        '' url 소개 페이지
    """
    return render(req, 'main_introduction.html')

def kakaomaps(req):
    """
        kakaomaps toy page
    """
    
    return render(req, 'kakaomap.html')