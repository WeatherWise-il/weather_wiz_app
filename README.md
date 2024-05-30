
![Logo](https://raw.githubusercontent.com/WeatherWise-il/weather_wiz_app/aba8e3da3e69f46ce384898e0346327e422e2cf3/backend/static/images/navbar_logo.svg)


# Weather WIZ
Weather wiz  is  brand new weather




## Installation



```bash
  npm install my-project
  cd my-project
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

