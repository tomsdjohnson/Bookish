export class ApiService {
  example() {
    return new Promise((resolve) =>
      fetch("/example", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => checkResponse(response))
        .then((response) => resolve(response.json()))
        .catch((error) => alert(error))
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
