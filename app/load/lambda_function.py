import boto3
import logging
import json
from botocore.exceptions import ClientError

# Configurar logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Inicializando clientes do S3 e SQS
s3 = boto3.client("s3")
sqs = boto3.client("sqs")

# Nome dos buckets
SOURCE_BUCKET = "bitcoin-near-real-time-bucket"
DEST_BUCKET = "bitcoin-backup"


def copy_file(source_bucket, dest_bucket, source_key):
    """
    Copia um arquivo de um bucket S3 para outro.
    """
    try:
        # Realiza a cópia do arquivo
        s3.copy_object(
            Bucket=dest_bucket,
            CopySource={"Bucket": source_bucket, "Key": source_key},
            Key=source_key,
        )
        logger.info(
            f"Arquivo {source_key} copiado de {source_bucket} para {dest_bucket}"
        )
    except ClientError as e:
        logger.error(f"Erro ao copiar {source_key}: {e}")


def process_sqs_messages(event):
    """
    Processa mensagens do SQS e copia arquivos mencionados para o bucket de backup.
    """
    for record in event.get("Records", []):
        try:
            # Obter o corpo da mensagem do SQS
            message_body = json.loads(record["body"])

            # Extrair a chave do arquivo do evento S3
            file_key = message_body["Records"][0]["s3"]["object"]["key"]
            logger.info(f"Processando arquivo: {file_key}")

            # Copiar o arquivo para o bucket de backup
            copy_file(SOURCE_BUCKET, DEST_BUCKET, file_key)
        except KeyError:
            logger.error("Mensagem no formato incorreto ou incompleta.")
        except json.JSONDecodeError:
            logger.error("Falha ao decodificar a mensagem do SQS.")


def lambda_handler(event, context):
    """
    Função principal para processar o evento SQS.
    """
    logger.info("Iniciando processamento do evento...")
    process_sqs_messages(event)
    logger.info("Processamento concluído.")
