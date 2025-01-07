import boto3
import json
import os
import logging

# Configuração básica do logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def put_record_to_firehose(delivery_stream_name, records):
    """
    Envia um registro para um Delivery Stream do Kinesis Firehose.

    :param delivery_stream_name (str): O nome do Delivery Stream.
    :param records (dict): O dado a ser enviado como um JSON.

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
        logger.info(
            f"Registro enviado com sucesso: {response['ResponseMetadata']['HTTPStatusCode']}"
        )
        return response
    except Exception as e:
        logger.error(f"Erro ao enviar o registro: {e}", exc_info=True)
        raise
