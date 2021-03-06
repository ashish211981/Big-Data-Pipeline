"""
Transfers 100 000 bytes per second from a CSV file to a Kafka topic.
"""

__author__ = "Mislav Jaksic"
__version__ = "0.1.0"
__license__ = "None"

from kafka import KafkaProducer
from csv import DictReader
from json import dumps

import context
from kafka_producer import settings



def SendCSVToKafkaTopic():
  kafka_producer = CreateKafkaProducer()
  row_generator = GenerateRowFromFile()
  
  for row in row_generator:
    clean_row = CleanUpRow(row)
    binary_JSON = TranformToBinaryJSON(clean_row)
    
    kafka_producer.send(topic=settings.kafka_topic, value=binary_JSON)

  DestroyKafkaProducer(kafka_producer)
  


def CreateKafkaProducer():
  """https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html"""
  return KafkaProducer(bootstrap_servers=settings.bootstrap_servers)



def GenerateRowFromFile():
  with open(settings.csv_file_name) as csv_file:
    dict_reader = DictReader(csv_file)
    for row in dict_reader:
      yield row
      
      
      
def CleanUpRow(row):
  row = CleanEmptyStrings(row)
  row = CleanDelemitersInValues(row)
  return row
  
def CleanEmptyStrings(row):
  for key, value in row.items():
    if (value == ""):
      row[key] = settings.empty_string_sentinel
  return row
  
def CleanDelemitersInValues(row):
  for key, value in row.items():
      row[key] = value.replace(settings.delimiter, settings.delimiter_in_value_sentinel)
  return row



def TranformToBinaryJSON(row):
  JSON_string = TransformToJSON(row)
  binary_JSON = EncodeToBinaryUTF(JSON_string)
  return binary_JSON
  
def TransformToJSON(data):
  return dumps(data)
  
def EncodeToBinaryUTF(string):
  return string.encode("utf-8")
  
  
  
def DestroyKafkaProducer(producer):
  producer.close()

  
  
def Run():
  SendCSVToKafkaTopic()
  
if __name__ == "__main__":
  Run()
