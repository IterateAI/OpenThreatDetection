#!/bin/bash

CLIENT_ID="iofmzyQz73woC7k3XIPopMHIqN8sRIZV"
CLIENT_SECRET="a7LubwnuCsAFWiVZVQ0te9RHwitE1TURzkJFXLb_se9cGRAgyjIojhLEqDzK0h-C"
#curl --request POST --url https://staginglogin.raptortech.com/oauth/token --header &apos;content-type: application/json&apos; --data &apos;{"client_id":"$CLIENT_ID","client_secret":"$CLIENT_SECRET","audience":" [https://api-stag.raptortech.com%22,%22grant_type%22:%22client_credentials%22%7d&apos]https://api-stag.raptortech.com","grant_type":"client_credentials"}&apos; 
#curl --request POST \
#     --url https://staginglogin.raptortech.com/oauth/token 
#     --header 'content-type: application/json' 
#     --data '{"client_id":"$CLIENT_ID","client_secret":"$CLIENT_SECRET","audience":" [https://api-stag.raptortech.com%22,%22grant_type%22:%22client_credentials%22%7d']https://api-stag.raptortech.com","grant_type":"client_credentials"}' 
echo $CLIENT_ID
echo $CLIENT_SECRET

curl --request POST \
     --url "https://staginglogin.raptortech.com/oauth/token" \
     --header "content-type: application/json" \
     --data '{"client_id":"iofmzyQz73woC7k3XIPopMHIqN8sRIZV","client_secret":"a7LubwnuCsAFWiVZVQ0te9RHwitE1TURzkJFXLb_se9cGRAgyjIojhLEqDzK0h-C","audience":"https://api-stag.raptortech.com","grant_type":"client_credentials"}' 
