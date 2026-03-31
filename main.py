from domain.billing_parser import BillingParser

dollar_price = 0

while True:
    try:
        dollar_price = float(input("Ingresa el precio del dolar: ")) # 17.9218
        break
    except ValueError:
        print("Nuevamente...")

parser = BillingParser(dollar_price=dollar_price)

parser.start()