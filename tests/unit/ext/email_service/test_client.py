from chargeapi.ext.email_service import EmailApiClient


async def test_email_notify_service():
    email_client = EmailApiClient(api_key='abcdef')
    email_client.from_("teste@gmail.com")
    email_client.to("harry@hogwarts.com")
    email_client.subject("Boleto Bancário")
    email_client.body("Olá")

    response = await email_client.notify()
    assert response.to == "harry@hogwarts.com"
    assert response.from_ == "teste@gmail.com"
    assert response.subject == "Boleto Bancário"
    assert response.body == "Olá"
