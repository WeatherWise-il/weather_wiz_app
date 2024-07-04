
![Logo](https://raw.githubusercontent.com/WeatherWise-il/weather_wiz_app/aba8e3da3e69f46ce384898e0346327e422e2cf3/backend/static/images/navbar_logo.svg)


# Weather WIZ
Weather Wiz is an intuitive weather forecasting application developed using Python Flask and a MySQL database, catering to global users who seek detailed weather updates. Leveraging the Weatherbit REST API, it provides accurate daily forecasts for an extensive list of cities worldwide. Users can access not only the current temperature but also daily maximum and minimum temperatures, along with sunrise and sunset times. This comprehensive data helps users plan their day better, whether they're considering travel, outdoor activities, or just everyday planning. The user-friendly interface ensures easy navigation through the app, making weather information readily accessible at your fingertips.




## Installation using Docker-compose
To Build the Docker images:
```bash
  docker compose build 
```

To run Docker containers:
```bash
  docker compose up -d 
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY` 

`ANOTHER_API_KEY`



## Authors

- [@Michael Shechter](https://github.com/MichaelShechter)
- [@Idan Cohen](https://github.com/IdanCohen)
- [@Or Guetta](https://github.com/orguetta)


## API Reference

#### Get all items

```http
  GET /api/items
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get item

```http
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### add(num1, num2)

Takes two numbers and returns the sum.

