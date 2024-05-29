import boto3
import json
from decimal import Decimal

load_dotenv()

dynamodb = boto3.resource('dynamodb', region_name=os.getenv('DYNAMODB_REGION'))
table = dynamodb.Table(os.getenv(DYNAMODB_TABLE))

# Custom encoder for JSON serialization
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

response = table.scan()
data = response['Items']

while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    print(response)
    data.extend(response['Items'])

with open('dynamodb_data.json', 'w') as outfile:
    json.dump(data, outfile, cls=DecimalEncoder)

print("Data extracted and saved to dynamodb_data.json")
