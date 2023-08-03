from http import HTTPStatus


async def test_upload_of_csv(bytes_reader, async_client):
    data = {"file": bytes_reader("bank_slip.csv").decode("utf-8")}
    headers = {
        "Content-Type": (
            "multipart/form-data; boundary=----WebKitFormBoundaryUeSnTkqf3ohuBZqy"
        )
    }
    response = await async_client.post(f"/debts/ingest", files=data, headers=headers)
    assert response.status_code == HTTPStatus.CREATED
