def message(domain, uidb64, token):
    return f"아래 링크를 클릭하면 회원가입이 인증이 완료됩니다.\n\n" \
           f"회원가입 링크: http://{domain}/auth/activate/{uidb64}/{token}\n\n" \
           f"감사합니다."
