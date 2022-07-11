export class ApiService {
  healthCheck() {
    return new Promise((resolve) =>
      fetch("/healthcheck", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
      })
        .then((response) => checkResponse(response))
        .then((response) => resolve(response.json()))
        .catch((error) => console.error(error))

    );
  }
}

const checkResponse = (response) => {
  if (response.ok) {
    return response;
  }
  return response.text().then((e) => {
    throw new Error(e);
  });
};
