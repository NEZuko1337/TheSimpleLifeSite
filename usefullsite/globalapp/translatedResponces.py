def translateResponse(response: str) -> str:
    if response == 'PLEASE SELECT TWO DISTINCT LANGUAGES':
        return 'Выбраны два одинаковых языка, выбери разные'
    if response == 'NO QUERY SPECIFIED. EXAMPLE REQUEST: GET?Q=HELLO&LANGPAIR=EN|IT':
        return 'Введи, что ты хочешь перевести, нельзя перевести пустоту'
    if response == 'INVALID LANGUAGE PAIR SPECIFIED. EXAMPLE: LANGPAIR=EN|IT USING 2 LETTER ISO OR RFC3066 LIKE ZH-CN. ALMOST ALL LANGUAGES SUPPORTED BUT SOME MAY HAVE NO CONTENT':
        return 'Выбрана неправильная пара языков'
    else:
        return 'Возникла ошибка, проверь правильность введенной тобой информации'
