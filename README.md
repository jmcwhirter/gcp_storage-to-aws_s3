

### Package function
1. Package libraries  
__Don't skip or optimize these steps. Zip creation is funky.__  
```
python3 -m venv env
source env/bin/activate
pip3 install google-cloud-storage
deactivate
cd env/lib/python3.7/site-packages
zip -r9 ../../../../function.zip .
cd ../../../../
```
2. Package code  
```
zip function.zip list_buckets.py gcp.json
```

### Upload and store the function
1. Create S3 bucket
  ```
  aws cloudformation create-stack \
    --stack-name gcp-to-aws-storage \
    --template-body file://cloudformation/s3.yml \
    --region us-east-1
  ```
2. Get S3 bucket name (may have to wait a few seconds)
  ```
  aws cloudformation describe-stacks \
    --stack-name gcp-to-aws-storage \
    --query 'Stacks[0].Outputs[0].OutputValue' \
    --output text
  ```
3. Upload function code to S3
  ```
  aws s3 cp function.zip s3://<bucket_name>
  ```

### Create function
1. Update the bucket name in `cloudformation/lambda-parameters.json`
2. Create the Lambda resources
```
aws cloudformation create-stack \
  --stack-name gcp-to-aws-function \
  --template-body file://cloudformation/lambda.yml \
  --parameters file://cloudformation/lambda-parameters.json \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1
```

### Test
1. Log in to AWS Console
2. Navigate to 'GCPtoAWS' function
3. Create a test named 'test' with default payload
4. Run the test

Expected output should look like this:
```
START RequestId: 07e75f2b-041f-4a25-b558-6f4e0162fc18 Version: $LATEST
[<Bucket: _____>, <Bucket: ____>, <Bucket: ____>]
END RequestId: 07e75f2b-041f-4a25-b558-6f4e0162fc18
REPORT RequestId: 07e75f2b-041f-4a25-b558-6f4e0162fc18	Duration: 1201.87 ms	Billed Duration: 1300 ms 	Memory Size: 128 MB	Max Memory Used: 81 MB
```

If you need to update your function code, use this short cut:
```
aws lambda update-function-code --function-name GCPtoAWS --zip-file fileb://function.zip
```

### Tear down stacks
1. Tear down storage
```
aws s3 rm --recursive s3://<bucket_name>
aws cloudformation delete-stack \
  --stack-name gcp-to-aws-storage \
  --region us-east-1
```
2. Tear down function
```
aws cloudformation delete-stack \
  --stack-name gcp-to-aws-function \
  --region us-east-1
```

### Misc
```
pip3 freeze > requirements.txt
pip3 install -f requirements.txt
```
