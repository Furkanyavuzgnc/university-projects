def calc_operation(op, a, b):
    """Dört işlem fonksiyonu"""
    if op == "toplama":
        return a + b
    elif op == "çıkarma":
        return a - b
    elif op == "çarpma":
        return a * b
    elif op == "bölme":
        if abs(b) <= 1e-12:  # Bölen 0 ise
            raise ZeroDivisionError("Bölen 0 olamaz!")
        return a / b
    else:
        raise ValueError("Geçersiz işlem türü.")

def check_result(expected, user_result, tolerance=1e-6):
    """Sonuç doğru mu diye kontrol eder (ondalık toleransla)"""
    return abs(expected - user_result) <= tolerance
