from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError
import os

app = Flask(__name__)

# Load AWS credentials from environment variables or configuration file
AWS_ACCESS_KEY = 'AKIAZMZVW2DE3PHR24VD'
AWS_SECRET_KEY = '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'
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')  # Default region is 'us-east-1'

# Configure AWS DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Reference the DynamoDB table
table_name = 'SampleTable'
table = dynamodb.Table(table_name)

# Create a new item
@app.route('/create', methods=['POST'])
def create_item():
    data = request.json
    try:
        table.put_item(Item=data)
        return jsonify({'message': 'Item created successfully', 'item': data}), 201
    except ClientError as e:
        return jsonify({'error': e.response['Error']['Message']}), 500

# Read an item by ID
@app.route('/read/<string:item_id>', methods=['GET'])
def read_item(item_id):
    try:
        response = table.get_item(Key={'id': item_id})
        if 'Item' in response:
            return jsonify(response['Item']), 200
        else:
            return jsonify({'message': 'Item not found'}), 404
    except ClientError as e:
        return jsonify({'error': e.response['Error']['Message']}), 500

# Update an item
@app.route('/update/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    try:
        # Update the item with new attributes
        update_expression = "SET " + ", ".join(f"{k}=:{k}" for k in data.keys())
        expression_attribute_values = {f":{k}": v for k, v in data.items()}
        table.update_item(
            Key={'id': item_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return jsonify({'message': 'Item updated successfully'}), 200
    except ClientError as e:
        return jsonify({'error': e.response['Error']['Message']}), 500

# Delete an item
@app.route('/delete/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        table.delete_item(Key={'id': item_id})
        return jsonify({'message': 'Item deleted successfully'}), 200
    except ClientError as e:
        return jsonify({'error': e.response['Error']['Message']}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
