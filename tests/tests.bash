#!/bin/bash

# URL of the Flask app
BASE_URL="http://localhost:80"

# Function to check the status code
check_status_code() {
    local endpoint=$1
    local expected_status=$2
    local actual_status

    echo "$BASE_URL$endpoint"
    actual_status=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL$endpoint")
    if [ "$actual_status" -eq "$expected_status" ]; then
        echo "PASS: $endpoint returned status code $actual_status"
    else
        echo "FAIL: $endpoint returned status code $actual_status, expected $expected_status"
    fi
}

# Function to check the response content
check_response_content() {
    local endpoint=$1
    local expected_content=$2
    local actual_content

    
    echo "$BASE_URL$endpoint"
    if echo "$actual_content" | grep -q "$expected_content"; then
        echo "PASS: $endpoint returned expected content"
    else
        echo "FAIL: $endpoint did not return expected content"
        echo "Expected: $expected_content"
        echo "Actual: $actual_content"
    fi
}

# Test cases

echo "Runnig test case #1 - App UI availability"
echo $(check_status_code "/" 200)


echo  "Running test case #2 - Calling GET request to  city_weather endpoint"
cities=("Paris" "New York City" "Tel aviv ")
for city in "${cities[@]}"; do
    encoded_city=$(echo "$city" | jq -sRr @uri)
    echo $(check_status_code "/city_weather?city=$encoded_city" 200)
done
