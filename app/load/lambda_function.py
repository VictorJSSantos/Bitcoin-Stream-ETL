import boto3
from datetime import datetime
import json
import logging
import os


# Setting basic configs for Logging purposes
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Creating the Client Object
glue = boto3.client("glue", region_name="us-east-1")

# Criação de cliente para o S3
s3 = boto3.client("s3")

# Nome do bucket S3 onde os arquivos serão armazenados
BUCKET_NAME = "backup-bitcoin"


def lambda_handler(event, context):
    """
    Handler da Lambda que processa eventos do SQS e salva os arquivos JSON no S3.
    """
    try:
        # Itera sobre os registros (mensagens) recebidos do SQS
        for record in event["Records"]:
            # A mensagem vem no campo body como string
            message_body = record["body"]

            # Parse do JSON (assumindo que o body contém um JSON válido)
            data = json.loads(message_body)

            # Nome do arquivo no S3 com timestamp único
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
            file_name = f"json_files/file_{timestamp}.json"

            # Salvar arquivo no S3
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=file_name,
                Body=json.dumps(data),
                ContentType="application/json",
            )

            print(f"Arquivo {file_name} salvo com sucesso no bucket {BUCKET_NAME}")

        return {"statusCode": 200, "body": "Mensagens processadas com sucesso."}

    except Exception as e:
        print(f"Erro ao processar mensagens: {e}")
        return {"statusCode": 500, "body": "Erro no processamento."}
