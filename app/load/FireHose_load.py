import boto3
import os
import json


def put_record_to_firehose(delivery_stream_name, records):
    """
    Envia um registro para um Delivery Stream do Kinesis Firehose.

    Args:
        delivery_stream_name (str): O nome do Delivery Stream.
        records (dict): O dado a ser enviado como um JSON.

    Returns:
        dict: Resposta da AWS para a solicitação.
    """
    # Inicializa o cliente do Firehose
    firehose_client = boto3.client(
        "firehose",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
        region_name=os.environ.get("AWS_REGION"),
    )

    data = {"Data": json.dumps(records)}

    try:
        # Envia o registro para o Delivery Stream
        response = firehose_client.put_record(
            DeliveryStreamName=delivery_stream_name, Record=data
        )
        print(f"Registro enviado com sucesso: {response}")
        return response
    except Exception as e:
        print(f"Erro ao enviar o registro: {e}")
        raise
