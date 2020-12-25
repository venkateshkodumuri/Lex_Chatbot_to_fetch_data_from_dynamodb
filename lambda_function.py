import json
import boto3
client = boto3.client('dynamodb')
result = {}
intent=""
Accountnumber=""

def lambda_handler(event, context):
    intent=(event['currentIntent']['name'])
    #print('the intent is : ',intent)
    Accountnumber=(event['currentIntent']['slots']['AccountNumber'])
    #print('accountnumber is : ',Accountnumber)
    if intent=='AccountBalanceEnquiry':
        balanceenquiry(Accountnumber)
        return result


# Method to Fetch the account balance from database by giving the Accountnumber as paramater
def balanceenquiry(Accountnumber):
        response = client.get_item(
            TableName='customerdetails',
            Key={
                'accountnumber': {
                    'S': Accountnumber,
                }
            }
            )
        #print('responce is: ',response)
# Declaring a key to verify the response
        key='Item'
# Storing the boolean value wether key present or not
        value = key in response.keys()
        if value:
            accountnumber=response['Item']['accountnumber']['S']
            name=response['Item']['name']['S']
            balance=response['Item']['balance']['N']
            message='Hello ', name, ' You have $',balance, ' in your account'
            msg=''.join(message)
            #print(msg)
            global result
# Result to lex bot
            result = {
                "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                  "contentType": "PlainText",
                  "content": msg
                },
              }
            }       
            return result
        else:
            #print("didnt find the account")
            message="Sorry I can't find your details in our records please contact our support center on 8083829227"
            result = {
                "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                  "contentType": "PlainText",
                  "content": message
                },
              }
            }
            return result
