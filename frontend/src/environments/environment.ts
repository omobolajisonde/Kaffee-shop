export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'udacity-kaffee-shop.us.auth0.com', // the auth0 domain prefix
    audience: 'kaffe-shop', // the audience set for the auth0 app
    clientId: 'aNjCOBpj2vmxgzqJPx3zDMGCcocZB6KX', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
